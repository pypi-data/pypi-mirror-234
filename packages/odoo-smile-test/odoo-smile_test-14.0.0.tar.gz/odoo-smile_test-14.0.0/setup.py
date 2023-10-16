from distutils.core import setup
from setuptools import find_packages


setup(
    name='odoo-smile_test',
    version='14.0.0',
    packages=find_packages(),
    include_package_data=True,
    license='LGPL',
    description='Smile test module',
    author='Smile',
    author_email='martin.deconinck@smile.fr',
    # url='https://github.com/madecsmile/odoo_smile_test',
    # download_url='https://github.com/madecsmile/odoo_smile_test/archive/refs/tags/16.0.0.zip',
    keywords=['odoo', 'test', 'smile_test', 'smile'],
    install_requires=[
        'coverage',
        'flake8',
        'unittest2',
        'pycobertura',
        'xmlrunner',
        'debugpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
