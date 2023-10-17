from setuptools import setup, find_namespace_packages

packagereqs = ['pygame', 'pandas', 'Scipy', 'Numpy']

with open('README.txt', 'r') as fh:
    long_description = fh.read()

setup(
    name='BS2-Back',
    version='1.0.2',
    packages=find_namespace_packages(include=['2-Back Requirements']),
    install_requires=packagereqs,
    entry_points={
        'console_scripts': [
            'myproject = myproject.main:main'
        ]
    },
    description=long_description,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    data_files=[('.', ['LICENSE.txt','README.txt', 'MANIFEST.in'])],
)
