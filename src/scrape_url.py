import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url):
    """Fetch HTML content using BeautifulSoup"""

    response = requests.get(url)

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
        except Exception as e:
            return { 
                "error": True,
                "message": f"Failed to parse URL content. Exception: {e}",
            }

        return {"error": False, "message": text}
    else:
        return { 
            "error": True,
            "message": f"Failed to fetch the URL. Status code: {response.status_code}",
        }
