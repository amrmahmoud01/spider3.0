# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name="spider3_0",
    version="0.1",
    packages=find_packages(),
    package_data={
        "spider3_0.configs": ["*.json"],
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={"scrapy": ["settings = spider3_0.settings"]},
)