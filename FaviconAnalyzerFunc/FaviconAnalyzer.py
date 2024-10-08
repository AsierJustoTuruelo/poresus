import requests
import socks
import socket
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import hashlib
import mmh3
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import base64
import re
import json
from tqdm import tqdm

class FaviconAnalyzerClass:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {}  # Dictionary to store hash results

    def make_tor_request(self, url):
        try:
            # Set the SOCKS5 proxy to the local Tor instance
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            # Make the request through the Tor network
            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            # If there's an error, store the error message in the results dictionary for the URL
            self.results[url] = f"Error making request through Tor, URL not accessible: {e}"
            return None

    def download_favicon(self):
        # Iterate over the list of URLs with a progress bar
        for url in tqdm(self.urls, desc="Scanning URLs for Favicons"):
            # Make a request to the URL through Tor
            response = self.make_tor_request(url)
            if response:
                try:
                    # Parse the HTML content of the response
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Find the link tag with the rel attribute set to 'icon'
                    link_tag = soup.find('link', rel='icon')
                    if link_tag:
                        # Construct the full URL for the favicon
                        favicon_url = urljoin(url, link_tag.get('href'))
                        # Make a request to the favicon URL through Tor
                        favicon_response = self.make_tor_request(favicon_url)
                        if favicon_response and favicon_response.status_code == 200:
                            favicon_content = favicon_response.content
                            
                            # Steps 1 to 3: Convert to base64 and add newlines every 76 characters
                            b64 = base64.b64encode(favicon_content)
                            utf8_b64 = b64.decode('utf-8')
                            with_newlines = re.sub("(.{76}|$)", "\\1\n", utf8_b64, 0, re.DOTALL)
                            
                            # Calculate MMH3 hash
                            mmh3_hash = mmh3.hash(with_newlines.encode())

                            # Calculate SHA-256 hash
                            sha256_hash = hashlib.sha256(favicon_content).hexdigest()

                            # Calculate MD5 hash
                            md5_hash = hashlib.md5(favicon_content).hexdigest()

                            # Store the hashes in the results dictionary for the URL
                            self.results[url] = {
                                "MMH3": mmh3_hash,
                                "SHA-256": sha256_hash,
                                "MD5": md5_hash
                            }
                        else:
                            self.results[url] = "Failed to download favicon"
                    else:
                        self.results[url] = "Failed to find favicon link tag"
                except Exception as e:
                    # If there's an error processing the URL, store the error message
                    self.results[url] = f"Error processing URL: {e}"
            else:
                # If no response is received, store an error message
                self.results[url] = "Error URL not accessible through Tor."

        # Return the results dictionary containing the hashes or error messages
        return self.results


if __name__ == "__main__":
    urls = ["http://53d5skw4ypzku4bfq2tk2mr3xh5yqrzss25sooiubmjz67lb3gdivcad.onion/","https://www.reddittorjg6rue252oqsxryoxengawnmo46qy4kyii5wtqnwfj4ooad.onion/?rdt=41078", "a"]
    downloader = FaviconAnalyzerClass(urls)
    hashes = downloader.download_favicon()
    if hashes:
        print(json.dumps(hashes, indent=4))
