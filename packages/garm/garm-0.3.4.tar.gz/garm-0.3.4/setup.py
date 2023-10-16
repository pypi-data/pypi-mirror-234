import platform
from setuptools import setup, find_packages

def requirements_from_file(file_name):
    return open(file_name).read().splitlines()

#The root_is_pure bit tells the wheel machinery to build 
# a non-purelib (pyX-none-any) wheel. 
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None


pf = platform.system()

if pf == 'Windows':
    package_data = ['lib/libcgarm.dll','lib/libgarm.dll']
elif pf == 'Linux':
    package_data = ['lib/libcgarm.so','lib/libgarm.so']
else:
    package_data = ['lib/libcgarm.dylib','lib/libgarm.dylib']

setup(
    name='garm',
    packages=['garm'],
    package_dir={'garm':'garm'},
    package_data={'garm':package_data},
    description='Library to generate 3D animation (glTF,USD) files from robot model in URDF',
    version='0.3.4',
    author='Masanobu Koga',
    author_email='koga@ics.kyutech.ac.jp',
    keywords=['URDF', 'ROS', 'robot', 'glTF', 'USD'],
    install_requires=requirements_from_file('requirements.txt'),
    classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS',
          ],
    cmdclass={'bdist_wheel' : bdist_wheel}
)
