# vuln_example.py
import requests

def fetch(url):
    # insecure: disables SSL verification
    resp = requests.get(url, verify=False)
    return resp.text

def unused_function():
    x = 1  # unused variable
