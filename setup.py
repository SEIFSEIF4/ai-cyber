from setuptools import setup, find_packages

setup(
    name="tsp_evolutionary",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "setuptools>=42.0.0"
    ],
    author="Seifelesllam Seif",
    author_email="seifsaif151@gmail.com",
    description="Evolutionary Algorithm for solving the Travelling Salesman Problem",
    keywords="tsp, evolutionary algorithm, optimization",
    url="https://github.com/SEIFSEIF4/ai-cyber.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
