import os
import subprocess
from functools import reduce
from collections import namedtuple
from django.core.management.base import BaseCommand

FileOutput = namedtuple('FileOutput', ['file_path', 'output', 'score'])


def extract_score_from_output(output):
    output = output.strip()
    return int(output.split()[-1])


def generate_file_output(file_path, output):
    output = output.strip()
    return [FileOutput(file_path, _output, extract_score_from_output(_output)) for _output in output.split('\n')]


def main(my_min=9):
    my_path = './'

    all_filters = [
        # 'python_file'
        lambda name: True if name.endswith('.py') else False,
        # 'exclude_migration_file'
        lambda name: True if not name[0].isdigit() else False,
        # exclude_double_under_score_file
        lambda name: True if not name.startswith('__') else False,
    ]

    all_python_file_paths = [os.path.join(os.path.relpath(dir_path, my_path), file)
                             for (dir_path, dir_names, file_names) in os.walk(my_path)
                             for file in list(reduce(lambda s, f: filter(f, s), all_filters, file_names))
                             if not dir_path.startswith('__')]

    results = []

    for file_path in all_python_file_paths:
        byte_output = subprocess.check_output(['python', '-m', 'mccabe', '--min', str(my_min), file_path])
        output = byte_output.decode("utf-8")
        if output:
            results.extend(generate_file_output(file_path, output))

    # filter out the ones without output
    results = filter(lambda r: r.output, results)

    # sort the results by score
    results = sorted(results, key=lambda r: -r.score)

    # print out the result order by complexity desc under format
    print('\n\n'.join(['\n'.join(('\t' + r.file_path, '\n\t\t' + r.output)) for r in results]))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-m', '--min', type=int)

    def handle(self, *args, **options):
        """
        mccabe analyze in django project, detect all python code files, and analyze them
        
        Usage:
            ./manage.py cyclomatic_complexity
            
        :param args: 
        :param options: 
        :return: 
        """
        my_min = options.get('min')
        if my_min is None:
            my_min = 9
        main(my_min=my_min)
