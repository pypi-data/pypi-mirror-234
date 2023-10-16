import setuptools
import datetime

__version__ = '2023.10.09'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latest-chromedriver",
    version=__version__,
    author="Charalampos Gkikas",
    author_email="hargikas@gmail.com",
    description="A small package to find the correct chromedriver version in windows machines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hargikas/auto-chromedriver/",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3',
    install_requires=['requests', 'logzero', 'ubelt', 'py-cpuinfo'],
    keywords='chromedriver windows',
    project_urls={
        # 'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        # 'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'https://saythanks.io/to/hargikas',
        'Source': 'https://github.com/hargikas/auto-chromedriver/',
        'Tracker': 'https://github.com/hargikas/auto-chromedriver/issues',
    },
    entry_points={
        'console_scripts': [
            'latest_chromedriver=latest_chromedriver:__main__',
        ],
    },
)
