from setuptools import setup, find_packages
import lxmlasdict


with open('README.md', 'r') as f:
    long_description = f.read()


with open('requirements/base.txt', 'r') as f:
    install_requires = f.read().splitlines()


setup(
    name='lxmlasdict',
    version=lxmlasdict.__version__,
    description=lxmlasdict.__doc__,
    license=lxmlasdict.__license__,
    author=lxmlasdict.__author__,
    author_email='alisher.nazarkhanov.dev@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nazarkhanov/lxmlasdict',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Text Processing :: Markup :: XML',
    ],
)
