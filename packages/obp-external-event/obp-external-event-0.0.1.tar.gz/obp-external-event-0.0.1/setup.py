from setuptools import setup, find_namespace_packages

version = "0.0.1"

setup(
    name="obp-external-event",
    version=version,
    description="Trigger Metaflow executions on the Outerbounds Platform",
    author="Outerbounds",
    author_email="ville@outerbounds.co",
    packages=find_namespace_packages(include=["obpevent"]),
    py_modules=[
        "obpevent"
    ],
    install_requires=[
         "outerbounds"
    ]
)
