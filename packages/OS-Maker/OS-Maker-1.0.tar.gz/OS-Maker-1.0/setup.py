from setuptools import setup

setup(
    name='OS-Maker',
    version='v1.0',
    packages=['AssemblyToC', 'os_maker_compiler'],
    url='',
    license='All Free',
    author='JonDev2023',
    author_email='',
    description='Make OS with some languages',
    entry_points={
        'console_scripts': [
            'omc = os_maker_compiler.__main__:main'
        ]
    },
    classifiers=[
        'Operating System :: POSIX :: Linux'
    ]
)