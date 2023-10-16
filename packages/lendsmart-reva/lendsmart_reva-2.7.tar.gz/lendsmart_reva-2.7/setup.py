from setuptools import setup, find_packages
import reva
import pkg_resources
import setuptools
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if (pkg_resources.parse_version(setuptools.__version__) >=
    pkg_resources.parse_version('36.2.0')):
    install_requires = [
        "remoto >= 1.1.4",
        "configparser;python_version<'3.0'",
        "setuptools < 45.0.0;python_version<'3.0'",
        "python-graphql-client",
        "ramda",
        "lendsmart-autotest",
        "setuptools;python_version>='3.0'",
        "PyJWT==2.7.0",
        "cryptography==37.0.4",
        "lendsmart-api"]
else:
    install_requires = [
        "remoto >= 1.1.4",
        "configparser",
        "python-graphql-client",
        "ramda",
        "lendsmart-autotest",
        "setuptools < 45.0.0",
        "PyJWT==2.7.0",
        "cryptography==37.0.4",
        "lendsmart-api"]

setup(
    name='lendsmart_reva',
    version=reva.__version__,
    packages=find_packages(),

    author='Lendsmart',
    author_email='accounts@lendsmart.ai',
    description='Lendsmart opinionated tool to mirror QA to Prod. Deploy with ease.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    keywords='lendsmart reva',
    url="https://github.com/lendsmartlabs",

    install_requires=install_requires,

    tests_require=[
        'pytest >=2.1.3',
        'mock >=1.0b1',
        ],

    entry_points={

        'console_scripts': [
            'reva = reva.cli:main',
            ],

        'reva.cli': [
            'info = reva.info:show',
            'ready = reva.info:ready',
            'workflow = reva.workflow:workflow',
            'sitesettings = reva.site_settings:site_settings',
            'namespace = reva.namespaces:namespaces',
            'autotest = reva.autotest:autotest',
            'loanproducts = reva.loan_products:loan_products',
            'documentaccesscontrol = reva.document_access_control:document_access_control',
            'roles = reva.roles:roles',
            'permissions = reva.permissions:permissions',
            'rolesandpermissions = reva.roles_and_permissions:roles_and_permissions',
            'branch = reva.branch:branch',
            'advisorprofiles = reva.advisor_profile:advisor_profile',
            'autotest_runner = reva.autotest_runner:autotest'
            ],

        },
    )
