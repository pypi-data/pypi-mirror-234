from setuptools import setup, find_packages

setup(
    name="xgh-t",
    version="0.1.1",
    packages=find_packages(exclude=["tests"], where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "x-t = t:main",
        ]
    },
)
