import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
        name='django-lti',
        version='0.1',
        packages=['lti'],
        include_package_data=True,
        description='LTI django application designed to work with socraticqs2',
        long_description=README,
        author='Alexander Kryklia, Maksim Sokolskiy',
        author_email='alex.kryklia@raccoongang.com, maksim.sokolskiy@raccoongang.com',
        classifiers=[
                    'Environment :: Web Environment',
                    'Framework :: Django',
                    'Intended Audience :: Developers',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.7',
                    'Topic :: Internet :: WWW/HTTP',
                    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                ],
)
