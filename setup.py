import setuptools

setuptools.setup(
    name='zharing',
    version='0.0.1',
    description='zharing',
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={'console_scripts': ['zharing = zharing.main:main', ]},
    )
