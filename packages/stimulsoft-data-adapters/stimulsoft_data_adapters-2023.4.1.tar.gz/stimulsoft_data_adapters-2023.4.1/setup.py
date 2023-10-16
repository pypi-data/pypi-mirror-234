from setuptools import setup, find_packages

with open('README.md') as file:
    readmeFile = file.read()

with open('REQUIREMENTS.txt') as file:
    requiresFile = [text.strip() for text in file if text.strip()]

setup(
    name = 'stimulsoft_data_adapters',
    version = '2023.4.1',
    author = 'Stimulsoft',
    author_email = 'info@stimulsoft.com',
    description = 'Stimulsoft Data Adapters for Python',
    long_description = readmeFile,
    long_description_content_type = 'text/markdown',
    url = 'https://www.stimulsoft.com/en',
    license = 'https://www.stimulsoft.com/en/licensing/developers',
    install_requires = ['pyodbc'],
    extras_require = {'ext': requiresFile},
    packages = find_packages(),
    python_requires = '>=3.7'
)
