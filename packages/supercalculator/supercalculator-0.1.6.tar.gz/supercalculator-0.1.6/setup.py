from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='supercalculator',
    version='0.1.6',
    description='A high precision calculator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='',
    author='Raymond Grottodden',
    author_email='raymondgrotto651@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['calculator', 'precise', 'math'],
    packages=find_packages(),
    install_requires=['']
)