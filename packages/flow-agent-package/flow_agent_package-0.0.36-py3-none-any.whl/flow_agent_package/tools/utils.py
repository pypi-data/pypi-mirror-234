import yaml
import os
from pathlib import Path
from azure.identity import DefaultAzureCredential

def collect_tools_from_directory(base_dir) -> dict:
    tools = {}
    for f in Path(base_dir).glob("**/*.yaml"):
        with open(f, "r") as f:
            tools_in_file = yaml.safe_load(f)
            for identifier, tool in tools_in_file.items():
                tools[identifier] = tool
    return tools


def list_package_tools():
    """List package tools"""
    yaml_dir = Path(__file__).parents[1] / "yamls"
    return collect_tools_from_directory(yaml_dir)


def get_token_for_audience(audience):
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    token = credential.get_token("https://management.azure.com/.default").token
    return token

def custom_active_instance(self, force=False):
    # def _activate_in_context(self, force=False):
    instance = self.active_instance()
    if instance is not None and instance is not self and not force:
        return
        #raise NotImplementedError(f"Cannot set active dummy since there is another active instance: {instance}")
    self.context_var.set(self)

# TODO: Make time based
def wait_for_completion(run_obj, retries = 5):
  import time
  retry_count = 0
  while retry_count < retries:
    try:
      run_obj._check_run_status_is_completed()
      break
    except:
      time.sleep(5)
      retry_count += 1