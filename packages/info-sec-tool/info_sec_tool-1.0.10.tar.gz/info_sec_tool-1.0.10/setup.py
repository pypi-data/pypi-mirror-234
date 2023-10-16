from setuptools import setup

setup(
    name='info_sec_tool',
    version='1.0.10',
    py_modules=['mycli'],
    entry_points={
        'console_scripts': [
            'fbc=mycli:main',
        ],
    },
)