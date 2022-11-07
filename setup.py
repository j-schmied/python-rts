from distutils.core import setup
from setuptools import find_packages

try:
      from version import __version__
except ModuleNotFoundError:
      exec(open("Module/version.py").read())

setup(name="python-rts", 
      version=__version__,
      packages=find_packages(),
      package_data={p: ['*'] for p in find_packages()},
      description="A package for Real Time Systems calculations", 
      url="https://github.com/j-schmied",
      author="Jannik Schmied",
      author_email="jannik.schmied@stud.htw-dresden.de",
      license="MIT",
      install_requires=[
            "numpy"
      ],
      zip_safe=False
)