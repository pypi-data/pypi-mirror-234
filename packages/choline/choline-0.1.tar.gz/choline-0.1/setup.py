from setuptools import setup, find_packages

setup(
    name='choline',
    version='0.1',
    packages=find_packages(),
    long_description="An easy way to access the cloud from the comamnd line.",
    long_description_content_type='text/plain',
    install_requires=[
        'paramiko',
        'scp',
        'PyYAML',
        'torch',
        'vastai'
    ],

    entry_points={
        'console_scripts': [
            'choline = choline.choline:main',
        ],
    },
)
