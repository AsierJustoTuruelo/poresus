"""
Pruebas a realizar:

1. Identificar el tipo de servidor que corre y su version. PUede ser en el header o habria que ver otros metodos.
2. Identificar puertos abiertos en el servidor.
3. Identificar si el html contiene mails, telefonos, direcciones
4. Identificar si el html contiene direcciones bitcoin
5. Identificar si el html contiene direcciones de redes sociales
6. Identificar si el html contiene direcciones de google analytics
7. Identificar si se pueden descargar imagenes, videos, pdfs, etc.

"""
"""

instalar mmh3 --> pip install mmh3
instalar mutagen --> pip install mutagen
instalar stem --> pip install stem

"""
import json
from bitcoin_scanner.bitcoin_scanner import BitcoinAddressExtractor
from brute_force.brute_force import AdvancedBruteForceScanner
from etag.etag import ETagScanner
from favicon_ico.favicon_ico import OnionFaviconDownloader
from file_input.file_input import FileUploadValidator
from files_hashes.files_hashes import OnionFileAnalyzer
from files_metadata.binary_metadata import BinaryFileScanner
from files_metadata.excel_metadata import OnionExcelScanner
from files_metadata.gif_metadata import OnionGifScanner
from files_metadata.pdf_metadata import OnionPdfScanner
from files_metadata.ppt_metadata import OnionPptScanner
#from files_metadata.txt_metadata import
from files_metadata.video_metadata import OnionMediaScanner
from files_metadata.word_metadata import OnionWordScanner
from google_services.google_services import GoogleIDsExtractor
from gzip_compression.gzip_compression import GzipHeaderScanner
from hostname.hostname import HostnameHackingScanner
from html_info.html_info import HtmlInfo
from images_metadata.images_metadata import OnionImageScanner
from mail_scanner.mail_scanner import HtmlEmailExtractor
from otherservices_scanner.otherservices_scanner import OnionServiceAnalyzer
from phone_scanner.phone_scanner import HtmlPhoneExtractor
from php_server.php_server import PHPServerInfoScanner
from server_info.server_info import InformacionServidor
from server_status.server_status import ServerStatusChecker
from socialnet_scanner.socialnet_scanner import RedesSocialesScanner
from sqli.sqli_scanner import AdvancedSqlInjectionScanner
from validacion_input.validacionInput import ValidacionInput
from xss.xss_scanner import XSSScanner
#from xml.xml_injector import XXEScanner

import argparse
import json
usernames_file = "./dics/usernames.txt"
passwords_file = "./dics/rockyou.txt"

def show_logo():
    logo = """⠀⠀⠀⠀⠀⠀
    ██████╗░░█████╗░██████╗░███████╗░██████╗░██╗░░░██╗░██████╗
    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝░██║░░░██║██╔════╝
    ██████╔╝██║░░██║██████╔╝█████╗░░╚█████╗░░██║░░░██║╚█████╗░
    ██╔═══╝░██║░░██║██╔══██╗██╔══╝░░░╚═══██╗░██║░░░██║░╚═══██╗
    ██║░░░░░╚█████╔╝██║░░██║███████╗██████╔╝╚ ██████╔╝██████╔╝
    ╚═╝░░░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░░ ╚═════╝░╚═════╝░
    """
    print(logo)



def main():
    # Mostrar el logo al inicio
    show_logo()

    # Crear un analizador de argumentos
    parser = argparse.ArgumentParser(description="Run specified scanners")

    # Agregar argumentos para cada escáner
    parser.add_argument("-b", "--bitcoin", action="store_true", help="Run Bitcoin address extractor")
    parser.add_argument("-bf", "--bruteforce", action="store_true", help="Run Brute Force scanner")
    parser.add_argument("-e", "--etag", action="store_true", help="Run ETag scanner")
    parser.add_argument("-f", "--favicon", action="store_true", help="Run Favicon downloader")
    parser.add_argument("-fi", "--fileinput", action="store_true", help="Run File Input validator")

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # Ejecutar los escáneres según los argumentos proporcionados
    results = {}
    if args.bitcoin:
        # Ejecutar Bitcoin address extractor
        bitcoin_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/bitcoin_address/bitcoin_adress.html"]
        bitcoin_extractor = BitcoinAddressExtractor(bitcoin_urls)
        bitcoin_addresses = bitcoin_extractor.fetch_html_and_extract_addresses()
        results["Bitcoin Results"] = {
            "Bitcoin Addresses": bitcoin_addresses if bitcoin_addresses else "No se encontraron direcciones Bitcoin."
        }
    
    if args.bruteforce:
        # Ejecutar Brute Force scanner
        brute_force_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_bruteforce/prueba_bruteforce.html"]
        brute_force_scanner = AdvancedBruteForceScanner(brute_force_urls)
        brute_force_results_json = json.loads(brute_force_scanner.brute_force(usernames_file, passwords_file))
        results["Brute Force Results"] = {
            "Brute Force Results": brute_force_results_json
        }
    
    if args.etag:
        # Ejecutar ETag scanner
        etag_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        etag_scanner = ETagScanner(etag_urls)
        etag_results_json = json.loads(etag_scanner.scan_etags())
        results["ETag Results"] = {
            "ETag Results": etag_results_json
        }
    
    if args.favicon:
        # Ejecutar Favicon downloader
        favicon_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/favicon-ico/favicon-ico.html"]
        favicon_downloader = OnionFaviconDownloader(favicon_urls)
        favicon_hashes = favicon_downloader.download_favicon()
        if favicon_hashes:
            results["Favicon Results"] = {
                "Favicon Hashes": favicon_hashes
            }
    
    if args.fileinput:
        # Ejecutar File Input validator
        file_input_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_file/index.html"]
        file_input_validator = FileUploadValidator(file_input_urls, tor_proxy="socks5h://127.0.0.1:9050")
        file_input_results = file_input_validator.run_tests()
        results["File Input Results"] = file_input_results

      
    # Imprimir los resultados en formato JSON
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()