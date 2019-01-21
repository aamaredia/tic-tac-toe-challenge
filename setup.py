import os
from setuptools import setup, find_packages

from tictactoe import VERSION


def get_requirements():
    req_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'requirements.txt')
    rfh = open(req_file, 'r')
    requirements = rfh.read().split('\n')
    app_requirements = [i for i in requirements if not i.startswith('#') and i.find('://') == -1]
    return app_requirements


def get_dependencies():
    req_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'requirements.txt')
    rfh = open(req_file, 'r')
    dependency_links = rfh.read().split('\n')
    dependency_links = [i for i in dependency_links if not i.startswith('#') and i.find('://') > 0]
    return dependency_links


setup(
    name='tictactoe',
    version=VERSION,
    description='Tic Tac Toe API',
    packages=find_packages(),
    install_requires=get_requirements(),
    dependency_links=get_dependencies()
)
