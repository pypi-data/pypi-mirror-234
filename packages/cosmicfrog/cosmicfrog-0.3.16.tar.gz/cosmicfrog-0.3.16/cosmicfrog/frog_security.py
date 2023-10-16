from flask import  request, abort
from functools import wraps

import os
import requests

# Functions to facilitate API security with Optilogic platform

def __check_key__(headers):
    rv = False
    # mixed case on purpose. flask supports this for getting keys
    # since we are relying on this make it break pretty quick if
    # something changes
    try:
        app_key = headers.get("X-App-KEY", None)
        api_key = headers.get("X-Api-KEY", None)
        bearer_token = headers.get("Authorization", None)
        if app_key or api_key or bearer_token:
            base_url = os.getenv("ATLAS_API_BASE_URL")
            auth_url = f'{base_url.strip("/")}/account'

            # set up header with app key or api key depending on value set
            if app_key:
                header_key = "X-APP-KEY"
            elif api_key:
                header_key = "X-API-KEY"
            else:
                header_key = 'X-API-KEY'
            new_headers = {header_key : app_key or api_key or bearer_token.replace("Bearer ","")}

            response = requests.request('GET', auth_url, headers=new_headers)
            rv = response.status_code in [200]
    except:
        rv = False
        pass

    return rv

def GetUserAccount(headers):
    rv = None
    # mixed case on purpose. flask supports this for getting keys
    # since we are relying on this make it break pretty quick if
    # something changes
    try:
        app_key = headers.get("X-App-KEY", None)
        api_key = headers.get("X-Api-KEY", None)
        bearer_token = headers.get("Authorization", None)
        if app_key or api_key or bearer_token:
            base_url = os.getenv("ATLAS_API_BASE_URL")
        
            if not base_url:
                print("ATLAS_API_BASE_URL is not configured")
                return None
        
            auth_url = f'{base_url.strip("/")}/account'

            # set up header with app key or api key depending on value set
            if app_key:
                header_key = "X-APP-KEY"
            elif api_key:
                header_key = "X-API-KEY"
            else:
                header_key = 'X-API-KEY'
            new_headers = {header_key : app_key or api_key or bearer_token.replace("Bearer ","")}

            response = requests.request('GET', auth_url, headers=new_headers)
            rv = response.json()
    except:
        rv = None
        pass

    return rv

def GetUserToken(headers):
    rv = ""
    try:
        appkey = headers.get("X-App-KEY", None)

        if not appkey:
            token_url = os.getenv("FROG_TOKEN_URL") or "https://white-bullfrog-c368f0-token.azurewebsites.net/cosmicfrog/v0.1/frogtokenservice/Token"

            apikey = headers.get("X-API-KEY", None)
            if apikey:
                headers = {"Authorization" : f"Bearer {apikey}"}
            response = requests.request('GET', token_url, headers=headers)

            appkey = response.json()['appKey']

        rv = appkey

    except Exception as e:
        print(f"exception getting token {e}")
        rv = ""
        pass

    return rv


def IsSecured(func):
    @wraps(func)
    def is_secured(*args, **kwargs):
        if (__check_key__(request.headers)):
            return func(*args, **kwargs)
        else:
            abort(401)

    return is_secured