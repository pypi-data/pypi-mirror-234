from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="refract-mlflow-plugin",
    version="1.0.2",
    description="Refract plugin for MLflow",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=find_packages(),
    # Require MLflow as a dependency of the plugin, so that plugin users can simply install
    # the plugin & then immediately use it with MLflow
    install_requires=["mlflow==2.6.0"],
    entry_points={
        "mlflow.request_header_provider": "unused=refract_mlflow_plugin.request_header_provider:RefractRequestHeaderProvider",  # pylint: disable=line-too-long
        # Define a custom Mlflow application with name custom_app
        "mlflow.app": "custom_app=refract_mlflow_plugin.app:custom_app"
    },
)
