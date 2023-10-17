"""The titan-iris module is a Python SDK for the TitanML platform."""
from setuptools import find_packages, setup

setup(
    name="titan-iris",
    install_requires=[
        "typer ~= 0.7.0",
        "rich ~= 13.3.1",
        "omegaconf ~= 2.3.0",
        "requests ~= 2.28.2",
        "auth0-python ~= 3.24.1",
        "python-dotenv ~= 0.19.1",
        "docker ~= 6.0.1",
        "tqdm ~=4.64.1",
        "wget ~= 3.2",
        "jmespath ~= 1.0",
        "tritonclient[http] ~= 2.30.0",
        "numpy >= 1.20.0",
        "tabulate ~= 0.9.0",
        "trogon ~= 0.2.1",
        "shortuuid ~= 1.0.11",
        "einops ~= 0.6.1",
        "py-cpuinfo ~= 8.0.0",
        "importlib-metadata >= 4.0.1",
        "pandas >= 1.3.5",
    ],
    entry_points={"console_scripts": ["iris = iris.main:main"]},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    use_scm_version={"root": "..", "local_scheme": "no-local-version"},
    setup_requires=["setuptools_scm"],
)
