from setuptools import find_packages, setup
setup(
    name='quahris',
    packages=find_packages(include=['quahris']),
    version='0.0.4.1',
    description='API Library for Qualys',
    author='Chris Nam',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)