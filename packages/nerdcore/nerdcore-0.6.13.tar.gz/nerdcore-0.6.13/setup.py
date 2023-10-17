from setuptools import setup, find_packages

setup(
    name='nerdcore',
    version='0.6.13',
    __description__="Nerd CLI is a Fivable-specific and highly configurable CLI tool for creating/running deployments, " \
                    "commands, and more.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/fivable/nerd-cli.git',
    author='David Wallace Cooley Jr',
    author_email='david@fivable.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'openai', 'pyyaml', 'python-dotenv', 'python-Levenshtein',
        'termcolor', 'tiktoken', 'psutil', 'ruamel.yaml'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'nerdcore=nerdcore.__main__:main',
        ],
    },
    scripts=['scripts/nerd', 'scripts/nerd-new']
)
