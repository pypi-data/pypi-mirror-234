from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solidlab-perftest-agent",
    version="0.3.10",
    description="SolidLab PerfTest Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SolidLabResearch/solidlab-perftest-agent",
    author="Wim Van de Meerssche",
    author_email="wim.vandemeerssche@imec.be",
    license="EUPL-1.2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["solidlab_perftest_agent"],
    install_requires=[
        "python-dateutil",
        "requests",
        "solidlab-perftest-common >=3.5.1, <4",
        "aiofiles",
        "aiohttp[speedups]",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "solidlab-perftest-agent=solidlab_perftest_agent.main:main",
        ],
    },
    # Zipped eggs don't play nicely with namespace packaging,
    # and may be implicitly installed by commands like python setup.py install.
    # To prevent this, it is recommended that you set zip_safe=False in setup.py
    zip_safe=False,
)
