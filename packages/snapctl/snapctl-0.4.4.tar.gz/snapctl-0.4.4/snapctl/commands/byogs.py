import base64
import json
import os
import re
import requests
import subprocess

from rich.progress import Progress, SpinnerColumn, TextColumn
from sys import platform
from typing import Union
from snapctl.config.constants import ERROR_SERVICE_VERSION_EXISTS, ERROR_TAG_NOT_AVAILABLE
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success
from snapctl.utils.helper import get_composite_token

class ByoGs:
  ID_PREFIX = 'byogs-'
  SUBCOMMANDS = ['create', 'publish-image', 'publish-version']
  PLATFORMS = ['linux/amd64']
  LANGUAGES = ['go', 'python', 'ruby', 'c#', 'c++', 'rust', 'java', 'node']
  DEFAULT_BUILD_PLATFORM = 'linux/amd64'

  def __init__(self, subcommand: str, base_url: str, api_key: str, sid: str, name: str, desc: str, platform: str, language: str, tag: str, path: Union[str, None], dockerfile: str, version: Union[str, None], http_port: Union[int, None]) -> None:
    self.subcommand: str = subcommand
    self.base_url: str = base_url
    self.api_key: str = api_key
    self.sid: str = sid
    self.name: str = name
    self.desc: str = desc
    self.platform: str = platform
    self.language: str = language
    self.token: Union[str, None] = get_composite_token(base_url, api_key, 'byogs', {'service_id': sid}) if subcommand != 'create' else None
    self.token_parts: Union[list, None] = ByoGs.get_token_values(self.token) if self.token is not None else None
    self.tag: str = tag
    self.path: Union[str, None] = path
    self.dockerfile: str = dockerfile
    self.version: Union[str, None] = version
    self.http_port: Union[int, None] = http_port

  @staticmethod
  def get_token_values(token: str) -> None | list:
    try:
      input_token = base64.b64decode(token).decode('ascii')
      token_parts = input_token.split('|')
      # url|web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
      # url = self.token_parts[0]
      # web_app_token = self.token_parts[1]
      # service_id = self.token_parts[2]
      # ecr_repo_url = self.token_parts[3]
      # ecr_repo_username = self.token_parts[4]
      # ecr_repo_token = self.token_parts[5]
      # platform = self.token_parts[6]
      if len(token_parts) >= 3:
        return token_parts
    except Exception:
      pass
    return None

  def validate_input(self) -> ResponseType:
    response: ResponseType = {
      'error': True,
      'msg': '',
      'data': []
    }
    # Check subcommand
    if not self.subcommand in ByoGs.SUBCOMMANDS:
      response['msg'] = f"Invalid command. Valid commands are {', '.join(ByoGs.SUBCOMMANDS)}."
      return response
    # Validate the SID
    if not self.sid.startswith(ByoGs.ID_PREFIX):
      response['msg'] = f"Invalid Game Server ID. Valid Game Server IDs start with {ByoGs.ID_PREFIX}."
      return response
    # Validation for subcommands
    if self.subcommand == 'create':
      if self.name == '':
        response['msg'] = f"Missing name"
        return response
      if self.language not in ByoGs.LANGUAGES:
        response['msg'] = f"Invalid language. Valid languages are {', '.join(ByoGs.LANGUAGES)}."
        return response
      if self.platform not in ByoGs.PLATFORMS:
        response['msg'] = f"Invalid platform. Valid platforms are {', '.join(ByoGs.PLATFORMS)}."
        return response
    else:
      if self.token_parts is None:
        response['msg'] = 'Invalid token. Please reach out to your support team'
        return response
      # Check tag
      if len(self.tag.split()) > 1 or len(self.tag) > 25:
        response['msg'] = f"Tag should be a single word with maximum of 25 characters"
        return response
      if self.subcommand == 'publish-image':
        if not self.path:
          response['msg'] = f"Missing path"
          return response
        # Check path
        if not os.path.isfile(f"{self.path}/{self.dockerfile}"):
          response['msg'] = f"Unable to find {self.dockerfile} at path {self.path}"
          return response
      elif self.subcommand == 'publish-version':
        if not self.version:
          response['msg'] = f"Missing version"
          return response
        if not self.http_port:
          response['msg'] = f"Missing Ingress HTTP Port"
          return response
        pattern = r'^v\d+\.\d+\.\d+$'
        if not re.match(pattern, self.version):
          response['msg'] = f"Version should be in the format vX.X.X"
          return response
        if not self.http_port.isdigit():
          response['msg'] = f"Ingress HTTP Port should be a number"
          return response
    # Send success
    response['error'] = False
    return response

  def create(self) -> bool:
     with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Creating your game server...', total=None)
      try:
        payload = {
          "service_id": self.sid,
          "name": self.name,
          "description": self.desc,
          "platform": self.platform,
          "language": self.language,
        }
        res = requests.post(f"{self.base_url}/v1/snapser-api/byogs", json=payload, headers={'api-key': self.api_key})
        if res.ok:
          return True
        response_json = res.json()
        if "api_error_code" in response_json:
          if response_json['api_error_code'] == ERROR_SERVICE_VERSION_EXISTS:
            error('Version already exists. Please update your version and try again')
          if response_json['api_error_code'] == ERROR_TAG_NOT_AVAILABLE:
            error('Invalid tag. Please use the correct tag')
        else:
          error(f'Server error: {json.dumps(response_json, indent=2)}')
      except Exception as e:
        error("Exception: Unable to create your game server")
      return False

  def build(self) -> bool:
    # Get the data
    ecr_repo_url = self.token_parts[0]
    ecr_repo_username = self.token_parts[1]
    ecr_repo_token = self.token_parts[2]
    image_tag = f'{self.sid}.{self.tag}'
    full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
    build_platform = ByoGs.DEFAULT_BUILD_PLATFORM
    if len(self.token_parts) == 4:
      build_platform = self.token_parts[3]
    try:
      # Check dependencies
      with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
      ) as progress:
        progress.add_task(description=f'Checking dependencies...', total=None)
        try:
          subprocess.run([
            "docker", "--version"
          ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except:
          error('Docker not present')
          return False
      success('Dependencies Verified')

      # Login to Snapser Registry
      with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
      ) as progress:
        progress.add_task(description=f'Logging into Snapser Image Registry...', total=None)
        if platform == 'win32':
          response = subprocess.run([
            'docker', 'login', '--username', ecr_repo_username, '--password', ecr_repo_token, ecr_repo_url
          ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
          response = subprocess.run([
            f'echo "{ecr_repo_token}" | docker login --username {ecr_repo_username} --password-stdin {ecr_repo_url}'
          ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if response.returncode:
          error('Unable to connect to the Snapser Container Repository. Please get the latest token from the Web app')
          return False
      success('Login Successful')

      # Build your snap
      with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
      ) as progress:
        progress.add_task(description=f'Building your snap...', total=None)
        if platform == "win32":
          response = subprocess.run([
            #f"docker build --no-cache -t {tag} {path}"
            'docker', 'build', '--platform', build_platform, '-t', image_tag, self.path
          ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
          response = subprocess.run([
            #f"docker build --no-cache -t {tag} {path}"
            f"docker build --platform {build_platform} -t {image_tag} {self.path}"
          ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if response.returncode:
          error('Unable to build docker')
          return False
      success('Build Successful')

      # Tag the repo
      with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
      ) as progress:
        progress.add_task(description=f'Tagging your snap...', total=None)
        if platform == "win32":
           response = subprocess.run([
            'docker', 'tag', image_tag, full_ecr_repo_url
          ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
          response = subprocess.run([
            f"docker tag {image_tag} {full_ecr_repo_url}"
          ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if response.returncode:
          error('Unable to tag your snap')
          return False
      success('Tag Successful')

      return True
    except:
      error('CLI Error')
      return False

  def push(self) -> bool:
    ecr_repo_url = self.token_parts[0]
    image_tag = f'{self.sid}.{self.tag}'
    full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'

    # Push the image
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Pushing your snap...', total=None)
      if platform == "win32":
        response = subprocess.run([
          'docker', 'push', full_ecr_repo_url
        ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      else:
        response = subprocess.run([
          f"docker push {full_ecr_repo_url}"
        ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      if response.returncode:
        error('Unable to push your snap')
        return False
    success('Snap Upload Successful')
    return True

  # def upload_docs(self) -> bool:
  #   '''
  #     Note this step is optional hence we always respond with a True
  #   '''
  #   # Push the swagger.json
  #   with Progress(
  #     SpinnerColumn(),
  #     TextColumn("[progress.description]{task.description}"),
  #     transient=True,
  #   ) as progress:
  #     progress.add_task(description=f'Uploading your API Json...', total=None)
  #     try:
  #       dfile = open(f"{self.path}/swagger.json", "rb")
  #       test_res = requests.post(f"{self.base_url}/v1/snapser-api/byogs/{self.sid}/upload/{self.tag}/openapispec", files = {"attachment": dfile}, headers={'api-key': self.api_key})
  #       if test_res.ok:
  #         success('Uploaded Swagger.json')
  #       else:
  #         response_json = test_res.json()
  #         error(response_json['details'][0])
  #     except Exception as e:
  #       info('Unable to find swagger.json at ' + self.path + str(e))

  #   # Push the README.md
  #   with Progress(
  #     SpinnerColumn(),
  #     TextColumn("[progress.description]{task.description}"),
  #     transient=True,
  #   ) as progress:
  #     progress.add_task(description=f'Uploading your README...', total=None)
  #     try:
  #       dfile = open(f"{self.path}/README.md", "rb")
  #       test_res = requests.post(f"{self.base_url}/v1/snapser-api/byogs/{self.sid}/upload/{self.tag}/markdown", files = {"attachment": dfile}, headers={'api-key': self.api_key})
  #       if test_res.ok:
  #         success('Uploaded README.md')
  #       else:
  #         error('Unable to upload your README.md')
  #     except Exception as e:
  #       info('Unable to find README.md at ' + self.path + str(e))
  #   return True

  def publish_image(self) -> bool:
    # if not self.build() or not self.push() or not self.upload_docs():
    if not self.build() or not self.push():
      return False
    return True

  def publish_version(self) -> bool:
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Publishing your snap...', total=None)
      try:
        payload = {
          "version": self.version,
          "image_tag": self.tag,
          "http_port": self.http_port,
        }
        res = requests.post(f"{self.base_url}/v1/snapser-api/byogs/{self.sid}/versions", json=payload, headers={'api-key': self.api_key})
        if res.ok:
          return True
        response_json = res.json()
        if "api_error_code" in response_json:
          if response_json['api_error_code'] == ERROR_SERVICE_VERSION_EXISTS:
            error('Version already exists. Please update your version and try again')
          if response_json['api_error_code'] == ERROR_TAG_NOT_AVAILABLE:
            error('Invalid tag. Please use the correct tag')
        else:
          error(f'Server error: {json.dumps(response_json, indent=2)}')
      except Exception as e:
        error("Exception: Unable to publish a version for your snap")
      return False

