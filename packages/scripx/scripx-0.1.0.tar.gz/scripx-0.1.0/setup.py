from setuptools import setup

setup(
    name="scripx",
    version="0.1.0",
    packages=["scripx"],
    entry_points={
        "console_scripts": [
            "scripx = scripx.main:main_cli",
        ],
    },
    install_requires=[
        # Add any dependencies your package needs
    ],
)
