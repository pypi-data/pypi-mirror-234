import os.path
from enum import Enum
from pingsafe_cli.version import build_type

CONFIG_FILE_NAME = "config.json"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG_ENABLED = 0
BASELINE_FILE = ".baseline"
PACKAGE_NAME = "pingsafe_cli"
DEFAULT_TIMEOUT = 10
BINARY_LIST = ["bin_secret_detector", "bin_eval_rego", "bin_vulnerability_scanner"]
SENTRY_TAGS = ["org_id", "project_id"]

MAIN_PIP_COMMAND = ["pip3", "install", "--upgrade", PACKAGE_NAME]
TEST_PIP_COMMAND = ["pip3", "install", "-i", "https://test.pypi.org/simple/", "--upgrade",
                    PACKAGE_NAME, "--extra-index-url", "https://pypi.org/simple"]

MAIN_PYPI_URL = f'https://pypi.org/pypi/{PACKAGE_NAME}/json'
TEST_PYPI_URL = f'https://test.pypi.org/pypi/{PACKAGE_NAME}/json'

PIP_COMMAND = MAIN_PIP_COMMAND if build_type == "pypi" else TEST_PIP_COMMAND
PYPI_URL = MAIN_PYPI_URL if build_type == "pypi" else TEST_PYPI_URL

APP_URL = "https://app.pingsafe.com"
APP2_URL = "https://app2.pingsafe.com"
LOCAL_URL = "http://localhost:8080"

GET_PRE_SIGNED_URL = "/apis/v1/cli/setup"
GET_CONFIG_DATA_URL = "/apis/v1/cli/config"
DOWNLOAD_CACHE_URL = "/apis/v1/cli/iac/cache"

DEFAULT_PINGSAFE_DIR = ".pingsafe"
BINARY_DIR = "bin"
PINGSAFE_LOCAL_CONFIG_PATH = os.path.join(DEFAULT_PINGSAFE_DIR, "local_config.json")
SUPPORTED_FRAMEWORKS = ["TERRAFORM", "TERRAFORM_PLAN", "CLOUDFORMATION", "KUBERNETES", "HELM"]

PUBLISH_ISSUES_API = "/apis/v1/cli/publish/issues"
SUPPORTED_GIT_PROVIDERS = ["GITHUB", "GITLAB", "BITBUCKET", "AZURE"]


PINGSAFE_JSON = "pingsafe-json"
DEFECT_DOJO_GENERIC_FORMAT = "defect-dojo-generic-format"

SEVERITIES = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}


class MainSubParser(str, Enum):
    SCAN = "scan"
    CONFIG = "config"


class CodeTypeSubParser(str, Enum):
    IAC = "iac"
    SECRET = "secret"
    VULN = "vuln"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class IacFramework(str, Enum):
    ALL = "all"
    TERRAFORM = "terraform"
    TERRAFORM_PLAN = "terraform-plan"
    CLOUDFORMATION = "cloudformation"
    KUBERNETES = "kubernetes"
    HELM = "helm"


class IacConfigData(str, Enum):
    LAST_REFRESHED_AT = "last_refreshed_at"


class OutputFormat(str, Enum):
    JSON = "JSON"
    CSV = "CSV"


class MissingConfig(Exception):
    pass


class HttpConnectionError(Exception):
    pass


class RequestTimeout(Exception):
    pass


class MissingRequiredFlags(Exception):
    pass


class PlatformNotSupported(Exception):
    pass


class MissingDependencies(Exception):
    pass


class InvalidGraphConnection(Exception):
    pass


class UnauthorizedUser(Exception):
    pass

class InvalidInput(Exception):
    pass


class DownloadException(Exception):
    def __init__(self, message, url="", filename=""):
        super().__init__(message)
        self.url = url
        self.filename = filename


class LogColors(str, Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    OKORANGE = '\033[38;5;208m'


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


GLOBAL_EPILOG = \
"""
Examples:
    Configure PingSafe CLI:
        pingsafe-cli config --help

    Scan using PingSafe CLI:
        pingsafe-cli scan --help

    Debugging command:
        pingsafe-cli --debug [sub-command]

    Get result in quiet mode:
        pingsafe-cli -q/--quiet scan [sub-command]

    Get result in verbose mode:
        pingsafe-cli --verbose scan [sub-command]

    Get result on a file:
        pingsafe-cli -output-file <path/to/file.ext> --output-format <JSON/CSV> scan [sub-command]

Use "pingsafe-cli [command] --help" for more information about a command.
"""


SCAN_EPILOG = \
"""
Examples:
    IaC Scan:
        pingsafe-cli scan iac --help
        
    Secret Detection Scan:
        pingsafe-cli scan secret --help
        
    Vulnerability Scan & SBOM generator:
        pingsafe-cli scan vuln --help
"""



CONFIG_EPILOG = \
"""
Examples:
    Configure PingSafe CLI:
        pingsafe-cli config --api-token <PINGSAFE-API-TOKEN>

    Other flags while configuring:
            pingsafe-cli config --api-token <PINGSAFE-API-TOKEN> (mandatory)
                                --output-file <path/to/file.ext> (optional)
                                --output-format <JSON/CSV> (optional, default: JSON)
                                --workers-count <int> (optional, default: 5)
                                --on-crash-exit-code <int> (optional, default: 0)
"""


IAC_EPILOG = \
"""
Examples:
    List plugins:
        pingsafe-cli scan iac --list-plugins
        
    Scan a directory:
        pingsafe-cli scan iac -d <path/to/dir>
        
    Generate baseline:
        pingsafe-cli scan iac -d <path/to/dir> --generate-baseline (optional, default: false)
        
    Delete IaC cache:
        pingsafe-cli scan iac --invalidate-cache
    
    Other flags:
        pingsafe-cli scan iac -d <path/to/dir> (mandatory)
                              --frameworks <all/terraform/cloudformation/kubernetes/helm> (optional, default: all)
                              --include-ignored (optional, default: false)
                              --download-external-modules (optional, default: false)
                              --var-file <file/1 file/2 ... file/n> (optional)
                              
"""


SECRET_EPILOG = \
"""
Examples:
    List detectors:
        pingsafe-cli scan secret --list-detectors
    
    Scan a directory:
        pingsafe-cli scan secret -d <path/to/dir>
        
    Generate baseline:
        pingsafe-cli scan secret -d <path/to/dir> --generate-baseline --range <start_ref end_ref>
        
    Other flags:
        pingsafe-cli scan secret -d <path/to/dir> (mandatory)
                                 --disable-verification (optional, default: false)
                                 --mask-secret (optional, default: false)
                                 --include-ignored (optional, default: false)
                                 --verified-only (optional, default: false)
                                 --pre-commit (optional, default: false)
                                 --range <start_ref end_ref> (optional)
                                 --pull-request <src_branch dest_branch> (optional)
                                 --skip-paths <path/1 path/2 ... path/n> (optional)
                                 --excluded-detectors <DETECTOR_API_KEY_1 DETECTOR_API_KEY_2 ... DETECTOR_API_KEY_N> (optional)
"""


VULN_EPILOG = \
"""
Examples:
    Scan a directory:
        pingsafe-cli scan vuln -d <path/to/dir>
        
    Other flags:
        pingsafe-cli scan vuln --docker-image <image> (mandatory)
                               --fixed-only (optional, default: false)
                               --registry (default: index.docker.io)
                               --username (registry username)
                               --password (registry password)
"""