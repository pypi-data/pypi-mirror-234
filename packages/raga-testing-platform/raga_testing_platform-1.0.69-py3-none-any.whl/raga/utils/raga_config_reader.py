import os
import configparser
from raga import RAGA_CONFIG_FILE
from raga.constants import AWS_RAGA_SECRET_KEY, AWS_RAGA_ACCESS_KEY, AWS_RAGA_ROLE_ARN
import sys
import platform

DEFAULT_CONFIG_VALUES = {
    "api_host": "https://example.com",
    "raga_access_key_id": "your-access-key",
    "raga_secret_access_key": "your-secret-key"
}

def get_config_file_path(path):
    if platform.system() == 'Linux':
        # Path for Linux machine
        return os.path.expanduser(os.path.join("~", path))
    elif platform.system() == 'Darwin':
        # Path for macOS machine (if required, add a different path for macOS)
        return os.path.expanduser(os.path.join("~", path))
    elif platform.system() == 'Windows':
        # Path for Windows machine (if required, add a different path for Windows)
        return os.path.expanduser(os.path.join("~", path))
    else:
        # Default path for other platforms (such as Google Colab)
        return '/content/MyDrive.raga/config'

def get_machine_platform():
        system = platform.system().lower()

        if system == "darwin":
            mac_version = "11_0" if platform.release() >= "20.0.0" else "10_9"
            arch = "arm64" if platform.machine() == "arm64" else "x86_64"
            platform_name = f"macosx_{mac_version}_{arch}"
        elif system == "linux":
            platform_name = (
                "linux_x86_64"  # if platform.architecture()[0] == '64bit' else 'linux_i686'
            )
        elif system == 'windows':
            platform_name = 'win_amd64' if platform.architecture()[0] == '64bit' else 'win32'
        else:
            raise RuntimeError(f"Unsupported platform: {system}")
        return platform_name
        
def get_python_version():
    version = sys.version.split()[0]
    major, minor, _ = map(int, version.split("."))
    return str(f"cp{major}{minor}")


def format_python_versions(version_str):
    versions = version_str.split(',')
    formatted_versions = []

    for version in versions:
        parts = version.split('.')
        major = int(parts[0])
        minor = int(parts[1])

        version = f"{major}.{minor}"
        formatted_versions.append(float(version))

    return formatted_versions


def read_raga_config():
    config_file_path = get_config_file_path(RAGA_CONFIG_FILE)

    if not os.path.isfile(config_file_path):
        create_default_config(config_file_path)
        print(f"A default config file has been created. Please update the credentials in the config file. You can update using this command `sudo vim {config_file_path}`")
        sys.exit(0)

    config = configparser.ConfigParser()
    try:
        config.read(config_file_path)
    except configparser.Error as e:
        raise ValueError(f"Invalid config file format: {str(e)}")

    validate_default_section(config)

    config_data = {}
    for section_name in config.sections():
        config_data[section_name] = dict(config.items(section_name))

    return config_data

def create_default_config(config_file_path):
    config = configparser.ConfigParser()
    config.add_section("default")

    for option, value in DEFAULT_CONFIG_VALUES.items():
        config.set("default", option, value)

    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

    with open(config_file_path, "w") as config_file:
        config.write(config_file)

def validate_default_section(config):
    default_section = config["default"]

    for option, default_value in DEFAULT_CONFIG_VALUES.items():
        if option not in default_section or default_section[option] == default_value:
            raise ValueError(f"Please update the value of '{option}' in the [default] section of the config file.")

def get_config_value(config_data, section, option):
    if section in config_data:
        section_data = config_data[section]
        if option in section_data:
            return section_data[option]
        else:
            if option == AWS_RAGA_SECRET_KEY or option == AWS_RAGA_ACCESS_KEY or option == AWS_RAGA_ROLE_ARN:
                return ""
            raise KeyError(f"Option '{option}' not found in section '{section}'.")
    else:
        raise KeyError(f"Section '{section}' not found in config data.")
