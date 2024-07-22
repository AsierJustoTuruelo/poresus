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
from favicon_ico.favicon_ico import FaviconAnalyzer
from file_input.file_input import FileUploadValidator
from files_hashes.files_hashes import FileAnalyzer
from files_metadata.binary_metadata import BinaryFileMetadataExtractor
from files_metadata.excel_metadata import ExcelMetadataExtractor
from files_metadata.gif_metadata import GifMdataExtractor
from files_metadata.pdf_metadata import PdfMetadataExtractor
from files_metadata.ppt_metadata import PptMetadataExtractor
from files_metadata.txt_metadata import TxtMetadataExtractor
from files_metadata.video_metadata import MediaMetadataExtractor
from files_metadata.word_metadata import WordMetadataExtractor
from google_services.google_services import GoogleIDsExtractor
from gzip_compression.gzip_compression import GzipHeaderScanner
from hostname.hostname import HostnameScanner
from html_info.html_info import HtmlInfoExtractor
from images_metadata.images_metadata import ImageMetadataExtractor
from mail_scanner.mail_scanner import HtmlEmailExtractor
from otherservices_scanner.otherservices_scanner import OtherServicesAnalyzer
from phone_scanner.phone_scanner import HtmlPhoneExtractor
from php_server.php_server import PHPServerInfoAnalyzer
from server_info.server_info import InformacionServidor
from server_status.server_status import ServerStatusAnalyzer
from socialnet_scanner.socialnet_scanner import SocialMediaExtractor
from sqli.sqli_scanner import AdvancedSqlInjectionScanner
from validacion_input.validacionInput import InputValidator
from xss.xss_scanner import XSSScanner
from database_type.database_type import DatabaseTypeScanner
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
    ╚═╝░░░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░░ ╚═════╝░╚═════╝░ by AJ
    """
    print(logo)

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls


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
    parser.add_argument("-fh", "--filehashes", action="store_true", help="Run File Hashes scanner")
    parser.add_argument("-bm", "--binarymetadata", action="store_true", help="Run Binary Metadata scanner")
    parser.add_argument("-em", "--excelmetadata", action="store_true", help="Run Excel Metadata scanner")
    parser.add_argument("-gm", "--gifmetadata", action="store_true", help="Run GIF Metadata scanner")
    parser.add_argument("-pm", "--pdfmetadata", action="store_true", help="Run PDF Metadata scanner")
    parser.add_argument("-pwm", "--pptmetadata", action="store_true", help="Run PPT Metadata scanner")
    parser.add_argument("-wm", "--wordmetadata", action="store_true", help="Run Word Metadata scanner")
    parser.add_argument("-mm", "--mediametadata", action="store_true", help="Run Media Metadata scanner")
    parser.add_argument("-tm", "--txtmetadata", action="store_true", help="Run Text Metadata scanner")
    parser.add_argument("-im", "--imagemetadata", action="store_true", help="Run Image Metadata scanner")
    parser.add_argument("-gs", "--googleids", action="store_true", help="Run Google IDs extractor")
    parser.add_argument("-gh", "--gzipheader", action="store_true", help="Run Gzip Header scanner")
    parser.add_argument("-hh", "--hostname", action="store_true", help="Run Hostname Hacking scanner")
    parser.add_argument("-hi", "--htmlinfo", action="store_true", help="Run HTML Info scanner")
    parser.add_argument("-me", "--mailextractor", action="store_true", help="Run Mail extractor")
    parser.add_argument("-os", "--otherservices", action="store_true", help="Run Other Services scanner")
    parser.add_argument("-ps", "--phonescanner", action="store_true", help="Run Phone scanner")
    parser.add_argument("-php", "--phpserver", action="store_true", help="Run PHP Server Info scanner")
    parser.add_argument("-si", "--serverinfo", action="store_true", help="Run Server Info scanner")
    parser.add_argument("-ss", "--serverstatus", action="store_true", help="Run Server Status checker")
    parser.add_argument("-rs", "--socialnets", action="store_true", help="Run Social Networks scanner")
    parser.add_argument("-sqli", "--sqlinjection", action="store_true", help="Run SQL Injection scanner")
    parser.add_argument("-vi", "--InputValidator", action="store_true", help="Run Validacion Input scanner")
    parser.add_argument("-xss", "--xss", action="store_true", help="Run XSS scanner")
    #parser.add_argument("-xxe", "--xxe", action="store_true", help="Run XXE scanner")
    parser.add_argument("-db", "--database", action="store_true", help="Run Data Base scanner")
    parser.add_argument("-all", "--all", action="store_true", help="Run all scanners")

    
    # Agregar un argumento para el archivo de texto con las URL
    parser.add_argument("url_file", help="Path to a file containing URLs, one per line")
    
    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # Lee las URL desde el archivo
    urls = read_urls_from_file(args.url_file)

    # Ejecutar los escáneres según los argumentos proporcionados
    results = {}
    if args.bitcoin:
        # Ejecutar Bitcoin address extractor
        bitcoin_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/bitcoin_address/bitcoin_adress.html", "http://kz62gxxlegswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/bitcoin_address/"]
        bitcoin_extractor = BitcoinAddressExtractor(urls)
        bitcoin_addresses = bitcoin_extractor.extract_bitcoin_addresses()
        results["Bitcoin Results"] = {
            "Bitcoin Addresses": bitcoin_addresses if bitcoin_addresses else "No se encontraron direcciones Bitcoin."
        }
    
    if args.bruteforce:
        # Ejecutar Brute Force scanner
        brute_force_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_bruteforce/prueba_bruteforce.html", "http://kz62gxxl6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_bruteforce/prueba_bruteforce.html"]
        brute_force_scanner = AdvancedBruteForceScanner(urls)
        brute_force_results_json = json.loads(brute_force_scanner.brute_force(usernames_file, passwords_file))
        results["Brute Force Results"] = {
            "Brute Force Results": brute_force_results_json
        }
    
    if args.etag:
        # Ejecutar ETag scanner
        etag_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/"]
        etag_scanner = ETagScanner(urls)
        etag_results_json = etag_scanner.scan_etags()
        results["ETag Results"] = {
            "ETags": etag_results_json
        }
    
    if args.favicon:
        # Ejecutar Favicon downloader
        favicon_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/favicon-ico/favicon-ico.html","http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/" ,"http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        favicon_downloader = FaviconAnalyzer(urls)
        favicon_hashes = favicon_downloader.download_favicon()
        if favicon_hashes:
            results["Favicon Results"] = {
                "Favicon Hashes": favicon_hashes
            }
    
    if args.fileinput:
        # Ejecutar File Input validator
        file_input_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_file/index.html", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/"]
        file_input_validator = FileUploadValidator(urls)
        file_input_validator.run_tests()
        results["File Input Results"] = file_input_validator.results
    
    if args.filehashes:
        # Ejecutar File Hashes scanner
        file_hashes_urls = ["http://z62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        file_hashes_scanner = FileAnalyzer(urls)
        file_hashes_results = file_hashes_scanner.analyze_files()
        results["File Hashes Results"] = {
            "File Hashes Results": file_hashes_results
        }
    
    if args.binarymetadata:
        # Ejecutar Binary Metadata scanner
        binary_metadata_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html']
        binary_metadata_scanner = BinaryFileMetadataExtractor(urls)
        binary_metadata_results = binary_metadata_scanner.scan_binary_files()
        results["Binary Metadata Results"] = {
            "Binary Metadata Results": binary_metadata_results
        }
    
    if args.excelmetadata:
        # Ejecutar Excel Metadata scanner
        excel_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        excel_metadata_scanner = ExcelMetadataExtractor(urls)
        excel_metadata_results = excel_metadata_scanner.scan_excel_files()
        results["Excel Metadata Results"] = {
            "Excel Metadata Results": excel_metadata_results
        }
    
    if args.gifmetadata:
        # Ejecutar GIF Metadata scanner
        gif_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        gif_metadata_scanner = GifMdataExtractor(urls)
        gif_metadata_results = gif_metadata_scanner.scan_gif_files()
        results["GIF Metadata Results"] = {
            "GIF Metadata Results": gif_metadata_results
        }
    
    if args.pdfmetadata:
        # Ejecutar PDF Metadata scanner
        pdf_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        pdf_metadata_scanner = PdfMetadataExtractor(urls)
        pdf_metadata_results = pdf_metadata_scanner.scan_pdf_files()
        results["PDF Metadata Results"] = {
            "PDF Metadata Results": pdf_metadata_results
        }
    
    if args.pptmetadata:
        # Ejecutar PPT Metadata scanner
        ppt_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        ppt_metadata_scanner = PptMetadataExtractor(urls)
        ppt_metadata_results = ppt_metadata_scanner.scan_ppt_files()
        results["PPT Metadata Results"] = {
            "PPT Metadata Results": ppt_metadata_results
        }
    
    if args.wordmetadata:
        # Ejecutar Word Metadata scanner
        word_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        word_metadata_scanner = WordMetadataExtractor(urls)
        word_metadata_results = word_metadata_scanner.scan_word_files()
        results["Word Metadata Results"] = {
            "Word Metadata Results": word_metadata_results
        }
    
    if args.mediametadata:
        # Ejecutar Media Metadata scanner
        media_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        media_metadata_scanner = MediaMetadataExtractor(urls)
        media_metadata_results = media_metadata_scanner.scan_media_files()
        results["Media Metadata Results"] = {
            "Media Metadata Results": media_metadata_results
        }
    
    if args.txtmetadata:
        # Ejecutar Text Metadata scanner
        text_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        text_metadata_scanner = TxtMetadataExtractor(urls)
        text_metadata_results = text_metadata_scanner.scan_text_files()
        results["Text Metadata Results"] = {
            "Text Metadata Results": text_metadata_results
        }
    
    if args.imagemetadata:
        # Ejecutar Image Metadata scanner
        image_metadata_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html']
        image_metadata_scanner = ImageMetadataExtractor(urls)  # <- Aquí debería ser image_metadata_urls
        image_metadata_results = image_metadata_scanner.scan_images()
        results["Image Metadata Results"] = {
            "Image Metadata Results": image_metadata_results
        }
    
    if args.googleids:
        # Ejecutar Google IDs extractor
        google_ids_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/google_ap/google_ap.html']
        google_ids_extractor = GoogleIDsExtractor(urls)
        google_ids = google_ids_extractor.scan_google_services()
        results["Google IDs Results"] = {
            "Google IDs": google_ids if google_ids else "No se encontraron IDs de Google."
        }
    
    if args.gzipheader:
        # Ejecutar Gzip Header scanner
        gzip_header_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/"]
        gzip_header_scanner = GzipHeaderScanner(urls)
        gzip_header_results = gzip_header_scanner.scan_gzip_headers()
        results["Gzip Header Results"] = {
            "Gzip Header Results": gzip_header_results
        }
    
    if args.hostname:
        # Ejecutar Hostname Hacking scanner
        hostname_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_hostname/prueba_hostname.html", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/"]
        hostname_scanner = HostnameScanner(urls)
        hostname_results = hostname_scanner.scan_hostnames()
        results["Hostname Results"] = {
            "Hostname Results": hostname_results
        }
    
    if args.htmlinfo:
        # Ejecutar HTML Info scanner
        html_info_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        html_info_scanner = HtmlInfo(urls)
        html_info_results = html_info_scanner.analyze_html()
        results["HTML Info Results"] = {
            "HTML Info Results": html_info_results
        }
    
    if args.mailextractor:
        # Ejecutar Mail extractor
        mail_extractor_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/mail/mail.html"]
        mail_extractor = HtmlEmailExtractor(urls)
        mail_addresses = mail_extractor.extract_emails()
        results["Mail Results"] = {
            "Mail Addresses": mail_addresses if mail_addresses else "No se encontraron direcciones de correo."
        }
    
    if args.otherservices:
        # Ejecutar Other Services scanner
        other_services_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/services/services.html"]
        other_services_scanner = OtherServicesAnalyzer(urls)
        other_services_results = other_services_scanner.analyze_services()
        results["Other Services Results"] = {
            "Other Services Results": other_services_results
        }
    
    if args.phonescanner:
        # Ejecutar Phone scanner
        phone_scanner_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/phone/phone.html"]
        phone_scanner = HtmlPhoneExtractor(urls)
        phone_numbers = phone_scanner.extract_phone_numbers()
        results["Phone Results"] = {
            "Phone Numbers": phone_numbers if phone_numbers else "No se encontraron números de teléfono."
        }
    
    if args.phpserver:
        # Ejecutar PHP Server Info scanner
        php_server_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        php_server_scanner = PHPServerInfoAnalyzer(urls)
        php_server_info = php_server_scanner.scan_php_server_info()
        results["PHP Server Results"] = {
            "PHP Server Info": php_server_info
        }
    
    if args.serverinfo:
        # Ejecutar Server Info scanner
        server_info_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        server_info_scanner = InformacionServidor(urls)
        server_info = server_info_scanner.get_server_info()
        results["Server Info Results"] = {
            "Server Info": server_info
        }
    
    if args.serverstatus:
        # Ejecutar Server Status checker
        server_status_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        server_status_checker = ServerStatusAnalyzer(urls)
        server_status = server_status_checker.check_servers_status()
        results["Server Status Results"] = {
            "Server Status": server_status
        }
    
    if args.socialnets:
        # Ejecutar Social Networks scanner
        socialnets_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/social/social.html"]
        socialnets_scanner = SocialMediaExtractor(urls)
        socialnets_results = socialnets_scanner.extract_social_networks()
        results["Social Networks Results"] = {
            "Social Networks": socialnets_results if socialnets_results else "No se encontraron redes sociales."
        }
    
    if args.sqlinjection:
        # Ejecutar SQL Injection scanner
        sqli_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_sqli/prueba_sqli.html"]
        sqli_scanner = AdvancedSqlInjectionScanner()
        sqli_results = sqli_scanner.scan_sql_injection(urls)
        results["SQL Injection Results"] = {
            "SQL Injection Results": sqli_results
        }
    
    if args.InputValidator:
        # Ejecutar Validacion Input scanner
        validacion_input_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_validacion_input/prueba_validacion_input.html"]
        validacion_input_scanner = InputValidator(urls)
        validacion_input_results = validacion_input_scanner.run_tests()
        results["Validacion Input Results"] = validacion_input_results
    
    if args.xss:
        # Ejecutar XSS scanner
        xss_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_xss/prueba_xss.html"]
        xss_scanner = XSSScanner(urls)
        xss_results = xss_scanner.scan_xss()
        results["XSS Results"] = {
            "XSS Results": xss_results
        }
    
    if args.database:
        # Ejecutar Data Base scanner
        database_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_dbtype/prueba_dbtype.html", "a", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/"]
        database_scanner = DatabaseTypeScanner(urls)
        results["Database Results"] = database_scanner.scan_urls()
    
    if args.all:
        # Ejecutar todos los escáneres
        bitcoin_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/bitcoin_address/bitcoin_adress.html", "http://kz62gxxlegswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/bitcoin_address/"]
        bitcoin_extractor = BitcoinAddressExtractor(urls)
        bitcoin_addresses = bitcoin_extractor.extract_bitcoin_addresses()
        results["Bitcoin Results"] = {
            "Bitcoin Addresses": bitcoin_addresses if bitcoin_addresses else "No se encontraron direcciones Bitcoin."
        }
        
        brute_force_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_bruteforce/prueba_bruteforce.html", "http://kz62gxxl6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_bruteforce/prueba_bruteforce.html"]
        brute_force_scanner = AdvancedBruteForceScanner(urls)
        brute_force_results_json = json.loads(brute_force_scanner.brute_force(usernames_file, passwords_file))
        results["Brute Force Results"] = {
            "Brute Force Results": brute_force_results_json
        }
        
        etag_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/"]
        etag_scanner = ETagScanner(urls)
        etag_results_json = etag_scanner.scan_etags()
        results["ETag Results"] = {
            "ETags": etag_results_json
        }
        favicon_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/favicon-ico/favicon-ico.html","http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/" ,"http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        favicon_downloader = FaviconAnalyzer(urls)
        favicon_hashes = favicon_downloader.download_favicon()
        if favicon_hashes:
            results["Favicon Results"] = {
                "Favicon Hashes": favicon_hashes
            }

        file_input_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_file/index.html", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/"]
        file_input_validator = FileUploadValidator(urls)
        file_input_validator.run_tests()
        results["File Input Results"] = file_input_validator.results

        file_hashes_urls = ["http://z62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        file_hashes_scanner = FileAnalyzer(urls)
        file_hashes_results = file_hashes_scanner.analyze_files()
        results["File Hashes Results"] = {
            "File Hashes Results": file_hashes_results
        }

        binary_metadata_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html']
        binary_metadata_scanner = BinaryFileMetadataExtractor(urls)
        binary_metadata_results = binary_metadata_scanner.scan_binary_files()
        results["Binary Metadata Results"] = {
            "Binary Metadata Results": binary_metadata_results
        }

        excel_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        excel_metadata_scanner = ExcelMetadataExtractor(urls)
        excel_metadata_results = excel_metadata_scanner.scan_excel_files()
        results["Excel Metadata Results"] = {
            "Excel Metadata Results": excel_metadata_results
        }

        gif_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        gif_metadata_scanner = GifMdataExtractor(urls)
        gif_metadata_results = gif_metadata_scanner.scan_gif_files()
        results["GIF Metadata Results"] = {
            "GIF Metadata Results": gif_metadata_results
        }

        pdf_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        pdf_metadata_scanner = PdfMetadataExtractor(urls)
        pdf_metadata_results = pdf_metadata_scanner.scan_pdf_files()
        results["PDF Metadata Results"] = {
            "PDF Metadata Results": pdf_metadata_results
        }

        ppt_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        ppt_metadata_scanner = PptMetadataExtractor(urls)
        ppt_metadata_results = ppt_metadata_scanner.scan_ppt_files()
        results["PPT Metadata Results"] = {
            "PPT Metadata Results": ppt_metadata_results
        }

        word_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        word_metadata_scanner = WordMetadataExtractor(urls)
        word_metadata_results = word_metadata_scanner.scan_word_files()
        results["Word Metadata Results"] = {
            "Word Metadata Results": word_metadata_results
        }

        media_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        media_metadata_scanner = MediaMetadataExtractor(urls)
        media_metadata_results = media_metadata_scanner.scan_media_files()
        results["Media Metadata Results"] = {
            "Media Metadata Results": media_metadata_results
        }

        image_metadata_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html']
        image_metadata_scanner = ImageMetadataExtractor(urls)
        image_metadata_results = image_metadata_scanner.scan_images()
        results["Image Metadata Results"] = {
            "Image Metadata Results": image_metadata_results
        }

        google_ids_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/google_ap/google_ap.html']
        google_ids_extractor = GoogleIDsExtractor(urls)
        google_ids = google_ids_extractor.scan_google_services()
        results["Google IDs Results"] = {
            "Google IDs": google_ids if google_ids else "No se encontraron IDs de Google."
        }

        gzip_header_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/"]
        gzip_header_scanner = GzipHeaderScanner(urls)
        gzip_header_results = gzip_header_scanner.scan_gzip_headers()
        results["Gzip Header Results"] = {
            "Gzip Header Results": gzip_header_results
        }

        hostname_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_hostname/prueba_hostname.html", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/"]
        hostname_scanner = HostnameScanner(urls)
        hostname_results = hostname_scanner.scan_hostnames()
        results["Hostname Results"] = {
            "Hostname Results": hostname_results
        }

        html_info_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        html_info_scanner = HtmlInfo(urls)
        html_info_results = html_info_scanner.analyze_html()
        results["HTML Info Results"] = {
            "HTML Info Results": html_info_results
        }

        mail_extractor_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/mailweb/mailweb.html"]
        mail_extractor = HtmlEmailExtractor(urls)
        mail_addresses = mail_extractor.extract_emails()
        results["Mail Results"] = {
            "Mail Addresses": mail_addresses if mail_addresses else "No se encontraron direcciones de correo."
        }

        other_services_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/otherservices/otherservices.html"]
        other_services_scanner = OtherServicesAnalyzer(urls)
        other_services_results = other_services_scanner.analyze_services()
        results["Other Services Results"] = {
            "Other Services Results": other_services_results
        }

        phone_scanner_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/phone_numbers/phone_numbers.html"]
        phone_scanner = HtmlPhoneExtractor(urls)
        phone_numbers = phone_scanner.extract_phone_numbers()
        results["Phone Results"] = {
            "Phone Numbers": phone_numbers
        }

        php_server_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/php_info/php_info.html"]
        php_server_scanner = PHPServerInfoAnalyzer(urls)
        php_server_info = php_server_scanner.scan_php_server_info()
        results["PHP Server Results"] = {
            "PHP Server Info": php_server_info
        }

        server_info_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/php_info/php_info.html"]
        server_info_scanner = InformacionServidor(urls)
        server_info = server_info_scanner.get_server_info()
        results["Server Info Results"] = {
            "Server Info": server_info
        }

        server_status_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/"]
        server_status_checker = ServerStatusAnalyzer(urls)
        server_status = server_status_checker.check_servers_status()
        results["Server Status Results"] = {
            "Server Status": server_status
        }

        socialnets_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/social/social.html"]
        socialnets_scanner = SocialMediaExtractor(urls)
        socialnets_results = socialnets_scanner.extract_social_networks()
        results["Social Networks Results"] = {
            "Social Networks": socialnets_results if socialnets_results else "No se encontraron redes sociales."
        }

        sqli_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_sqli/prueba_sqli.html"]
        sqli_scanner = AdvancedSqlInjectionScanner()
        sqli_results = sqli_scanner.scan_sql_injection(urls)
        results["SQL Injection Results"] = {
            "SQL Injection Results": sqli_results
        }

        validacion_input_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_validacion_input/prueba_validacion_input.html"]
        validacion_input_scanner = InputValidator(urls)
        validacion_input_results = validacion_input_scanner.run_tests()
        results["Validacion Input Results"] = validacion_input_results

        xss_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_xss/prueba_xss.html"]
        xss_scanner = XSSScanner(urls)
        xss_results = xss_scanner.scan_xss()
        results["XSS Results"] = {
            "XSS Results": xss_results
        }

        database_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_dbtype/prueba_dbtype.html", "a", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/"]
        database_scanner = DatabaseTypeScanner(urls)
        results["Database Results"] = database_scanner.scan_urls()

      
    # Imprimir los resultados en formato JSON
    print(json.dumps(results, indent=4))
    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)

    print("Resultados escritos en res.json exitosamente.")

if __name__ == "__main__":
    main()
