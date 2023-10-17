from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='owlsec',
    version='0.9',
    packages=find_packages(),
    install_requires=[
        'pyOpenSSL==23.2.0',
        'requests==2.29.0',
        'urllib3==1.26.17',
        'beautifulsoup4==4.12.2',
        'tldextract==2.2.0',
        'argparse==1.4.0',
    ],
    entry_points={
        'console_scripts': [
            'owlsec=owlsec.main:run',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)