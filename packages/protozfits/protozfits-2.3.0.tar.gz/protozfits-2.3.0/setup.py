# see https://stackoverflow.com/a/48015772/3838691
import os
import sys
import sysconfig
import pathlib
import subprocess as sp
import re
import warnings

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext


SETUP_DIR = pathlib.Path(__file__).parent.absolute()


with (SETUP_DIR / 'python/protozfits/__init__.py').open('r') as f:
    content = f.read()
    m = re.search(r'__version__ = \'(.*)\'', content)
    if not m:
        raise ValueError()

    version = m.group(1)


with open(os.path.join(SETUP_DIR, 'python/README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_cmake(required_major=3, required_minor=15, required_patch=0):
    '''Find appropriate cmake'''

    # cmake >= 3 is called cmaked3 on centos 7
    for exe in ['cmake3', 'cmake']:
        try:
            ret = sp.run(
                [exe, '--version'],
                stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf-8'
            )
        except Exception:
            continue

        if ret.returncode != 0:
            continue

        m = re.match(r'cmake3? version (\d+).(\d+).(\d+)', ret.stdout)
        if not m:
            warnings.warn('Failed to get cmake version')

        major, minor, patch = map(int, m.groups())
        if major >= required_major and minor >= required_minor and patch >= required_patch:
            return exe

    required_version = f'{required_major}.{required_minor}.{required_patch}'
    raise OSError(f'cmake >= {required_version} is required')


class CMakeExtension(Extension):
    def __init__(self, name, source_dir=None, target=None, **kwargs):
        if source_dir is None:
            self.source_dir = SETUP_DIR
        else:
            self.source_dir = SETUP_DIR / source_dir
        self.target = target
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[], **kwargs)


class build_ext_cmake(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        for d in (self.build_temp, extdir):
            os.makedirs(d, exist_ok=True)

        cfg = 'Debug' if self.debug else 'Release'
        cmake = get_cmake()

        rpath = '@loader_path' if sys.platform == 'darwin' else '$ORIGIN'
        python_lib = pathlib.Path(
            sysconfig.get_config_var('LIBDIR'),
            sysconfig.get_config_var('INSTSONAME'),
        )
        cmake_call = [
            cmake,
            str(ext.source_dir),
            '-DCMAKE_BUILD_TYPE=' + cfg,
            '-DPYTHON=ON',
            '-DSWAT=OFF',
            '-DPYTHON_EXECUTABLE=' + sys.executable,
            '-DPYTHON_LIBRARY=' + str(python_lib),
            '-DPYTHON_INCLUDE_DIR=' + sysconfig.get_path('include'),
            '-DCMAKE_INSTALL_RPATH={}'.format(rpath),
            '-DCMAKE_BUILD_WITH_INSTALL_RPATH:BOOL=ON',
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=OFF',
        ]

        # Add sys.prefix to CMAKE_PREFIX_PATH
        # This e.g. makes setup.py find zeromq / protobuf
        # installed in a conda environment / virtualenv / custom location
        env = os.environ.copy()
        if 'CMAKE_PREFIX_PATH' in os.environ:
            env['CMAKE_PREFIX_PATH'] += os.pathsep + sys.prefix
        else:
            env['CMAKE_PREFIX_PATH'] = sys.prefix

        sp.run(cmake_call, cwd=self.build_temp, check=True, env=env)
        build_call = [
            cmake,
            '--build', '.',
            '--config', cfg,
        ]
        if ext.target is not None:
            build_call.extend(['--target', ext.target])

        build_call.extend(['--', '-j{}'.format(os.getenv('BUILD_CORES', 2))])
        sp.run(build_call, cwd=self.build_temp, check=True, env=env)


extras_require = {
    'tests': ['pytest']
}
extras_require['all'] = list(set(dep for extra in extras_require.values() for dep in extra))

setup(
    package_dir={'': 'python'},
    packages=find_packages('python'),
    name='protozfits',
    description='Python bindings for the protobuf zfits library',
    author="Etienne Lyard et al.",
    author_email="etienne.lyard@unige.ch",
    license="bsd",
    version=version,
    install_requires=['numpy', 'protobuf~=3.20', 'astropy'],
    extras_require=extras_require,
    ext_modules=[
        CMakeExtension('protozfits.rawzfits', target='pyrawzfits'),
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
    ],
    cmdclass={
        'build_ext': build_ext_cmake,
    },
    package_data={'': ['tests/resources/*']},
    zip_safe=False,
)
