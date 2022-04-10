from setuptools import find_packages, setup

from os import path
top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='nautobot_adfs_plugin',
    version='0.0.1',
    description='Nautbot plugin for ADFS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Max Ioncev',
    author_email='iontzev@gmail.com',
    install_requires=[],
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    keywords=['nautobot', 'nautobot-plugin', 'plugin'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
