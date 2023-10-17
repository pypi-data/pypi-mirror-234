import setuptools
from setuptools import setup
from setuptools.command.install import install
import subprocess
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
# class CustomInstallCommand(install):
#     def run(self):
#         install.run(self)
#         subprocess.call(['python', 'install_spekpy.py'])

setup(
    name='multiel_spectra',
    author='Fernando Garcia-Avello ',
    author_email='fgarciaa@fi.infn.it',
    description='Multi-Element Fluorescence Xray Spectra Generator',
    keywords='xray,fluorescence, pypi, package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://baltig.infn.it/fgarciaa/multiel_spectra',
    project_urls={
        'Documentation': 'https://baltig.infn.it/fgarciaa/multiel_spectra',
        'Bug Reports':
        'https://baltig.infn.it/fgarciaa/multiel_spectra',
        'Source Code': 'https://baltig.infn.it/fgarciaa/multiel_spectra',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'xraylarch>=0.9.68',  
        'scipy',
        'pandas', 
        'numpy', 
        'matplotlib', 
        'bokeh'
        ],
    # cmdclass={
    #     'install': CustomInstallCommand,
    # },
    dependency_links=[
        'git+https://github.com/username/repo.git#egg=package_name',
    ],
    extras_require={
        "torch": ["torch"],
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    include_package_data=True,
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)
