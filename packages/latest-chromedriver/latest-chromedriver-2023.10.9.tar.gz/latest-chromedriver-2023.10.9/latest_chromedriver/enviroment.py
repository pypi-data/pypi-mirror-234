"""Usefull tools to set the enviroment"""
import os
import tempfile
from functools import lru_cache

import cpuinfo
from logzero import logger

from . import download_driver


@lru_cache(maxsize=1)
def get_cpu_arch():
    """Try to guess what cpu architecture we are running on"""
    manufacturer = cpuinfo.get_cpu_info().get('brand_raw')
    arch = 'arm' if 'm1' in manufacturer.lower() else 'x86_64'
    return arch


def is_fs_case_sensitive():
    """Is the filesystem case sensitive"""
    if not hasattr(is_fs_case_sensitive, 'case_sensitive'):
        with tempfile.NamedTemporaryFile(prefix='TmP') as tmp_file:
            setattr(is_fs_case_sensitive,
                    'case_sensitive',
                    not os.path.exists(tmp_file.name.casefold()))
    return is_fs_case_sensitive.case_sensitive


def _clean_and_add_env_path(add_path):
    # Clean the already defined path
    # Remove multiple identincal entries
    cleaned_path = []
    abs_path = [os.path.abspath(x)
                for x in os.environ['PATH'].split(os.pathsep)]

    for c_path in abs_path:
        if c_path:
            if is_fs_case_sensitive():
                case_path = c_path
                checked_paths = cleaned_path
            else:
                case_path = c_path.casefold()
                checked_paths = [x.casefold() for x in cleaned_path]

            if case_path not in checked_paths:
                cleaned_path.append(c_path)

    # Add the new path in the start of the enviroment $PATH
    if add_path:
        add_path = os.path.abspath(add_path)
        if is_fs_case_sensitive():
            add_path_case = add_path
        else:
            add_path_case = add_path.casefold()
        for c_path in cleaned_path[:]:
            if is_fs_case_sensitive():
                case_path = c_path
            else:
                case_path = c_path.casefold()

            if add_path_case == case_path:
                cleaned_path.remove(c_path)

        cleaned_path.insert(0, add_path)

    os.environ['PATH'] = os.pathsep.join(cleaned_path)


def safely_set_chromedriver_path(**kwargs):
    """Manipulate the enviroment PATH to include the chromedriver folder"""
    chromedriver_path = download_driver.download_only_if_needed(chrome_path=kwargs.get(
        'chrome_path'), chromedriver_folder=kwargs.get('chromedriver_folder'))
    if chromedriver_path:
        logger.debug("Adding %s to PATH", chromedriver_path)
        _clean_and_add_env_path(chromedriver_path)
