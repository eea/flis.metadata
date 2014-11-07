import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-flis-metadata-client',
    version='0.1',
    packages=['flis_metadata',
              'flis_metadata.client',
              'flis_metadata.common',
              'flis_metadata.common.migrations'],
    install_requires=['requests'],
    include_package_data=True,
    license='BSD License',
    description='EEA Metadata models replication support',
    long_description=README,
    author='Mihai Bivol',
    author_email='mm.bivol@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
