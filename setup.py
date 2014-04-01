from setuptools import setup

with open('README.rst', 'r', encoding='utf8') as fp:
    README = fp.read()

requires = [
    'requests',
    'scrypt',
]

setup(
    name='keybase-py',
    version='0.0',
    description='Python bindings for keybase.io',
    long_description=README,
    py_module='keybase',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: MIT',
    ],
    keywords='keybase.io keybase',
    author='Michael Merickel',
    author_email='me@m.merickel.org',
    url='https://github.com/mmerickel/keybase-py',
    license='MIT',
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'keybase = keybase:main',
        ],
    }
)
