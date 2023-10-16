import os
from pathlib import Path
import requests
import json
import time

from logclshelper import LogClsHelper
from syshelper import SysHelper
from venvhelper import VenvHelper
from pytowhl import PyToWhl

class PyToPypi(PyToWhl):
    URL_PYPI = 'https://pypi.org'
    URL_TEST_PYPI = 'https://test.pypi.org'
    
class PyToPypi(PyToWhl):
    URL_PYPI = 'https://pypi.org'
    URL_TEST_PYPI = 'https://test.pypi.org'

    @classmethod
    def get_pkg_info_from_repo(cls, pkg_name, repo_url = PyToPypi.URL_TEST_PYPI):
        url = os.path.join(repo_url, 'pypi', pkg_name, 'json')
        resp = requests.get(url)
        js_resp = json.loads(resp.content)

        if('info' in js_resp):
            return js_resp

        return None 

    @classmethod
    def get_pkg_current_version_from_repo(cls, pkg_name, repo_url = PyToPypi.URL_TEST_PYPI):
        js_resp = cls.get_pkg_info_from_repo(pkg_name = pkg_name, repo_url = repo_url)
        return js_resp['info']['version'] if(js_resp is not None) else None

    @classmethod
    def get_pkg_version_to_build(cls, pkg_name, repo_url = PyToPypi.URL_TEST_PYPI, pkg_default_version = '0.0.0'):
        cls.logger().debug(f'#beg# get pkg version to build {pkg_name, repo_url, pkg_default_version}')
        
        current_version = cls.get_pkg_current_version_from_repo(pkg_name = pkg_name, repo_url = repo_url)   
        pkg_version_to_build = cls.increment_pkg_version(current_version) if current_version is not None else pkg_default_version

        cls.logger().debug(f'#end# get pkg version to build {pkg_name, repo_url, pkg_default_version, pkg_version_to_build}')
        
        return pkg_version_to_build

    @classmethod
    def upload_pkg_to_repo(cls, pkg_parent_dir = '.', repo_url = PyToPypi.URL_TEST_PYPI):
        cls.logger().debug(f'#beg# upload pkg to repo {pkg_parent_dir, repo_url}')
        
        path = os.path.join(pkg_parent_dir, 'dist/*.whl')
        
        if('test' in repo_url):
            cmd = f'twine upload --repository testpypi {path}'
        else:
            cmd = f'twine upload {path}'

        tmp_venv_name = os.path.basename(pkg_parent_dir) + '-' + str(id(cmd))      
        with VenvHelper.activate_venv_context(tmp_venv_name):
            cls.run_cmd('pip install twine')
            p = cls.run_cmd(cmd)

        cls.logger().debug(f'#end# upload pkg to repo {pkg_parent_dir, repo_url}')
        
        return p

    @classmethod
    def wait_for_repo_version_to_match_uploaded_version(cls, pkg_name, pkg_uploaded_version, repo_url = PyToPypi.URL_TEST_PYPI, seconds_timeout = 120):
        cls.logger().debug(f'#beg# wait for repo version to match uploaded version {pkg_name, pkg_uploaded_version, repo_url, seconds_timeout}')
        
        pkg_repo_version = cls.get_pkg_current_version_from_repo(pkg_name = pkg_name, repo_url = repo_url)
        
        matched = (pkg_repo_version == pkg_uploaded_version)
        seconds_elapsed = 0
        while((not matched) and (seconds_elapsed < seconds_timeout)):
            time.sleep(1)
            
            pkg_repo_version = cls.get_pkg_current_version_from_repo(pkg_name = pkg_name, repo_url = repo_url)
            
            matched = (pkg_repo_version == pkg_uploaded_version)
            seconds_elapsed += 1

            cls.logger().debug(f'waited 1s for repo version to match uploaded version {seconds_elapsed}/{seconds_timeout} {pkg_name, pkg_uploaded_version, pkg_repo_version}')

        cls.logger().debug(f'#end# wait for repo version to match uploaded version {pkg_name, pkg_uploaded_version, repo_url, seconds_timeout, pkg_repo_version}')
        
        return matched

    @classmethod
    def upload_pkg_to_repo_wait(cls, 
        pkg_name, 
        pkg_version_to_upload = None, 
        pkg_parent_dir = '.', 
        repo_url = PyToPypi.URL_TEST_PYPI, 
        seconds_timeout = 120
    ):
        cls.logger().debug(f'#beg# upload pkg to repo wait {pkg_name, pkg_version_to_upload, pkg_parent_dir, repo_url, seconds_timeout}')
        
        cls.upload_pkg_to_repo(pkg_parent_dir = pkg_parent_dir, repo_url = repo_url)

        if(pkg_version_to_upload is None):
            pkg_version_to_upload = cls.get_pkg_version_to_build(
                pkg_name = pkg_name, 
                repo_url = repo_url
            )
        
        matched = cls.wait_for_repo_version_to_match_uploaded_version(
            pkg_name = pkg_name, 
            pkg_uploaded_version = pkg_version_to_upload, 
            repo_url = repo_url, 
            seconds_timeout = seconds_timeout
        )

        cls.logger().debug(f'#end# upload pkg to repo wait {pkg_name, pkg_version_to_upload, pkg_parent_dir, repo_url, seconds_timeout, matched}')

        return matched

    @classmethod
    def convert_py_to_wheel_for_repo(cls, pkg_name, pkg_parent_dir = '.', repo_url = PyToPypi.URL_TEST_PYPI, required_modules = None, pkg_default_version = '0.0.0', pkg_version_to_build = None):
        cls.logger().debug(f'#beg# convert py to wheel for repo {pkg_name, pkg_parent_dir, repo_url, pkg_default_version, pkg_version_to_build}')

        if(pkg_version_to_build is None):
            pkg_version_to_build = cls.get_pkg_version_to_build(pkg_name = pkg_name, repo_url = repo_url, pkg_default_version = pkg_default_version)
        
        cls.convert_py_to_wheel(pkg_name = pkg_name, pkg_parent_dir = pkg_parent_dir, required_modules = required_modules, pkg_version_to_build = pkg_version_to_build)

        cls.logger().debug(f'#end# convert py to wheel for repo {pkg_name, pkg_parent_dir, repo_url, pkg_default_version, pkg_version_to_build}')

    @classmethod
    def convert_py_to_wheel_upload_to_repo_wait(cls, pkg_name, pkg_parent_dir = '.', repo_url = PyToPypi.URL_TEST_PYPI, required_modules = None, pkg_default_version = '0.0.0', seconds_timeout = 120):
        cls.logger().debug(f'#beg# convert py to wheel upload to repo wait {pkg_name, pkg_parent_dir, repo_url, pkg_default_version, seconds_timeout}')

        pkg_version_to_build = cls.get_pkg_version_to_build(pkg_name = pkg_name, repo_url = repo_url, pkg_default_version = pkg_default_version)
        
        cls.convert_py_to_wheel_for_repo(
            pkg_name = pkg_name, 
            pkg_parent_dir = pkg_parent_dir, 
            repo_url = repo_url, 
            required_modules = required_modules,
            pkg_default_version = pkg_default_version, 
            pkg_version_to_build = pkg_version_to_build
        )
        
        matched = cls.upload_pkg_to_repo_wait(
            pkg_name = pkg_name, 
            pkg_uploaded_version = pkg_version_to_build, 
            pkg_parent_dir = pkg_parent_dir, 
            repo_url = repo_url, 
            seconds_timeout = seconds_timeout
        )

        cls.logger().debug(f'#end# convert py to wheel upload to repo wait {pkg_name, pkg_parent_dir, repo_url, pkg_default_version, seconds_timeout, pkg_version_to_build, matched}')

        return matched





