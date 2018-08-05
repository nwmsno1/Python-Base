from setuptools import find_packages, setup
packages = find_packages()

VERSION = "1.4.2"
setup(name = 'AutoMonitor',
      version = VERSION,
      author = 'XXX',
      author_email = 'xxx@XX.com.cn',
      packages = find_packages(),
      package_dir = {'AutoMonitor': 'automonitor'},
      install_requires = ['numpy', 'pyvisa', 'paramiko'],
      include_package_data = True,
      zip_safe = False
      )
