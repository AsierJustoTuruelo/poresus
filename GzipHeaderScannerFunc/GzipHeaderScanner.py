import io
import socks
import socket
import requests
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import pytz

class GzipHeaderScannerClass:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return {"Error": f"Could not make request to URL: {e}"}

    def extract_sensitive_data(self, headers):
        sensitive_headers = [
            "Date",
            "Server",
            "Set-Cookie",
            "X-Powered-By",
            "X-Frame-Options",
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options"
        ]
        extracted_data = {}
        try:
            for header in sensitive_headers:
                if header in headers:
                    extracted_data[header] = headers[header]
        except Exception as e:
            extracted_data["Error"] = f"Error extracting headers: {e}"
        return extracted_data

    def convert_server_time(self, date_str):
        try:
            server_time = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            return server_time
        except ValueError as e:
            return {"Error": f"Error converting server time: {e}"}

    def estimate_location(self, server_time):
        try:
            if server_time is None:
                return "Unknown"

            # Convert server time to UTC if not already in UTC
            if server_time.tzinfo is None:
                server_time = pytz.utc.localize(server_time)

            server_hour = server_time.hour

            if 0 <= server_hour < 6:
                return "Oceanía"
            elif 6 <= server_hour < 12:
                return "Asia"
            elif 12 <= server_hour < 18:
                return "Europa"
            else:
                return "América"
        except Exception as e:
            return {"Error": f"Error estimating location: {e}"}

    def scan_gzip_headers(self):
        results = {}
        try:
            for url in tqdm(self.urls, desc="Scanning URLs for GZIP header"):
                response = self.make_tor_request(url)
                if isinstance(response, dict) and "Error" in response:
                    results[url] = response
                    continue

                headers = response.headers

                gzip_enabled = 'Content-Encoding' in headers and headers['Content-Encoding'] == 'gzip'

                extracted_data = self.extract_sensitive_data(headers)
                server_time_str = extracted_data.get("Date")
                if "Error" in extracted_data:
                    results[url] = extracted_data
                    continue

                server_time = self.convert_server_time(server_time_str) if server_time_str else None
                if isinstance(server_time, dict) and "Error" in server_time:
                    results[url] = server_time
                    continue

                estimated_location = self.estimate_location(server_time)
                if isinstance(estimated_location, dict) and "Error" in estimated_location:
                    results[url] = estimated_location
                    continue

                results[url] = {
                    "GZIP enabled": gzip_enabled,
                    "Header Sensitive Data": extracted_data,
                    "Estimated Location": estimated_location
                }

            return results

        except Exception as e:
            return {"Error": f"Error scanning GZIP headers: {e}"}

if __name__ == "__main__":
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html',
        'a',
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/',
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_bruteforce/prueba_bruteforce.html',
        'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/'
    ]
    scanner = GzipHeaderScannerClass(urls)
    results_json = scanner.scan_gzip_headers()
    print(results_json)
