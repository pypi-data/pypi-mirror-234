import setuptools


mods = ['leanixpy_az']

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name='leanix-az-py',
  version='0.0.4',
  description='Functionality to support the development of Azure Functions',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Felix Jeske',
  author_email='felix.jeske@leanix.net',
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
  #Packages that are included in the project
  packages=mods,
  #Package requirements that 
  install_requires=['requests'],
  setup_requires=['pytest-runner'],
  tests_require=['pytest'],
  test_suite="tests",
)
