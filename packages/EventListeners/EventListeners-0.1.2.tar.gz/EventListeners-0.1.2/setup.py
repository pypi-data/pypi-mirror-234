from setuptools import setup, find_packages

setup(
    name='EventListeners',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'azure-eventhub',
        'azure-keyvault',
        'azure-identity',
        'requests'
    ],
    description='Event hub listener for Common Spec use case that triggers DBX jobs',
    author='Archana Bellamkonda',
    author_email='archana.bellamkonda@lamresearch.com'
)
