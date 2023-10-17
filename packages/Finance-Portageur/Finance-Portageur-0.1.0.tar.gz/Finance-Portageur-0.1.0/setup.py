# -*- coding: utf-8 -*-
from Cython.Build import cythonize
from setuptools import setup
from setuptools import find_packages
from distutils.cmd import Command
from distutils.extension import Extension
import os, sys, io, subprocess, platform
from portageur import __version__

PACKAGE = "portageur"
NAME = "Finance-Portageur"
VERSION = __version__
DESCRIPTION = "Portageur" + VERSION
AUTHOR = "flaght"
AUTHOR_EMAIL = "flaght@gmail.com"
URL = 'https://github.com/flaght'


def git_version():
    from subprocess import Popen, PIPE
    gitproc = Popen(['git', 'rev-parse', 'HEAD'], stdout=PIPE)
    (stdout, _) = gitproc.communicate()
    return stdout.strip()


if "--line_trace" in sys.argv:
    line_trace = True
    print("Build with line trace enabled ...")
    sys.argv.remove("--line_trace")
else:
    line_trace = False


class version_build(Command):

    description = "test the distribution prior to install"

    user_options = [
        ('test-dir=', None, "directory that contains the test definitions"),
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        git_ver = git_version()[:10]
        configFile = 'portageur/__init__.py'

        file_handle = open(configFile, 'r')
        lines = file_handle.readlines()
        newFiles = []
        for line in lines:
            if line.startswith('__version__'):
                line = line.split('+')[0].rstrip()
                line = line + " + \"-" + git_ver + "\"\n"
            newFiles.append(line)
        file_handle.close()
        os.remove(configFile)
        file_handle = open(configFile, 'w')
        file_handle.writelines(newFiles)
        file_handle.close()


requirements = "requirements/py3.txt"

if platform.system() != "Windows":
    import multiprocessing
    n_cpu = multiprocessing.cpu_count()
else:
    n_cpu = 0

ext_modules = [
    'portageur/plugins/models/base.pyx',
    'portageur/plugins/models/chat_models.pyx',
    'portageur/plugins/models/llms.pyx',
    'portageur/plugins/chain/news.pyx',
    #'portageur/plugins/chain/concerns.pyx',
    #'portageur/plugins/chain/empolyee.pyx',
    'portageur/plugins/prompt/base.pyx',
    'portageur/plugins/prompt/esg_hint.pyx',
    'portageur/plugins/prompt/employee_hint.pyx',
    'portageur/plugins/prompt/esg_controversy.pyx',
    #'portageur/plugins/auth/base.pyx',
    # 'portageur/plugins/auth/azure.pyx',
    #'portageur/plugins/auth/openai.pyx'
    #'portageur/plugins/serper/base.pyx',
    #'portageur/plugins/serper/bing.pyx',
]


def generate_extensions(ext_modules, line_trace=True):

    extensions = []

    if line_trace:
        print("define cython trace to True ...")
        define_macros = [('CYTHON_TRACE', 1), ('CYTHON_TRACE_NOGIL', 1)]
    else:
        define_macros = []

    for pyxfile in ext_modules:
        ext = Extension(name='.'.join(pyxfile.split('/'))[:-4],
                        sources=[pyxfile],
                        define_macros=define_macros)
        extensions.append(ext)
    return extensions


ext_modules_settings = cythonize(generate_extensions(ext_modules, line_trace),
                                 compiler_directives={
                                     'embedsignature': True,
                                     'linetrace': line_trace
                                 },
                                 nthreads=n_cpu)

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      ext_modules=ext_modules_settings,
      packages=find_packages(),
      include_package_data=False,
      install_requires=io.open(requirements, encoding='utf8').read(),
      classifiers=[])
