import subprocess
import os
from contextlib import contextmanager
from pathlib import Path 
from logclshelper import LogClsHelper
from syshelper import SysHelper

class VenvHelper(LogClsHelper):
  
    @classmethod
    def run_cmd(cls, cmd):
        return SysHelper.run_cmd(cmd)
        
    @classmethod
    def get_venv_paths(cls):
        paths = cls.run_cmd('find / -name "*activate" -type f').stdout.read().decode().split('\n')[:-1]
        venv_paths = [path.split('/bin/activate')[0] for path in paths if '/bin/activate' in path]
        return venv_paths

    @classmethod
    def remove_venv_paths_from_path(cls, venv_paths = None):
        cls.logger().debug(f'#beg# remove venv paths {venv_paths} from $PATH')

        if(venv_paths is None):
            venv_paths = cls.get_venv_paths()
        
        paths = os.environ['PATH'].split(':')
                
        venv_path_bins = {os.path.join(venv_path, 'bin') for venv_path in venv_paths}
        paths_without_venv_path_bins = [path for path in paths if path not in venv_path_bins]
        os.environ['PATH'] =  ':'.join(paths_without_venv_path_bins)

        cls.logger().debug(f'#end# remove venv paths {venv_paths} from $PATH {paths, os.environ["PATH"].split(":")}')

    @classmethod
    def create_venv_if_not_exists(cls, venv_dir):
        cls.logger().debug(f'#beg# create venv if not exists {venv_dir}')
        
        not_exists = not os.path.isdir(venv_dir)
        
        if(not_exists):
            cls.run_cmd(f'python -m venv {venv_dir}')
       
        cls.logger().debug(f'#end# create venv if not exists {venv_dir}')

        return not_exists
            
    @classmethod
    def remove_venv_from_path(cls, venv_dir):
        cls.remove_venv_paths_from_path([venv_dir])

    @classmethod
    def activate_venv(cls, venv_dir):
        cls.logger().debug(f'#beg# activate venv {venv_dir}')
        
        os.environ['VIRTUAL_ENV'] = venv_dir
        cls.remove_venv_from_path(venv_dir)
        os.environ['PATH'] =  venv_dir + '/bin:' + os.environ['PATH']

        cls.logger().debug(f'#end# activate venv {venv_dir}')

    @classmethod
    def reset_os_environ(cls, origin_environ):
        cls.logger().debug(f'#beg# reset os environ {origin_environ["PATH"].split(":")}')
        
        os.environ.clear()
        os.environ.update(origin_environ)
        
        cls.logger().debug(f'#beg# reset os environ {origin_environ["PATH"].split(":")}')

    @classmethod
    def deactivate_venv(cls, venv_dir, origin_environ = None):
        cls.logger().debug(f'#beg# deactivate venv {venv_dir}')

        cls.remove_venv_from_path(venv_dir)
        os.environ['VIRTUAL_ENV'] = ''

        if(origin_environ is not None):
            cls.reset_os_environ(origin_environ)

        cls.logger().debug(f'#end# deactivate venv {venv_dir}')

    @classmethod
    def remove_venv_dir(cls, venv_dir):
        cls.logger().debug(f'#beg# remove venv dir {venv_dir}')
        
        cls.run_cmd(f'rm -rf {venv_dir}')

        cls.logger().debug(f'#end# remove venv dir {venv_dir}')

    @classmethod
    @contextmanager
    def activate_venv_context(cls, venv_dir):  
        cls.logger().debug(f'#beg# activate venv context {venv_dir}')
        
        should_remove = False
        
        try:                
            should_remove = cls.create_venv_if_not_exists(venv_dir)
            origin_environ = {**os.environ}
            cls.activate_venv(venv_dir)
            yield
            
        finally:
            cls.deactivate_venv(venv_dir, origin_environ)
            if(should_remove):
                cls.remove_venv_dir(venv_dir)

            cls.logger().debug(f'#end# activate venv context {venv_dir}')











