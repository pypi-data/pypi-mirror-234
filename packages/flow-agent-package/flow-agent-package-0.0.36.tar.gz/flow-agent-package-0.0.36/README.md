# Create your own tool package
To rapidly create your own tool package, duplicate the `tool-package-quickstart` folder. Substitute `my_tool` with the specific tools you would like to include in your package.

### Prerequisites
Run below command to install PromptFlow dependencies:
```
// Eventually the dependency is prompt-flow package.
pip install promptflow-sdk[builtins]==0.0.99385094 --extra-index-url https://azuremlsdktestpypi.azureedge.net/promptflow/
```
Install Pytest packages for running tests:
```
pip install pytest
pip install pytest-mock
```

### Detailed steps
In this section, we outline the essential steps to create your tool package. Kindly follow the step-by-step instructions below.
* step 1. Create your tool  
  Implement tool with @tool decorator. There are two ways to write a tool.

  - Option 1 **[Recommended]**: function implementation way, using [my_tool_1.py](my_tool_package/tools/my_tool_1.py) as a reference.
  - Option 2: class implementation way, referring to [my_tool_2.py](my_tool_package/tools/my_tool_2.py) as an example. 


* step 2. Create tool yaml
  
  Please refer to [my_tool_1.yaml](my_tool_package/yamls/my_tool_1.yaml) for guidance.
  
  Alternatively, use the following command under `tool-package-quickstart` folder to generate the tool meta yaml file:
  ```
  python ..\scripts\package_tools_generator.py -m <tool_module> -o <tool_yaml_path>
  ```
  For example:
  ```
  python ..\scripts\package_tools_generator.py -m my_tool_package.tools.my_tool_1 -o my_tool_package\yamls\my_tool_1.yaml
  ```

* step 3. Implement list tool API
  
  The [List Package Tool API](my_tool_package/tools/utils.py), which retrieves YAML files for your tools, is utilized by the user interface (UI) to display the available tools.

* step 4. Configure entry point in package setup.py
  
  In Python, configuring the entry point in [setup.py](setup.py) helps establish the primary execution point for a package, streamlining its integration with other software. The `package_tools` entry point is specifically utilized by the user interface to automatically display your tools.
  ```python
  entry_points={
        "package_tools": ["<your_tool_name> = <list_module>:<list_method>"],
  },
  ```
  >[!Note] Entry point key must be `package_tools`.

* step 5. Test the tools
  
  To test your tools locally, please refer to [tests folder](tests/). Run below command under `tool-package-quickstart` folder to begin testing.
  ```
  pytest tests
  ```

* step 6. Build the tool package
  
  Execute the following command in the tool package root directory to build your tool package:
  ```
  python setup.py sdist bdist_wheel
  ```
  This will generate a tool package named `my-tools-package-0.0.1.tar.gz` inside the dist folder.

* step 7. Install and test the tool package
    
    First, install your tool package in local environment by running the subsequent command:
    ```
    pip install <path-to-my-tools-package-0.0.1.tar.gz>
    ``` 
    You can ensure the accuracy of your tool package by running the test below. This will return the metadata of all tools installed in your local environment, and you should verify that your tools are listed.
    > [!Note] Kindly make sure to install the tool package before running this script.

    ```python
    def test():
        # `collect_package_tools` gathers all tools info using the `package-tools` entry point. This ensures that your package is correctly packed and your tools are accurately collected. 
        from promptflow.core.tools_manager import collect_package_tools
        tools = collect_package_tools()
        print(tools)


    if __name__ == "__main__":
        test()
    ```