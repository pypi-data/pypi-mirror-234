from setuptools import __version__, setup

with open("./README.md", "r") as f:
    readme = f.read()

with open("./requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="vtarget",
    packages=[
        "vtarget",
        "vtarget.dataprep",
        "vtarget.dataprep.nodes",
        "vtarget.handlers",
        "vtarget.utils",
    ],
    version="0.1.2",
    description="vtarget lib",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="vTarget Team",
    author_email="contact@vtarget.ai",
    keywords=["vtarget", "dataprep"],
    classifiers=[],
    license="BSD",
    install_requires=requirements,
    include_package_data=False,
)
