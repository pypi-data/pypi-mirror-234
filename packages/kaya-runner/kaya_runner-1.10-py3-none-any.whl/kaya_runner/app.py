import argparse
import json
import os
import pkgutil
import logging
import subprocess
import sys
import importlib
import pip
#import pysnooper

from flask import Flask, request, jsonify
from kaya_runner.src.config import Config

DEFAULT = {
    'log-file': 'log/kaya_runner.log',
    'conf-file': 'conf/kaya_runner.conf.json',
    'host': '0.0.0.0',
    'port': 8080,
    'base-path': '/',
    'workers': 4,
    'debug-flag': False,
}
ENV = {
    'module-name': 'KAYA_MODULE_NAME',
    'module-version': 'KAYA_MODULE_VERSION',
}

log = logging.getLogger('KayaRunnerSDK')


class ModuleRunner:

#   @pysnooper.snoop()
    def __init__(self, module: str, debug_mode: bool = False,
                 host: str = '0.0.0.0', port: int = 8080) -> None:
        log.debug('')
        self.module = module
        self.server_host = host
        self.server_port = port
        self.app = Flask(__name__)
        self.app.config['DEBUG'] = debug_mode
        self.package_instance = None

    def setup_package_instance(self, package: str):
        log.debug('')
        loaded_pkg = import_package(f'{package}.module')
        class_ = getattr(loaded_pkg, 'KayaStrategyModule')
        instance = class_()
        self.package_instance = instance
        return self.package_instance

#   @pysnooper.snoop()
    def generate_module_route(self, package: str, module: str) -> bool:
        '''
        [ NOTE ]: Dynamically generates web server paths for each Strategy
            Module specified in the modules.json file.
        '''
        log.debug('')

#       @pysnooper.snoop()
        def module_route():
            '''
            [ INPUT ]: JSON request with module parameters

                {'args': [...], 'kwargs': {...}}

                [ Ex ]: Issue module args and kwargs via POST request

                    url = 'http://localhost:80/endpoint'
                    data = {
                        'args': ['value1', 'value2', ...],
                        'kwargs': {'key1': 'value1', ...}
                    }
                    response = requests.post(url, json=data)

            [ RETURN ]: JSON-ified dict

                -OK- {
                    'package': 'dummy',
                    'module': 'MyThing',
                    'args': ['value1', 'value2'],
                    'kwargs': {'key1': 'value1', ...},
                    'result': <module-return-value>
                }

                -NOK- {
                    'package': 'dummy',
                    'module': 'MyThing',
                    'args': ['value1', 'value2'],
                    'kwargs': {'key1': 'value1', ...},
                    'error': <error-string>
                }
            '''
            log.debug('')
            response = {'package': package, 'module': module,}
            data = request.get_json()
            if not isinstance(data, dict):
                data = json.loads(data)
            args = data.get('args', [])
            kwargs = data.get('kwargs', {})
            try:
                result = self.package_instance.modules[module].main(
                    *args, **kwargs
                )
                response.update({
                    'args': args,
                    'kwargs': kwargs,
                    'result': result,
                })
            except ImportError as e:
                log.error(e)
                response.update({'error': 'Package not found!'})
            except Exception as e:
                log.error(e)
                response.update({'error': 'Unknown exception occured!'})
            finally:
                return jsonify(response)

        self.app.route(
                f"{DEFAULT['base-path']}{package}/{module}",
                methods=['GET', 'POST'], endpoint=module,
            )(module_route)
        return True

#   @pysnooper.snoop()
    def generate_module_routes(self, package: str):
        log.debug('')
        ok, nok = [], []
        pkg_inst = self.setup_package_instance(package)
        for module in pkg_inst.modules:
            route = self.generate_module_route(package, module)
            if route:
                ok.append(route)
                log.info(
                    'Generated route for Kaya Strategy Module! '
                    f'({package}.{module})'
                )
            else:
                nok.append(route)
                log.error(
                    'Could not generate route for Kaya Strategy Module! '
                    f'({package}.{module})'
                )
        return {'ok': ok, 'nok': nok}

    # TODO - Use Production Server
#   @pysnooper.snoop()
    def start_server(self, package_name: str):
        log.debug('TODO - Use Production Server')
#       cmd = [
#           sys.executable, '-m', 'gunicorn', '--bind',
#           f'{DEFAULT["host"]}:{DEFAULT["port"]}',
#           '--workers', str(DEFAULT['workers']), 'kaya_runner.app:init'
#       ]
        try:
            route_gen = self.generate_module_routes(package_name)
            self.app.run(host=self.server_host, port=self.server_port)
            # TODO - FIX ME - Production WSGI server
#           if DEFAULT['debug-flag']:
#               self.app.run(host=self.server_host, port=self.server_port)
#           else:
#               subprocess.call(cmd)
        except Exception as e:
            log.error(e)

# CHECKERS

def check_module_installed(module_name: str) -> bool:
    log.debug('')
    return False if pkgutil.find_loader(module_name) is None else True

# CREATORS

def create_cli_arg_parser() -> argparse.ArgumentParser:
    log.debug('')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--start', action='store_true', help='Start web server.\n'
    )
    parser.add_argument(
        '-c', '--config-file', dest='config_file', type=str,
        help='Path to the Module Runner JSON configuration file.\n'
    )
    parser.add_argument(
        '-m', '--modules-file', dest='modules_file', type=str,
        help='Path to JSON file that contains the Strategy Module names.\n'
    )
    return parser

# CONVERTORS

def json2dict(file_path):
    if not file_path or not os.path.exists(file_path):
        log.warning('File not found! ({})'.format(file_path))
        return {}
    with open(file_path, 'r') as fl:
        converted = json.load(fl)
    log.debug('Converted JSON: ({})'.format(converted))
    return converted

# PARSERS

#@pysnooper.snoop()
def parse_cli_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    log.debug('')
    return parser.parse_args()

# GENERAL

def import_package(package_name: str):
    log.debug('')
    pkg = importlib.import_module(package_name)
    return pkg

# LOADERS

#@pysnooper.snoop()
def load_module(module: str, version: str) -> list:
    log.debug('')
    check = check_module_installed(module)
    if check:
        return True
    install = install_package(module, version)
    if not install:
        failures += 1
        log.error(f'Failed  to install dependency module! ({module} v{version})')
        return False
    return True

#@pysnooper.snoop()
def reload_config(file_path: str) -> dict:
    global DEFAULT
    global ENV
    if not os.path.exists(file_path):
        log.warning(f'Config file not found! ({file_path})')
        return None, None
    conf = Config(file_path)
    DEFAULT = DEFAULT if not conf.DEFAULT else conf.DEFAULT
    ENV = ENV if not conf.ENV else conf.ENV
    DEFAULT.update({var: os.environ.get(ENV[var]) for var in ENV})
    return DEFAULT, ENV

# INSTALLERS

#@pysnooper.snoop()
def install_package(package: str, version: str) -> bool:
    log.debug('')
    pkg_label = str(package) if not version else f'{package}=={version}'
    install = pip.main(['install', pkg_label])
    return True if install else False

# INIT

#@pysnooper.snoop()
def init(environ=None, start_response=None) -> int:
    global DEFAULT
    global ENV
    log.debug('')
    parser = create_cli_arg_parser()
    args = parse_cli_args(parser)
    if args.config_file:
        DEFAULT, ENV = reload_config(args.config_file)
    if args.start:
        pkg_load = load_module(DEFAULT['module-name'], DEFAULT['module-version'])
        if not pkg_load:
            log.warning(
                'No package/modules specified! Nothing to load, nothing to run.'
            )
            return 1
        runner = ModuleRunner(
            DEFAULT['module-name'], debug_mode=DEFAULT['debug-flag'],
            host=DEFAULT['host'], port=DEFAULT['port']
        )
        runner.start_server(DEFAULT['module-name'])
    return 0

# MISCELLANEOUS

if __name__ == '__main__':
    reload_config(DEFAULT['conf-file'])
    init()


# CODE DUMP

