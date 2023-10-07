# # # # # # # # # # # # # # # # # # # # # #
#    Rewrote on 2023/06/24 by rathaROG    #
#    Updated on 2023/07/23 by rathaROG    #
# # # # # # # # # # # # # # # # # # # # # #


import distutils.cmd
from setuptools import setup
from setuptools.extension import Extension

###################################################################

DESCRIPTION = "Linear Assignment Problem solver (LAPJV/LAPMOD)."
LICENSE = 'BSD-2-Clause'
LONG_DESCRIPTION = open("README.md", encoding="utf-8").read()

###################################################################

package_name = 'lapx'
package_path = 'lap'
_lapjv_src = "_lapjv_src"
requirements_txt = "requirements.txt"

###################################################################

def get_version_string():
    version_py = "lap/__init__.py"
    with open(version_py) as version_file:
        for line in version_file.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]

def read_requirements():
    with open(requirements_txt) as requirements_file:
        return [line for line in requirements_file.read().splitlines()]

def include_numpy():
    import numpy as np
    try:
        numpy_include = np.get_include()
    except AttributeError:
        numpy_include = np.get_numpy_include()
    return numpy_include

def compile_cpp(cython_file):
    """Compile cpp from Cython's pyx or py.
    """
    import os
    import subprocess
    cpp_file = os.path.splitext(cython_file)[0] + '.cpp'
    flags = ['--fast-fail', '--cplus']
    rc = subprocess.call(['cython'] + flags + ["-o", cpp_file, cython_file])
    if rc != 0: raise Exception('Cythonizing %s failed' % cython_file)
    else: return cpp_file

class ExportCythonCommand(distutils.cmd.Command):
    description = 'Export _lapjv binary from source.'
    def run(self):
        super().run()
        import os
        import shutil
        this_dir = os.path.dirname(os.path.realpath(__file__))
        lap = os.path.join(this_dir, "lap")
        _lapjv_src = os.path.join(this_dir, "_lapjv_src")
        for file in  os.listdir(_lapjv_src):
            if file[-2:].lower() in "soyd":
                shutil.copy2(os.path.join(_lapjv_src, file), lap)
                break

def main_setup():
    """Use modern setup() by setuptools
    """
    import os
    from Cython.Build import cythonize
    _lapjvpyx = os.path.join(_lapjv_src, '_lapjv.pyx')
    _lapjvcpp = compile_cpp(_lapjvpyx)
    lapjvcpp = os.path.join(_lapjv_src, 'lapjv.cpp')
    lapmodcpp = os.path.join(_lapjv_src, 'lapmod.cpp')

    ext_modules = [
        Extension(
            name='lap._lapjv',
            sources=[_lapjvcpp, lapjvcpp, lapmodcpp],
            include_dirs=[include_numpy(), _lapjv_src, package_path],
        )
    ]

    package_data = {}
    tests_package = package_path + ".tests"
    packages = [package_path, tests_package]
    for p in packages: package_data.update({p: ["*"]})

    setup(
        name=package_name,
        version=get_version_string(),
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author='rathaROG',
        url='https://github.com/rathaROG/lapx',
        license=LICENSE,
        packages=packages,
        package_data=package_data,
        include_package_data=True,
        keywords=['Linear Assignment', 'LAPJV', 'LAPMOD', 'lap'],
        install_requires=read_requirements(),
        classifiers=['Development Status :: 4 - Beta',
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Education',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: BSD License',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: 3.9',
                     'Programming Language :: Python :: 3.10',
                     'Programming Language :: Python :: 3.11',
                     'Programming Language :: Python :: 3.12',
                     'Topic :: Education',
                     'Topic :: Education :: Testing',
                     'Topic :: Scientific/Engineering',
                     'Topic :: Scientific/Engineering :: Mathematics',
                     'Topic :: Software Development',
                     'Topic :: Software Development :: Libraries',
                     'Operating System :: Microsoft :: Windows',                                  
                     'Operating System :: POSIX',
                     'Operating System :: Unix',
                     'Operating System :: MacOS',],
        ext_modules=cythonize(ext_modules),
        cmdclass={'cmdexport': ExportCythonCommand,},
    )

if __name__ == "__main__":
    """
    Recommend using :py:mod:`build` to build the package as it does not 
    mess up your current enviroment.

    >>> pip install wheel build
    >>> python -m build --sdist
    >>> python -m build --wheel
    """ 
    main_setup()
