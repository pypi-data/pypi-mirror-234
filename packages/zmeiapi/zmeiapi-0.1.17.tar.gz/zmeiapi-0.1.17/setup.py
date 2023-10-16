from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='zmeiapi',
    version='0.1.17',
    description='Useful tools to work with Zmei calculation code',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    include_package_data = True,
    author='Vladislav Romanenko',
    author_email='vliromanenko@yandex.ru',
    keywords=['zmei-api'],
    url='https://github.com/vliromanenko/zmei-api',
    download_url='https://pypi.org/project/zmeiapi/'
)

install_requires = [
    
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=None)
