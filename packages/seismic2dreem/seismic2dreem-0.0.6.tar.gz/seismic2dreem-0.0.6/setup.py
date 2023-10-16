from setuptools import setup, find_packages


setup(
    name="seismic2dreem",
    version='0.0.6',
    description="Converts seismic data to dreem format",
    author="Yves Martin des Taillades for the Rouskin Lab",
    author_email="yves@martin.yt",
    url="https://github.com/rouskinlab/seismic2dreem",
    packages=find_packages(),
    install_requires=['pandas','numpy','click'],
    python_requires=">=3.9",
    # add entry point
    entry_points={
        'console_scripts': [
            'seismic2dreem = seismic2dreem.cli:cli'
        ]
    },
)
