import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strimdb",
    version="1.0.5",
    author="matf",
    author_email="matf@disr.it",
    description="A TUI to search IMDb, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.sr.ht/~matf/strimdb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["requests", "argparse", "bs4"],
    scripts=["strimdb"],
)
