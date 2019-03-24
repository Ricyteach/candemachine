"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    name='candemachine',
    version='0.1',
    author="Ricky L Teachey Jr",
    author_email='ricky@teachey.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=requirements,
    license="MIT license",
    description='A simplified CANDE file reader/writer',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='candemachine',
    packages=find_packages(include=['candemachine']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Ricyteach/candemachine',
    zip_safe=False,
)
