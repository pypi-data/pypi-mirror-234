import requests
import typer
from snapctl.config.constants import HTTP_NOT_FOUND, HTTP_FORBIDDEN, HTTP_UNAUTHORIZED
from snapctl.utils.echo import error, success

def get_composite_token(base_url:str, api_key: str, action: str, params: object) -> str:
  # Exhange the api_key for a token
  payload: object = {
    'action': action,
    'params': params
  }
  res = requests.post(f"{base_url}/v1/snapser-api/composite-token", headers={'api-key': api_key}, json=payload)
  if not res.ok:
    if res.status_code == HTTP_NOT_FOUND:
      error('Service ID is invalid.')
    elif res.status_code == HTTP_UNAUTHORIZED:
      error('API Key verification failed. Your API Key may have expired. Please generate a new one from the Snapser dashboard.')
    elif res.status_code == HTTP_FORBIDDEN:
      error('Permission denied. Your role has been revoked. Please contact your administrator.')
    else:
      error(f'Failed to validate API Key. Error: {res.text}')
    raise typer.Exit()
  success('API Key validated')
  return res.json()['token']

