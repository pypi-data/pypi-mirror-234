from setuptools import setup, find_packages

setup(
    name='myproject',
    version='1.0.0',
    description='My project description',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'myproject = myproject.main:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
