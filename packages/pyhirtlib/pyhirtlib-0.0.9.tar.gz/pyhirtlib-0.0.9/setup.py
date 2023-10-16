from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyhirtlib',
  version='0.0.9',
  description='A tag reader for halo infinite',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jorge Glez',
  author_email='urium86@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='halo infinite, tags, module', 
  include_package_data=True,
  package_data={"pyhirtlib": ['unpacker/oo2core_8_win64.dll']},
  packages=find_packages(),
  install_requires=[''] 
)
