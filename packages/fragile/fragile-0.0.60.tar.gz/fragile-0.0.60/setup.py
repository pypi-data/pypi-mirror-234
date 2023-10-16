from importlib.machinery import SourceFileLoader
from pathlib import Path

from setuptools import find_packages, setup


version = SourceFileLoader(
    "fragile.version",
    str(Path(__file__).parent / "fragile" / "version.py"),
).load_module()

with open(Path(__file__).with_name("README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Module-specific dependencies.
extras = {
    "atari": ["atari-py==0.1.1", "opencv-python", "gym==0.17.3", "pillow-simd", "plangym>=0.0.31"],
    "dataviz": [
        "matplotlib==3.7.1",
        "bokeh==2.4.0",
        "pandas==1.5.3",
        "panel==0.14.4",
        "holoviews",
        "hvplot",
        "plotly",
        "streamz",
        "param",
        "selenium",
        "pyarrow",
    ],
    "test": [
        "pytest==6.2.5",
        "pytest-cov==3.0.0",
        "pytest-xdist==2.4.0",
        "pytest-rerunfailures==10.2",
        "hypothesis==6.24.6",
    ],
    "ray": ["ray>=1.0.1.post1", "setproctitle"],
}

# Meta dependency groups.
extras["all"] = [item for group in extras.values() for item in group]

setup(
    name="fragile",
    description="Framework for developing FractalAI based algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    version=version.__version__,
    license="MIT",
    author="Guillem Duran Ballester",
    author_email="info@fragile.tech",
    url="https://github.com/FragileTech/fragile",
    download_url="https://github.com/FragileTech/fragile",
    keywords=["reinforcement learning", "artificial intelligence", "monte carlo", "planning"],
    tests_require=["pytest>=5.3.5", "hypothesis>=5.6.0"],
    extras_require=extras,
    install_requires=[
        "einops",
        "flogging",
        "judo>=0.0.15",
        "networkx",
        "numba",
        "scipy",
        # "plangym>=0.0.31",
        "tqdm",
    ],
    package_data={"": ["README.md"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
)
