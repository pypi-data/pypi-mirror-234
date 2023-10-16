from setuptools import setup, find_packages

setup(
    name="pixegami_hello",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "pixegami-hello = pixegami_hello:hello",
        ],
    },
)
