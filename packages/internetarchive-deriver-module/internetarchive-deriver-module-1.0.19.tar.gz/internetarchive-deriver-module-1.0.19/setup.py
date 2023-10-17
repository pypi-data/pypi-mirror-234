from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('derivermodule/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

version = main_ns['__version__']
setup(name='internetarchive-deriver-module',
      version=version,
      packages=['derivermodule'],
      description='Python derivermodule package',
      author='Merlijn Boris Wolf Wajer',
      author_email='merlijn@archive.org',
      url='https://git.archive.org/merlijn/python-derivermodule',
      download_url='https://git.archive.org/merlijn/python-derivermodule/-/archive/1.0.0/python-derivermodule-%s.tar.gz' % version,
      keywords=['Deriver', 'Internet Archive'],
      license='AGPL-3.0',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Programming Language :: Python :: 3',
      ],
      python_requires='>=3.6',
      install_requires=['xmltodict==0.12.0'])
