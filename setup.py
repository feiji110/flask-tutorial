import io

from setuptools import find_packages, setup
from setuptools import setup
with io.open('README.md', "rt", encoding="utf-8") as f:
    readme = f.read()

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)