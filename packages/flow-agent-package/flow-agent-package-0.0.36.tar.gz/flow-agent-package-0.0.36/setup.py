from setuptools import find_packages, setup

setup(
    name="flow-agent-package",
    version="0.0.36",
    description="This is my agent tools package",
    packages=find_packages(),
    entry_points={
        "package_tools": ["flow_agent = flow_agent_package.tools.utils:list_package_tools"],
    },
    install_requires=[
        'semantic_kernel',
        "keyrings.alt",
        "azureml-rag==0.1.24.2"
    ],
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)
