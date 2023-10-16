import os
from pathlib import Path
import json

from logclshelper import LogClsHelper
from syshelper import SysHelper

class IPyToPy(LogClsHelper):

    @classmethod
    def run_cmd(cls, cmd):
        return SysHelper.run_cmd(cmd)

    @classmethod
    def format_nb_json(cls, nb_json):
        for cell in nb_json['cells']:
            if('outputs' in cell):
                cell['outputs'] = []

    @classmethod
    def format_nb_file(cls, nb_path):
        cls.logger().debug(f'#beg# format nb file {nb_path}')
        
        nb_json = json.load(open(nb_path))
        cls.format_nb_json(nb_json)
        
        with open(nb_path, "w") as outfile:
            json.dump(nb_json, outfile)

        cls.logger().debug(f'#end# format nb file {nb_path}')

    @classmethod
    def yield_nb_file_paths(cls, nb_dir_path = '.'):
        return SysHelper.yield_filtered_paths(
            parent_dir = nb_dir_path,
            lambda_filter_path = lambda path : path.endswith('.ipynb') and ('.ipynb_checkpoints/' not in path),
            accept_dirs = False
        )

    @classmethod
    def format_nb_files(cls, nb_dir_path = '.'):
        cls.logger().debug('#beg# format nb files')
        
        for nb_path in cls.yield_nb_file_paths(nb_dir_path = nb_dir_path):
            cls.format_nb_file(nb_path)

        cls.logger().debug('#end# format nb files')

    @classmethod
    def get_py_path_from_nb_path(cls, nb_path, nb_dir_path = '.', py_dir_path = '.'):
        return nb_path.replace(nb_dir_path, py_dir_path).replace('.ipynb', '.py')

    @classmethod
    def yield_py_lines_from_nb_cell_code_source(cls, nb_cell_code_source, prefix_py_only = '#py# ', suffix_nb_only = ' #nb#'):
        last_stripped_line = ''
        for line in nb_cell_code_source:
            stripped_line = line.strip()
                
            if(not stripped_line.endswith(suffix_nb_only)): 
                if(stripped_line or last_stripped_line):
                    if(stripped_line.startswith(prefix_py_only)):
                        line = line.replace(prefix_py_only, '')
                    yield line
                    last_stripped_line = stripped_line

    @classmethod
    def yield_py_lines_from_nb_cell_markdown_source(cls, nb_cell_markdown_source):
        for line in nb_cell_markdown_source:
            if line.strip():
                yield('#' + line)

    @classmethod
    def yield_py_lines_from_nb_cell(cls, nb_cell, prefix_py_only = '#py# ', suffix_nb_only = ' #nb#'):
        if nb_cell['cell_type'] == 'code':
            return cls.yield_py_lines_from_nb_cell_code_source(nb_cell['source'], prefix_py_only = prefix_py_only, suffix_nb_only = suffix_nb_only)

        elif nb_cell['cell_type'] == 'markdown':
            return cls.yield_py_lines_from_nb_cell_markdown_source(nb_cell['source'])

    @classmethod
    def yield_py_lines_from_nb_json(cls, nb_json, prefix_py_only = '#py# ', suffix_nb_only = ' #nb#'):
        for nb_cell in nb_json['cells']:
            for line in cls.yield_py_lines_from_nb_cell(nb_cell, prefix_py_only = prefix_py_only, suffix_nb_only = suffix_nb_only):
                yield line
            yield '\n\n'

    @classmethod
    def convert_nb_file_to_py_file(cls, nb_file_path, nb_dir_path = '.', py_dir_path = '.', prefix_py_only = '#py# ', suffix_nb_only = ' #nb#'):
        cls.logger().debug(f'#beg# convert nb file to py file {nb_file_path}')
        
        nb_json = json.load(open(nb_file_path))
        py_file_path = cls.get_py_path_from_nb_path(nb_file_path, nb_dir_path = nb_dir_path, py_dir_path = py_dir_path)
        
        py_path_dir = os.path.dirname(py_file_path)
        Path(py_path_dir).mkdir(parents = True, exist_ok = True)
        
        with open(py_file_path, 'w+') as py_file:
            for line in cls.yield_py_lines_from_nb_json(nb_json, prefix_py_only = prefix_py_only, suffix_nb_only = suffix_nb_only):
                py_file.write(line)

        cls.logger().debug(f'#end# convert nb file to py file {nb_file_path} {py_file_path}')

    @classmethod
    def convert_nb_files_to_py_files(cls, nb_dir_path = '.', py_dir_path = '.', prefix_py_only = '#py# ', suffix_nb_only = ' #nb#'):
        cls.logger().debug('#end# convert nb files to py files')
        
        for nb_file_path in cls.yield_nb_file_paths(nb_dir_path = nb_dir_path):
            cls.convert_nb_file_to_py_file(
                nb_file_path = nb_file_path, 
                nb_dir_path = nb_dir_path, 
                py_dir_path = py_dir_path, 
                prefix_py_only = prefix_py_only, 
                suffix_nb_only = suffix_nb_only
            )
            
        cls.logger().debug('#end# convert nb files to py files')

    @classmethod
    def format_convert_nb_files_to_py_files(cls, nb_dir_path = '.', py_dir_path = '.', prefix_py_only = '#py# ', suffix_nb_only = ' #nb#'):
        cls.logger().debug('#beg# format convert nb files to py files')
        
        cls.format_nb_files(nb_dir_path = nb_dir_path)
        
        cls.convert_nb_files_to_py_files(
            nb_dir_path = nb_dir_path, 
            py_dir_path = py_dir_path, 
            prefix_py_only = prefix_py_only, 
            suffix_nb_only = suffix_nb_only
        )

        cls.logger().debug('#end# format convert nb files to py files')
        
    @classmethod
    def is_path_nb_dir(cls, path):
        nb_files = SysHelper.yield_filtered_paths(
            parent_dir = path,
            accept_dirs = False, 
            max_depth = 0,
            lambda_filter_path = lambda path : path.endswith('.ipynb')
        )

        nb_files_not_empty = next(nb_files, None) is not None
        return nb_files_not_empty

    @classmethod
    def yield_nb_dir_paths(cls, nb_dir_path = '.'):
        return SysHelper.yield_filtered_paths(
            parent_dir = nb_dir_path,
            lambda_filter_path = lambda path : cls.is_path_nb_dir(path) and ('.ipynb_checkpoints/' not in path),
            accept_files = False
        )

    @classmethod
    def yield_py_dir_paths(cls, nb_dir_path = '.', py_dir_path = '.'):
        for nb_path in cls.yield_nb_dir_paths(nb_dir_path = nb_dir_path):
            py_path = cls.get_py_path_from_nb_path(nb_path = nb_path, nb_dir_path = nb_dir_path, py_dir_path = py_dir_path)
            yield py_path

    @classmethod
    def clear_py_dir_paths(cls, nb_dir_path = '.', py_dir_path = '.'):
        cls.logger().debug('#beg# clear py dir paths')
        
        for path in cls.yield_py_dir_paths(nb_dir_path = nb_dir_path, py_dir_path = py_dir_path):
            cls.run_cmd(f'rm -rf {path}/*.py')

        cls.logger().debug('#end# clear py dir paths')

    @classmethod
    def clear_py_dir_paths_format_convert_nb_files_to_py_files(cls, nb_dir_path = '.', py_dir_path = '.', prefix_py_only = '#py# ', suffix_nb_only = ' #nb#'):
        cls.logger().debug('#beg# clear py dir paths format convert nb files to py files')
        
        cls.clear_py_dir_paths(nb_dir_path = nb_dir_path, py_dir_path = py_dir_path)
        
        cls.format_convert_nb_files_to_py_files(
            nb_dir_path = nb_dir_path, 
            py_dir_path = py_dir_path, 
            prefix_py_only = prefix_py_only, 
            suffix_nb_only = suffix_nb_only
        )
        
        cls.logger().debug('#end# clear py dir paths format convert nb files to py files')



