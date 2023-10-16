from setuptools import setup

MAIN_REQUIREMENTS = [
    "pydantic==1.10.11",
    "esdk-obs-python",
    "prefect>=2.10.11"
]

setup(
    name="prefect-hwc",
    description="Prefect collection of tasks and sub flows to integrate with HuaweiCloud",
    license="Apache License 2.0",
    author="HuaweiCloud",
    author_email="",
    keywords="prefect",
    url="https://gitee.com/HuaweiCloudDeveloper/huaweicloud-prefect-block-python",
    version="0.2.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    install_requires=MAIN_REQUIREMENTS,
    classifiers=[],
)
