import setuptools
from django_madmin import __version__ as version

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-madmin",
    version=version,
    author="IT Expendables",
    author_email="ericalunson@gmail.com",
    description="django admin plus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IT-Expendables/django_madmin",
    packages=setuptools.find_packages(exclude=["demo", "demo.*"]),
    include_package_data=True,
    install_requires=['django>=4.0.0,<5.0.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)
