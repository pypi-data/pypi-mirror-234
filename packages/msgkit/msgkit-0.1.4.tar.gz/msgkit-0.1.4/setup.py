from setuptools import find_packages, setup
setup(
    name='msgkit',
    packages=find_packages(include=['msgkit']),
    version='0.1.4',
    license='MIT',
    description='A Python library that is used for logging informative causes/solutions for given errors.',
    long_description='A Python library that is used for logging informative causes/solutions for given errors.',
    author='Jack Scallan',
    author_email='jack.gregory.scallan@gmail.com',
    url='https://github.com/JackScallan02/msgkit',
    download_url='https://github.com/JackScallan02/msgkit/archive/refs/tags/v_01.4.tar.gz',
    keywords=['LOGGING', 'LOG', 'LOGS', 'ERROR','ERRORS'],
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],

)