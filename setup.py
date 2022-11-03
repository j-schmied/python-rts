from distutils.core import setup
from setuptools import find_packages

setup(name="python-rts", 
      version="0.1",
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
      packages=["rts"],
      zip_safe=False
)