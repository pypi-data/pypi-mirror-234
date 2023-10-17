import argparse
import glob
import json
import logging
import multiprocessing
import os
import pathlib
import platform
import shutil
from argparse import Namespace
from logging.handlers import RotatingFileHandler
from stat import S_IWUSR, S_IREAD

from jsonschema import ValidationError, validate
import jsonpickle
import psutil as psutil
import sys
from fernet import Fernet, InvalidToken
from sys import exit
import inspect


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Framework(metaclass=Singleton):
    """Class Object Framework
    Base setting for the whole framework"""
    __instance = None

    def __init__(self, module):
        self.module = module
        sys.tracebacklimit = 0
        try:
            Framework.__instance = self
            self.file_dir = self.set_file_dir()
            self.config_framework = self.set_config_framework()
            self.log = self.set_logger(self.module)
            self.log.info('======================= F R A M E W O R K ===========================')
            self.args = self.set_arguments()
            self.config_framework['platform'] = self.set_host_config()
            if self.args.debug:
                self.save_status_to_file(status_object=self.config_framework, status_type='framework')
            self.config_framework['returnCodes'] = self.set_return_codes()
            self.config_framework['docker']['password'] = self.set_docker_password()
            self.log.info('_______________________ F R A M E W O R K ___________________________')
        except Exception as e:
            self.log.error('Failure to load the Framework data - %s', repr(e))
            raise

    @classmethod
    def get_framework_obj(cls):
        if Framework.__instance:
            return Framework.__instance
        return Framework(os.path.basename(sys.modules['__main__'].__file__).rsplit(".", 1)[0])

    def get_file_dir(self):
        if hasattr(self, "file_dir") and (self.file_dir is not None):
            return self.file_dir
        else:
            return None

    def get_internal_encryption_key(self):
        if hasattr(self, "config_framework") and self.config_framework.get('encryptionKeyFile'):
            return self.config_framework.get('encryptionKeyFile')
        else:
            return '/encryption.key'

    def get_config_framework(self):
        if hasattr(self, "config_framework"):
            return self.config_framework
        else:
            return None

    def get_logger(self):
        if hasattr(self, "log"):
            return self.log
        else:
            return None

    def get_arguments(self):
        if hasattr(self, "args"):
            return self.args
        else:
            return None

    def get_framework_license_check(self):
        if self.config_framework['controller'].get('licenseCheck') is not None:
            return self.config_framework['controller']['licenseCheck']
        else:
            return None

    def get_volumes(self):
        if self.config_framework.get('volumes') is not None:
            return self.config_framework['volumes']
        else:
            return None

    def get_network_mode(self):
        return self.config_framework['controller'].get('networkMode', None)

    def get_sequence(self):
        if self.config_framework['controller'].get('sequence') is not None:
            return self.config_framework['controller']['sequence']
        else:
            return None

    def get_product_dependencies(self):
        if self.config_framework.get('dependencies') is not None:
            return self.config_framework['dependencies']
        else:
            return None

    def get_version(self):
        if self.config_framework.get('version') is not None:
            return self.config_framework['version']
        else:
            return None

    @staticmethod
    def set_file_dir() -> str:
        """set the filename - prefix for testing purposes to the local IDE or Container filesystem
        in:  - None
        out: - str file and path"""
        tmp_file_dir = "" if "/dist/" in os.path.dirname(os.path.abspath(__file__)) else \
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return tmp_file_dir

    def set_general_json(self, file_name: str) -> bool:
        """ set the general.json/ general.yaml file to be used
        """
        self.log.debug('Starting to replace {0} with {1}'.format('general.json / general.yaml', file_name))
        general = pathlib.Path(self.file_dir + os.path.join('/json/', file_name))
        if file_name.endswith('.json'):
            new_general = pathlib.Path(self.file_dir + '/json/general.json')
        else:
            new_general = pathlib.Path(self.file_dir + '/json/general.yaml')
        self.log.debug('Checking if filename {} exists'.format(general))
        if general.exists():
            try:
                shutil.copy(general, new_general)
                self.log.debug('Successfully replaced {0} with {1}'.format('general.json / general.yaml', file_name))
                return True
            except PermissionError:
                os.chown(general, 1999, 1999)
                os.chmod(general, S_IWUSR | S_IREAD)
                self.set_general_json(file_name)
            except Exception:
                raise
        else:
            self.log.error('Please check the file: {0} mentioned as alternative general.json / general.yaml'
                           ' file.'.format(file_name))
            return False

    def set_host_config(self) -> dict:
        """loads infrastructure data from the docker host"""
        self.log.debug('Starting to load the local host platform data')
        try:
            tmp_platform = {'os': platform.platform(aliased=True, terse=True), 'arch': platform.machine(),
                            'node': platform.node(), 'cpu': platform.processor(),
                            'cpuCount': multiprocessing.cpu_count(),
                            'memory': psutil.virtual_memory()}
            self.log.debug('the following settings: ' + platform.platform(aliased=True, terse=True) +
                           ' ' + platform.machine() +
                           ' ' + str(multiprocessing.cpu_count()) +
                           ' ' + str(psutil.virtual_memory()))
            self.log.info("Successfully loaded the local host platform data, 0")
            return tmp_platform
        except Exception:
            self.log.error('Failure loading the local host platform data')
            raise

    def set_logger(self, module: str) -> logging.Logger:
        """setting the logger for console, info and debug (--debug)

        uses the settings from config_framework"""
        logger = logging.getLogger(module)
        formatter_i = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        formatter_d = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(threadName)s - %(module)s - %(message)s')
        try:
            for handler in self.config_framework['log']['loggers']:
                if handler['name'] == 'console':
                    handler_class = getattr(logging, handler['class'])
                    instance = handler_class(sys.stdout)
                    formatter = formatter_i
                    if '--debug' in sys.argv:
                        handler['level'] = 'DEBUG'
                        formatter = formatter_d
                elif handler['name'] == 'info':
                    handler_class = getattr(logging, handler['class'])
                    instance = handler_class(self.file_dir + '/logs/' + self.module + '-info.log', encoding='utf-8')
                    formatter = formatter_i
                else:
                    # if '--debug' not in sys.argv:
                    #     continue
                    handler_class = RotatingFileHandler(self.file_dir + '/logs/' + self.module + '-debug.log',
                                                        maxBytes=200000, backupCount=10, encoding='utf-8')
                    instance = handler_class
                    formatter = formatter_d
                instance.setFormatter(formatter)
                instance.setLevel(handler['level'])
                logger.addHandler(instance)
            logger.setLevel(logging.DEBUG)
            return logger
        except Exception as sl:
            logger.error('Failure setting up the logger factory: {}'.format(repr(sl)))
            raise

    def set_debug_settings(self) -> logging.Logger:
        """sets the log level to debug if --debug"""
        self.log.setLevel(logging.DEBUG)
        return self.log

    def set_log_prune(self) -> bool:
        """prunes all logfiles if selected (--prune)

        uses the glob function to delete path content"""
        if not self.module == 'controller':
            return False
        self.log.info('Starting to clean the log path')
        files = glob.glob(self.get_file_dir() + '/logs/*.log', recursive=True)
        for f in files:
            try:
                os.remove(f)
                self.log.debug("Deleted by prune command: {}".format(f))
            except Exception as e:
                self.log.warning("Logs cannot be removed - {} - {}, 1".format(e.__class__, e))
                pass
        self.log.info('Successfully cleaned the log path, 0')
        return True

    # Validates the schema if controller and not --test
    def run_schema_validation(self, config: dict, schema) -> bool:
        if self.args.test or self.module != 'controller':
            return True
        if not os.path.isfile(self.get_file_dir() + '/python/' + schema):
            self.log.error('Failure reading the json schema file')
            raise Exception
        try:
            self.log.debug('Starting to validate the schema')
            with open(self.get_file_dir() + '/python/' + schema) as schema:
                schema = json.load(schema)
            validate(config, schema)
            return True
        except ValidationError:
            self.log.error('Failure validating the schema')
            raise
        except Exception:
            raise

    def set_docker_password(self) -> str:
        """set the docker repository password to the config_docker dict and decrypts it

        Decryption needs encryptionFile to be defined in config_docker/encryptionKeyFile.

        While the docker url is loaded from General class,
        the docker password for docker.io is loaded from here"""
        self.log.debug('Starting to set the docker password')
        try:
            if self.module != 'controller':
                return ''
            docker_data = self.config_framework['docker']
            self.log.debug('Checking config_docker: {}'.format(json.dumps(docker_data)))
            self.log.debug('Actual docker password is {}'.format(self.config_framework['docker']['password']))
            tmp_password = self.get_decrypted_pwd(env_file=self.get_internal_encryption_key(),
                                                  pwd=self.config_framework['docker']['password'],
                                                  context="docker")
            self.log.debug('Docker password is not None')
            self.log.info('Successfully added the docker password, 0')
            return tmp_password
        except Exception:
            self.log.error('Failure to set the docker password')
            raise

    def set_arguments(self) -> Namespace:
        """sets the args Namespace for argument usage and help

        Triggers divers functions if args are submitted"""
        self.log.info('Starting to parse the command line')
        args_description = 'Welcome to ammp-xe\n\n' \
                           'This is the smartdeployX framework auto deployment\n' \
                           'If you prepared the general,json file and saved it in \n' \
                           'a directory you should be able to deploy the products\n' \
                           'automatically.\n'
        parser = argparse.ArgumentParser(prog=self.module, description=args_description)
        parser.add_argument("-action", action='store',
                            help="choose 'deploy' to activate the smartdeploy framework \
                           execution including the check components. You can also choose \
                           rerun. In this case the controller will try to rerun the action. \
                           If not add --nocheck to run it in a productive system. If you choose \
                           load the images will be loaded for further storage")
        parser.add_argument("--check",
                            help="if you want to run the check container stand-alone \
                           without touching the target systems", required=False,
                            action="store_true", default=False)
        parser.add_argument("--nocheck",
                            help="select this if it already checked the targets",
                            required=False, action="store_true", default=False)
        parser.add_argument("--debug", help="adds debug messages", required=False,
                            action="store_true", default=False)
        parser.add_argument("-encrypt", action='store',
                            help="if you want to encrypt your password use this switch and add your cleartext password",
                            required=False, default=False)
        # internal for testing log removal
        parser.add_argument("--test", action='store_true', help=argparse.SUPPRESS,
                            required=False, default=False)
        # internal for testing json file replacement
        parser.add_argument("--json", action='store', help=argparse.SUPPRESS,
                            required=False)
        parser.add_argument("--prune", action='store_true', help=argparse.SUPPRESS,
                            required=False, default=False)
        parser.add_argument("-secret_id", action="store",
                            help='if you want to generate the initial token add your secret id here')
        if not self.module == 'controller':
            parser.add_argument("product", default='test', action="store", help=argparse.SUPPRESS)
        try:
            args: Namespace = parser.parse_args()
        except SystemExit:
            self.log.error("Failure, Invalid Arguments, 1")
            raise
        if args.encrypt:
            encrypted_pwd = self.set_encrypted_password(
                encrypt_file=self.get_internal_encryption_key(),
                pass_wd=args.encrypt)
            # TODO: SHOULD GET General encryption key here ????????????????????????????????????????????????????????????????????
            print('This is your encrypted password: ' + encrypted_pwd)
            exit(0)
        if args.test is True:
            self.log.warning("Validation sequence switched off, json files not checked")
        if args.json is not None:
            self.log.warning('general.json replacement selected. Switching json files to {0}'.format(args.json))
            result = self.set_general_json(args.json)
            self.log.debug('set args.json to {}'.format(result))
        if args.prune is not False and args.test is False:
            self.log.warning('log prune selected')
            result = self.set_log_prune()
            self.log.debug('set args.prune to {}'.format(result))
        if args.debug:
            self.log.warning("Log level set to debug")
            self.log.setLevel(logging.DEBUG)
        if args.action == 'rerun' and args.check:
            self.log.warning("rerun cannot be combined with check")
            raise SystemExit
        if args.check and args.nocheck:
            self.log.warning("check cannot be combined with nocheck")
            raise SystemExit
        if args.action == 'load':
            self.log.debug("Push images to artifactory")

        self.log.info('Successfully parsed the command line - {}, 0'.format(args))
        print(args)
        return args

    def save_status_to_file(self, status_object: dict, status_type: str) -> bool:
        """Saves a status information (dict) to a given file

        status_type = name of the file"""
        self.log.info("Starting to save current setting for " + status_type)
        tmp_file = self.file_dir + '/logs/' + status_type + '.status'
        try:
            status = jsonpickle.encode(status_object, indent=2)
            self.log.debug('Saving the status for {}: {}'.format(tmp_file, json.dumps(status)))
            with open(tmp_file, 'w') as outfile:
                outfile.write(status)
            self.log.info('Successfully saved the status to {}, 0'.format(tmp_file))
            return True
        except PermissionError:
            os.chown(tmp_file, 1999, 1999)
            os.chmod(tmp_file, S_IWUSR | S_IREAD)
            self.save_status_to_file(status_object, status_type)
        except OSError:
            self.log.error('Could not save file to {0}'.format(tmp_file))
            raise

    # saves the defined status of a container or image to a file in /logs
    def load_status_from_file(self, status_type='container or image'):
        try:
            with open(self.file_dir + self.config_framework['controller']['status'] + '/' + status_type + '.status',
                      'r') as outfile:
                status_file = json.load(outfile)
            self.log.info('Successfully loaded the status for ' + status_type + '.status')
            return status_file
        except FileNotFoundError:
            self.log.warning('Cannot load status from file, does not exist')
            return None

    # decrypts a password (general meaning)
    # Input: encryption file and password
    def get_decrypted_pwd(self, env_file, pwd: str, context: str) -> str:
        if env_file is None or (pwd is None or pwd == ''):
            self.log.warning(
                'Cannot find encryptionKeyFile or password is empty ' + inspect.currentframe().f_back.f_code.co_name)
            return ""
        else:
            file = open(env_file, "rb")
            key = file.read()
            f = Fernet(key)
            password = pwd.encode()
            try:
                dec = f.decrypt(password).decode()
                return dec
            except InvalidToken:
                err_msg = 'Something is wrong with the password for ' + context + ', cannot be decrypted:' + \
                          inspect.currentframe().f_back.f_code.co_name
                self.log.error(err_msg)
                raise RuntimeError(err_msg)

    @staticmethod
    def set_encrypted_password(encrypt_file, pass_wd: str) -> str:
        try:
            key = open(encrypt_file, "rb").read()
            encoded_message = pass_wd.encode()
            f = Fernet(key)
            encrypted_message = f.encrypt(encoded_message)
            return encrypted_message.decode("utf-8")
        except InvalidToken:
            print('Warning: Cannot encrypt your password')
            raise

    # loads the framework configuration
    @staticmethod
    def set_config_framework() -> dict:
        tmp_framework = {
            "version": "2023.05", "lastChangeDate": "2022-07-16", "lastChangeBy": "Madhav",
            'vault': {
                "HashiCorp": {
                    "useInternalVault": False, "vaultType": "dev", "url": "",
                    "role_id": "",
                    "base_path": ""},
                "NetIq": {
                    "useInternalVault": False, "vaultType": "dev", "url": "",
                    "role_id": "",
                    "base_path": ""}
            },
            'docker': {
                "useDocker": True,
                "useLocalImages": True,
                "registry": "https://index.docker.io/v1/",
                "useTlsVerify": False,
                "serverCA": "",
                "clientCert": "",
                "clientKey": "",
                "username": "platformxapi",
                "password": "gAAAAABgDv49o0yhzGksioBwWjyf_MQd-Em2RGKMFdHBOd5zsqB6MubeUl1xZW1XxTttk_"
                            "UczgHxkrdKYW7bWUfUjMLZxSGfcQ==",
                "prune": False,
                "minCpuCount": 16,
                "minMemory": 16000},
            "artifactory": {
                "useArtifactory": True,
                "hostname": "svsartifactory.swinfra.net",
                "repoUrl": "https://svsartifactory.swinfra.net:443/artifactory",
                "userName": "vonderhe",
                "password": "Harley2019!",
            },
            'volumes': {
                "/logs": {"bind": "/logs", "mode": "rw", "owner": 1999},
                "/pki": {"bind": "/pki", "mode": "rw", "owner": 1999},
                "/json": {"bind": "/json", "mode": "rw", "owner": 1999}
            },
            'controller': {
                "generalFile": "/json/general.json",
                "licenseCheck": True,
                "validation": True,
                "status": "/logs",
                "networkMode": "bridge",
                "sequence": [
                    {"name": "mfpsna/security", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": {"8200/tcp: 8200"}},
                    {"name": "mfpsna/infra", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/check", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/transport", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/prepare", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/inject", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/persist", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/deploy", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/integrate", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/content", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]},
                    {"name": "mfpsna/test", "tag": "2023.05",
                     "persistent": False,
                     "runOnce": False,
                     "ports": ["4000/tcp"]}
                ]
            },
            "dependencies":  {
                "obmha": ["pghapool"],
                "obm": ["pghapool"],
                "oa": ["obm", "obmha"],
                "dfp": ["cms"],
                "uda": ["dfp"],
                "sis": ["obm", "obmha", "oa", "dfp"],
                "ooras": ["oo"],
                "haproxy": ["pgha"],
                "cms": ["sma"],
                "na": ["pghapool", "pgha"],
                "ispiqa": ["nnmi"],
                "ispitrafficbase": ["nnmi", "ispiqa"],
                "ispimpls": ["nnmi", "ispiqa", "ispitrafficbase"],
                "ispimulticast": ["nnmi", "ispiqa", "ispitrafficbase", "ispimpls"],
                "ispiipt": ["nnmi", "ispiqa", "ispitrafficbase", "ispimpls", "ispimulticast"],
                "ispitrafficmasterleaf": ["nnmi", "ispitrafficbase"],
                "nnmi": ["pghapool", "pgha"],
                "cdf": ["pghapool", "pgha"],
                "opticdl": ["cdf", "pghapool", "pgha"],
                "identityengine": ["docker"],
                "imanager": ["docker", "identityengine"]

            },
            "packages": [
                {"product": "obm", "title": "Operations Bridge Manager Single Server"},
                {"product": "obmha", "title": "Operations Bridge Manager High Available, 2 servers"},
                {"product": "obmprimary", "title": "Operations Bridge Manager, primary"},
                {"product": "obmsecondary", "title": "Operations Bridge Manager, secondary"},
                {"product": "sis", "title": "SiteScope Monitoring Server"},
                {"product": "dfp", "title": "UCMDB Data Flow Probe"},
                {"product": "ooras", "title": "Operation Orchestration Remote Access Server"},
                {"product": "uda", "title": "Universal Discovery Agent"},
                {"product": "oa", "title": "Operations Agent"},
                {"product": "sma", "title": "Service Management Automation (AWS)"},
                {"product": "cms", "title": "Configuration Management System (AWS)"},
                {"product": "pgha", "title": "Postgres HA Database-12"},
                {"product": "haproxy", "title": "Layer 7 Load Balancer"},
                {"product": "nnmi", "title": "Network Node Manager in Application Failover"},
                {"product": "na", "title": "Network Automation Standalone or HS topology"},
                {"product": "ispiqa", "title": "iSPI Performance for Quality Assurance"},
                {"product": "ispimulticast", "title": "iSPI for IP Multicast"},
                {"product": "ispiipt", "title": "iSPI for IP Telephony "},
                {"product": "ispitrafficbase", "title": "iSPI Performance for Traffic"},
                {"product": "ispimpls", "title": "iSPI for MPLS"},
                {"product": "ispitrafficmasterleaf", "title": "iSPI Performance for Traffic Master and Leaf Collectors"},
                {"product": "identityengine", "title": "Identity Engine for Identity Manager"},
                {"product": "imanager", "title": "iManager for Identity Manager"}
            ],
            "ignoreFailedServers": ["oa","co"],
            "actions": ["install", "update", "uninstall"],
            "encryptionKeyFile": "/encryption.key",
            'log': {
                "useLogger": True, "dockerPrune": False, "debug": False, "logPrune": False,
                "logPruned": "",
                "loggers": [
                    {"name": "console", "class": "StreamHandler", "file": "", "level": "INFO"},
                    {"name": "info", "class": "FileHandler",
                     "file": "/logs/controller.log", "level": "INFO"},
                    {"name": "debug", "class": "RotatingFileHandler",
                     "file": "/logs/debug.log", "max": 50000, "level": "DEBUG"}
                ]},
            "utilities": {
                "utilityCheck": True,
                "linux": {
                    "nslookup": "sudo which nslookup",
                    "stat": "sudo stat --help",
                    "mount": "sudo mount --help",
                    "unmount": "sudo umount --help",
                    "rpm": "sudo rpm --help",
                    "nproc-cpu-count": "sudo nproc --help",
                    "yum": "sudo yum --help",
                    "systemd": "sudo systemctl status | grep /systemd",
                    "awk": "sudo awk --help",
                    "procps": "sudo free --help",
                    "filesystem": "sudo df --help"
                },
                "windows": {
                    "nslookup": "nslookup help",
                    "PSManagement": "Get-Service /?",
                    "gpresult": "gpresult /?",
                    "Test-NetConnection": "(tnc).PingSucceeded",
                    "net user": "net user $env:UserName",
                    "ipconfig": "ipconfig",
                    "systeminfo": "systeminfo /?",
                    "icacls": "icacls /?",
                    "timesync": "w32tm /?",
                    "ping": "ping /?"
                }
            }
        }
        return tmp_framework

    @staticmethod
    def set_return_codes():
        return_codes = {
            "1": "General Failure",
            "12": "cannot load general or framework.json for initialization of the general class",
            "11": "File cannot be found",
            "51": "Json file wrongly configured",
            "52": "Container could not be initialized",
            "53": "failure to download images from repository",
            "54": "Failure in validating the existence and rights for the mounted volumes",
            "55": "Failure to connect to the docker server:",
            "56": "Failure to load the following image from docker server:",
            "57": "Failure to connect to the external docker server:",
            "61": "Failure to connect to ITSM server:",
            "62": "Failure to connect during timeout to:",
            "63": "Failure with request, cannot  be accepted by the server:",
            "71": "Failure loading the configuration files for ITSM",
            "72": "Failure sending an incident request to:",
            "73": "Failure during the communication to the ITSM system",
            "75": "Failure sending an change request to:",
            "76": "Failure sending a relationship request to:",
            "77": "Failure retrieving the license verification from portal:"
        }
        return return_codes
