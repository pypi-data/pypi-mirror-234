import json
import requests
from python_graphql_client import GraphqlClient

from .login import get_bearer_auth_base, get_bearer_authorization_header_value


def retrieve_graphql(url=None, query=None, variables=None, use_auth=None, log_prefix='Do a GraphQL query'):
    auth = get_bearer_auth_base() if use_auth else None
    client = GraphqlClient(endpoint=url, auth=auth)
    prefix = f"{log_prefix} to {url}"
    print(prefix, 'variables', variables)
    response = client.execute(query, variables)
    print(prefix, 'response', response)
    return response


def retrieve_http(url=None, method=requests.get, log_prefix='Do a HTTP GET request', 
                  use_default_headers=True, use_auth=False, extra_headers={},
                  payload=None):
    prefix = f"{log_prefix} to {url}"

    def get_default_headers():
        headers = {}
        if use_default_headers:
            headers.update({
                'Content-Type': 'application/json'
            })
            if use_auth:
                headers['Authorization'] = get_bearer_authorization_header_value()
        headers.update(extra_headers)
        print(prefix, 'headers', headers)
        return headers

    print(prefix, 'payload', payload)
    response = method(
        url=url,
        data=None if payload is None else json.dumps(payload),
        headers=get_default_headers(),
    )
    print(prefix, 'response', response)
    data = response.json()
    print(prefix, 'JSON response', data)
    return data
