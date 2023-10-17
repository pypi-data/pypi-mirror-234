import setuptools

setuptools.setup(
    name='talkytimes_package',
    author='Steven Correa',
    author_email='brayancorrea78@gmail.com',
    description='Talkytimes package',
    url='https://github.com/Steven339/talkytimes-package',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.10',
    install_requires=[
        "selenium",
        "beautifulsoup4",
        "html5lib",
        "boto3",
        "pytz",
    ]
)
