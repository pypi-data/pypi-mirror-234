import subprocess
import os
import re
from contextlib import contextmanager
from pathlib import Path
import itertools
from logclshelper import LogClsHelper

class SysHelper(LogClsHelper):
    
    @classmethod
    def run_cmd(cls, cmd):
        cls.logger().debug(f'#beg# ! {cmd}')
        
        p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, env = os.environ)
        p.wait()

        cls.logger().debug(f'#end# ! {cmd}')
        return p
                            
    @classmethod
    def yield_filtered_paths(cls, 
        parent_dir = '.', 
        lambda_filter_path = lambda path : True,
        accept_files = True,
        accept_dirs = True,
        min_depth = None,
        max_depth = None
    ):  
        depth = 0

        if((max_depth is None) or (depth <= max_depth)):
            for pdir, dirs, files in os.walk(parent_dir):                
                if((min_depth is not None) and (depth < min_depth)):
                    depth += 1
                    continue
                
                accepted = (
                    itertools.chain(files, dirs) if(accept_files and accept_dirs) 
                    else(
                        files if accept_files 
                        else (
                            dirs if accept_dirs
                            else []
                        )
                    )
                )
                
                for file_or_dir in accepted:
                    path = os.path.join(pdir, file_or_dir)
                    if lambda_filter_path(path):
                        yield path
                
                depth += 1
                            
                if((max_depth is not None) and (depth > max_depth)):
                    break
    
    @classmethod
    @contextmanager
    def chdir_context(cls, path):
        cls.logger().debug(f'#beg# chdir context {path}')
        
        origin = Path().absolute()
        try:
            os.chdir(path)
            yield
        finally:
            os.chdir(origin)
            
            cls.logger().debug(f'#end# chdir context {path}')





