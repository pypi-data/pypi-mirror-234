import import_ipynb
import os
from pathlib import Path

from logclshelper import LogClsHelper
from syshelper import SysHelper
from venvhelper import VenvHelper

class PyToWhl(LogClsHelper):

    @classmethod
    def run_cmd(cls, cmd):
        return SysHelper.run_cmd(cmd)

    @classmethod
    def get_installed_pkgs(cls):
        return cls.run_cmd('pip freeze').stdout.read().decode().split('\n')[:-1]

    @classmethod
    def get_installed_version_of_pkg(cls, pkg_name):
        local_version = self.run_cmd(f'pip freeze | grep {pkg_name}').stdout.read().decode().split('==')[-1].strip()
        return local_version
        
    @classmethod
    def install_pkgs(cls, pkgs = []):
        cls.logger().debug(f'#beg# install pkgs {pkgs}')
        
        if(any(pkgs)):
            cls.run_cmd(f'pip install {" ".join(pkgs)}')

        cls.logger().debug(f'#end# install pkgs {pkgs}')

    @classmethod
    def uninstall_pkgs(cls, pkgs = []):
        cls.logger().debug(f'#beg# uninstall pkgs {pkgs}')
        
        if(any(pkgs)):
            cls.run_cmd(f'pip uninstall {" ".join(pkgs)} -y')

        cls.logger().debug(f'#end# uninstall pkgs {pkgs}')

    @classmethod
    def increment_pkg_version(cls, version):
        version_without_dot = version.replace('.', '')
        next_version_int = int(version_without_dot) + 1
        next_version_str = str(next_version_int).zfill(len(version_without_dot))
        next_version_dot = '.'.join(crc for crc in next_version_str)
        return next_version_dot

    @classmethod
    def generate_requirements_txt_lines(cls):
        cls.logger().debug('#beg# generate requirements.txt lines')

        lines = [pkg.replace('==', '>=') for pkg in cls.get_installed_pkgs()]

        cls.logger().debug(f'#end# generate requirements.txt lines {lines}')
        
        return lines

    @classmethod
    def generate_requirements_txt_file(cls, pkg_parent_dir = '.', required_modules = None):
        cls.logger().debug(f'#beg# generate requirements.txt file {pkg_parent_dir}')

        lines = cls.generate_requirements_txt_lines() if required_modules is None else required_modules
        
        output_path = os.path.join(pkg_parent_dir, 'requirements.txt')
        with open(output_path, 'w') as fw:
            fw.write('\n'.join(lines))

        cls.logger().debug(f'#end# generate requirements.txt file {output_path}')

    @classmethod
    def generate_readme_md_lines(cls, pkg_parent_dir = '.'):
        cls.logger().debug('#beg# generate README.md lines')
        
        content = [
            '#### README ####'
        ]
        
        cls.logger().debug('#end# generate README.md lines')
        
        return content

    @classmethod
    def generate_readme_md_file(cls, pkg_parent_dir = '.'):
        cls.logger().debug(f'#beg# generate README.md file {pkg_parent_dir}')
        
        lines = cls.generate_readme_md_lines(pkg_parent_dir = pkg_parent_dir)

        output_path = os.path.join(pkg_parent_dir, 'README.md')
        with open(output_path, 'w') as fw:
            fw.write('\n'.join(lines))

        cls.logger().debug(f'#end# generate README.md file {output_path}')

    @classmethod
    def generate_setup_py_lines(cls, pkg_name, pkg_parent_dir = '.', pkg_version_to_build = '0.0.0'):
        cls.logger().debug(f'#beg# generate setup.py lines {pkg_name, pkg_parent_dir, pkg_version_to_build}')
        
        lines = [
            'import setuptools',
            
            '\n',
            'with open("' + os.path.join(pkg_parent_dir, "requirements.txt") + '") as fr:',
            '\trequirements = fr.read().splitlines()',
            '\n',

            'with open("' + os.path.join(pkg_parent_dir, "README.md") + '") as fr:',
            '\tlong_description = fr.read()',
            '\n',
            
            'setuptools.setup(',
            f'name="{pkg_name}",',
            f'version="{pkg_version_to_build}",',
            'packages=setuptools.find_packages(),',
            'install_requires=requirements,',
            'long_description=long_description,',
            'long_description_content_type="text/markdown"',
            ')',
        ]

        cls.logger().debug(f'#end# generate setup.py lines {pkg_name, pkg_parent_dir, pkg_version_to_build}')

        return lines

    @classmethod
    def generate_setup_py_file(cls, pkg_name, pkg_parent_dir = '.', pkg_version_to_build = '0.0.0'):   
        cls.logger().debug(f'#beg# generate setup.py file {pkg_name, pkg_parent_dir, pkg_version_to_build}')
      
        output_path = os.path.join(pkg_parent_dir, 'setup.py')
        with open(output_path, 'w') as fw:
            fw.write('\n'.join(cls.generate_setup_py_lines(pkg_name = pkg_name, pkg_parent_dir = pkg_parent_dir, pkg_version_to_build = pkg_version_to_build)))    
    
        cls.logger().debug(f'#end# generate setup.py file {pkg_name, pkg_parent_dir, pkg_version_to_build}')

    @classmethod
    def get_paths_to_remove_before_generate(cls, pkg_parent_dir = '.'):
        egg_info_files = SysHelper.yield_filtered_paths(
            parent_dir = pkg_parent_dir, 
            lambda_filter_path = lambda path : path.endswith('.egg-info'),
            accept_dirs = True,
            min_depth = 0,
            max_depth = 0
        )
        
        return [
            os.path.join(pkg_parent_dir, 'requirements.txt'),
            #os.path.join(pkg_parent_dir, 'README.md'),
            os.path.join(pkg_parent_dir, 'setup.py'),
            os.path.join(pkg_parent_dir, 'build'),
            os.path.join(pkg_parent_dir, 'dist')
        ] + [egg_info_file for egg_info_file in egg_info_files]
 
    @classmethod
    def remove_paths_to_generate(cls, pkg_parent_dir = '.'):
        cls.logger().debug(f'#beg# remove paths to generate {pkg_parent_dir}')
        
        for path in cls.get_paths_to_remove_before_generate(pkg_parent_dir = pkg_parent_dir):
            cls.run_cmd(f'rm -rf {path}')
    
        cls.logger().debug(f'#end# remove paths to generate {pkg_parent_dir}')
        
    @classmethod
    def generate_meta_files(cls, pkg_name, pkg_parent_dir = '.', required_modules = None, pkg_version_to_build = '0.0.0'):
        cls.logger().debug(f'#beg# generate meta files {pkg_name, pkg_parent_dir, pkg_version_to_build}')
        
        cls.remove_paths_to_generate(pkg_parent_dir = pkg_parent_dir)

        if(not os.path.exists(os.path.join(pkg_parent_dir, 'README.md'))):
            cls.generate_readme_md_file(pkg_parent_dir = pkg_parent_dir)
            
        cls.generate_requirements_txt_file(pkg_parent_dir = pkg_parent_dir, required_modules = required_modules)
        cls.generate_setup_py_file(pkg_parent_dir = pkg_parent_dir, pkg_name = pkg_name, pkg_version_to_build = pkg_version_to_build)

        cls.logger().debug(f'#end# generate meta files {pkg_name, pkg_parent_dir, pkg_version_to_build}')

    @classmethod
    def build_wheel_from_setup_py_file(cls, pkg_parent_dir = '.'):
        cls.logger().debug(f'#beg# build wheel from setup.py file {pkg_parent_dir}')
                
        with VenvHelper.activate_venv_context(f'venv-pytowhl-{str(id(pkg_parent_dir))}'):
            cls.run_cmd('pip install wheel build')
            cls.run_cmd(f'python -m build {pkg_parent_dir}')

        cls.logger().debug(f'#end# build wheel from setup.py file {pkg_parent_dir}')

    @classmethod
    def install_pkg_as_editable(cls, pkg_parent_dir = '.'):
        cls.logger().debug(f'#beg# install pkg as editable')
        
        SysHelper.run_cmd(f'pip install -e {pkg_parent_dir}')

        cls.logger().debug(f'#end# install pkg as editable')

    @classmethod
    def convert_py_to_wheel(cls, pkg_name, pkg_parent_dir = '.', required_modules = None, pkg_version_to_build = '0.0.0'):
        cls.logger().debug(f'#beg# convert py to wheel {pkg_name, pkg_parent_dir, pkg_version_to_build}')

        cls.generate_meta_files(pkg_name = pkg_name, pkg_parent_dir = pkg_parent_dir, required_modules = required_modules, pkg_version_to_build = pkg_version_to_build)
        cls.build_wheel_from_setup_py_file(pkg_parent_dir = pkg_parent_dir)
        
        cls.logger().debug(f'#end# convert py to wheel {pkg_name, pkg_parent_dir, pkg_version_to_build}')





