from logclshelper import LogClsHelper
from syshelper import SysHelper
from venvhelper import VenvHelper
from ipytopy import IPyToPy
from pytowhl import PyToWhl
from pytopypi import PyToPypi

class CicdHelper(LogClsHelper):
    c_ipytopy = IPyToPy
    c_pytopypi = PyToPypi
    
    @classmethod
    def run_cmd(cls, cmd):
        return SysHelper.run_cmd(cmd)

    @classmethod
    def convert_nb_to_py(cls, nb_dir_path = '.', py_dir_path = '.'):
        cls.c_ipytopy.clear_py_dir_paths_format_convert_nb_files_to_py_files(nb_dir_path = nb_dir_path, py_dir_path = py_dir_path)

    @classmethod
    def convert_py_to_wheel(cls, 
        pkg_name, 
        pkg_parent_dir = '.', 
        repo_url = PyToPypi.URL_TEST_PYPI, 
        required_modules = None,
        pkg_default_version = '0.0.0', 
        pkg_version_to_build = None,
        
    ):
        if(repo_url is not None):
            cls.c_pytopypi.convert_py_to_wheel_for_repo(
                pkg_name = pkg_name, 
                pkg_parent_dir = pkg_parent_dir, 
                repo_url = repo_url,
                required_modules = required_modules,
                pkg_default_version = pkg_default_version,
                pkg_version_to_build = pkg_version_to_build
            )
        else:
            cls.c_ipytopy.convert_py_to_wheel(
                pkg_name = pkg_name, 
                pkg_parent_dir = pkg_parent_dir, 
                required_modules = required_modules,
                pkg_version_to_build = pkg_version_to_build
            )

    @classmethod
    def upload_wheel_to_repo(cls, 
        pkg_name, 
        pkg_parent_dir = '.', 
        repo_url = PyToPypi.URL_TEST_PYPI, 
        seconds_timeout = 120
    ):
        cls.c_pytopypi.upload_pkg_to_repo_wait(
            pkg_name = pkg_name, 
            pkg_version_to_upload = None, 
            pkg_parent_dir = pkg_parent_dir, 
            repo_url = repo_url, 
            seconds_timeout = seconds_timeout
        )

    @classmethod
    def install_pkg_as_editable(cls, pkg_parent_dir = '.'):
        cls.c_pytopypi.install_pkg_as_editable(pkg_parent_dir = pkg_parent_dir)
        
    @classmethod
    def nb_to_py_to_wheel_install(cls, pkg_name, pkg_parent_dir = '.', nb_dir_path = '.', py_dir_path = '.', repo_url = PyToPypi.URL_TEST_PYPI, required_modules = None):
        cls.logger().debug(f'#beg# nb to py to wheel install {pkg_name, pkg_parent_dir, nb_dir_path, py_dir_path, repo_url, required_modules}')
        
        cls.convert_nb_to_py(nb_dir_path = nb_dir_path, py_dir_path = py_dir_path)
        
        cls.convert_py_to_wheel(
            pkg_name = pkg_name, 
            pkg_parent_dir = py_dir_path, 
            repo_url = repo_url,
            required_modules = required_modules
        )

        cls.install_pkg_as_editable(pkg_parent_dir = py_dir_path)

        cls.logger().debug(f'#end# nb to py to wheel install {pkg_name, pkg_parent_dir, nb_dir_path, py_dir_path, repo_url, required_modules}')   

    @classmethod
    def nb_to_py_to_wheel_install_upload(cls, pkg_name, pkg_parent_dir = '.', nb_dir_path = '.', py_dir_path = '.', repo_url = PyToPypi.URL_TEST_PYPI, required_modules = None, seconds_timeout = 120):
        cls.logger().debug(f'#beg# nb to py to wheel install upload {pkg_name, pkg_parent_dir, nb_dir_path, py_dir_path, repo_url, required_modules, seconds_timeout}')
                
        cls.nb_to_py_to_wheel_install(
            pkg_name = pkg_name, 
            pkg_parent_dir = py_dir_path, 
            nb_dir_path = nb_dir_path,
            py_dir_path = py_dir_path,
            repo_url = repo_url,
            required_modules = required_modules
        )

        cls.upload_wheel_to_repo( 
            pkg_name = pkg_name, 
            pkg_parent_dir = pkg_parent_dir, 
            repo_url = repo_url, 
            seconds_timeout = seconds_timeout
        )

        cls.logger().debug(f'#end# nb to py to whl install {pkg_name, pkg_parent_dir, nb_dir_path, py_dir_path, repo_url, required_modules, seconds_timeout}')   



























