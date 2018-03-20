from setuptools import setup

setup(
    name='osx-tags',
    version='0.1.3',
    packages=['osx_tags'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ], description='Module to manipulate Finder tags on OS X',
    entry_points={
        'console_scripts': [
            'finder-tags=osx_tags.cmd:main [click]',
        ]
    }, extras_require={
        'click': ['click']
    }, install_requires=[
        'biplist',
        'xattr',
    ], license='MIT',
    url='https://github.com/scooby/osx-tags',
    zip_safe=True
)
