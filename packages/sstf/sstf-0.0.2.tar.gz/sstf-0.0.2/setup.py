from setuptools import find_packages, setup
 
setup(
    name="sstf",
    author="lxhzzy",
    version="0.0.2",
    author_email="lxhzzy@outlook.com",
    description="",
    long_description="",
    license='MIT',
    packages=find_packages(),
    install_requires= [
        "psutil",
        "argparse",
        "pathlib"
    ],
    entry_points={
        'console_scripts': [
            'sstf = sstf:main',
        ],
    }
)