import setuptools

long_description:str = open('README.md').read()

setuptools.setup (
    include_package_data=True,
    name='celerabit-pipeline-integration',
    version='1.0.4',
    description='Celerabit tools to integrate with pipelines',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='https://git-codecommit.zone.amazonaws.com/v1/repos/celerabit-pipeline-integration-py-package',
    author='Raul A. de Villa C.',
    author_email='raul.devilla@techandsolve.com',
    python_requires='>=3.6',
    package_dir={'':'.'},
    packages=setuptools.find_packages(exclude=["test", "test.*", "*.test"]),
    install_requires=['requests', 'urllib3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    license_files=('LICENCE',)
)