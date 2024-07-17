import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
from tqdm import tqdm

class DatabaseTypeScanner:
    def __init__(self, urls):
        self.session = requests.Session()
        self.proxies = {
            'http': f'socks5h://{"127.0.0.1"}:{9050}',
            'https': f'socks5h://{"127.0.0.1"}:{9050}'
        }
        self.urls = urls

    def is_accessible(self, url):
        try:
            response = self.session.head(url, proxies=self.proxies)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def detect_database_type(self, url):
        res = None  # Initialize res
        try:
            if not self.is_accessible(url):
                return "URL not accessible."

            response = self.session.get(url, proxies=self.proxies, allow_redirects=True)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            form = soup.find('form')

            if not form:
                return 'No form found'

            form_action = form.get('action')
            form_method = form.get('method', '').lower()

            # Send POST or GET request to the PHP file and receive response
            if form_method == 'post':
                res = self.session.post(urljoin(url, form_action), data={}, proxies=self.proxies, allow_redirects=True)
            elif form_method == 'get':
                res = self.session.get(urljoin(url, form_action), params={}, proxies=self.proxies, allow_redirects=True)

            # List of error patterns associated with different database types
            database_errors = {
                'MySQL': r"SQLSTATE\[.*?\] \[.*?\] Access denied for user .*? \(using password: YES\)",
                'PostgreSQL': r"SQLSTATE\[.*?\] \[.*?\] FATAL:  password authentication failed",
                'SQL Server': r"Login failed for user .*?",
                'SQLite': r"unable to open database"
            }

            # Iterate over error patterns and check if any is present in the server response
            for db_type, error_pattern in database_errors.items():
                if res and re.search(error_pattern, res.text, re.IGNORECASE):
                    return db_type

            return 'Unknown'

        except requests.exceptions.RequestException as e:
            return f"Not accessible: {str(e)}"

    def scan_urls(self):
        results = {}

        for url in tqdm(self.urls, desc="Scanning URLs for Database Type"):
            if not self.is_accessible(url):
                results[url] = "URL not accessible"
                continue
            database_type = self.detect_database_type(url)
            results[url] = database_type

        return results


# Example usage
if __name__ == "__main__":
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_dbtype/prueba_dbtype.html',
        'a',
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/"
        # Add more URLs here
    ]

    scanner = DatabaseTypeScanner(urls)
    results = scanner.scan_urls()

    print(json.dumps(results, indent=4))
