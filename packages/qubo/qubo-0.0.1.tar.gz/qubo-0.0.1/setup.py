import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()


dependencies = ["numpy"]
lint = ["black", "flake8", "isort"]
test = ["coverage", "pytest"]
dev = lint + test


setuptools.setup(
    name="qubo",
    version="0.0.1",
    description="Formulation of QUBO problems.",
    url="https://github.com/bqth29/qubo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
    ],
    install_requires=dependencies,
    extras_require={
        "lint": lint,
        "test": test,
        "dev": dev,
        "all": dev,
    },
    python_requires=">=3.8",
    package_dir={"": "src"},
)
