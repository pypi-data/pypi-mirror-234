from setuptools import setup, find_packages

setup(
    name='catcode',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'keyring',
        'cryptography',
    ],
    author='moeen dehqan',
    author_email='moeen.dehqan@gmail.com',
    description='A Python library for secure encryption and decryption of sensitive data using the CatCode algorithm.',
    long_description_content_type='text/markdown',
    keywords='encryption security cryptography catcode',
    url='https://github.com/moeendehqan/catcode',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
