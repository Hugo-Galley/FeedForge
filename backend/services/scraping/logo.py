import requests

def get_site_logo(domain: str, size: int):
    response = requests.get(f"https://www.google.com/s2/favicons?domain={domain}.com&sz={size}")
    return response.status_code

