from setuptools import setup, find_packages

setup(
    name='dkdrlahel',
    version='0.0.3',
    description='This is a project developed by Serem for development purposes',
    author='serem',
    author_email='gangh9230@gmail.com',
    url='https://github.com/hayul0629/wdex',
    install_requires=[
        "colored==1.4.4",
        "tk",
        "python-dateutil",
        "requests",
        "pyyaml",
    ],
    packages=find_packages(exclude=[]),
    keywords=['serem'],
    python_requires=">=3.9",
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
