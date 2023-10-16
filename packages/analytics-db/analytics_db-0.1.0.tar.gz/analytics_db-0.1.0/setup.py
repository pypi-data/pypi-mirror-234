from setuptools import find_packages, setup

setup(
    name="analytics_db",
    version="0.1.0",
    url="https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/analytics-db",
    author="Lemon AI",
    author_email="dev@lemon-ai.com",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["clickhouse-driver[lz4,zstd]==0.2.6"],
    extras_require = {
        "pandas":  ["pandas==2.0.3"]
    }
)
