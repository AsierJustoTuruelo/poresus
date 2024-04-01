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
    parser.add_argument("-fh", "--filehashes", action="store_true", help="Run File Hashes scanner")
    parser.add_argument("-bm", "--binarymetadata", action="store_true", help="Run Binary Metadata scanner")
    parser.add_argument("-em", "--excelmetadata", action="store_true", help="Run Excel Metadata scanner")
    parser.add_argument("-gm", "--gifmetadata", action="store_true", help="Run GIF Metadata scanner")
    parser.add_argument("-pm", "--pdfmetadata", action="store_true", help="Run PDF Metadata scanner")
    parser.add_argument("-pwm", "--pptmetadata", action="store_true", help="Run PPT Metadata scanner")
    parser.add_argument("-wm", "--wordmetadata", action="store_true", help="Run Word Metadata scanner")
    parser.add_argument("-mm", "--mediametadata", action="store_true", help="Run Media Metadata scanner")
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
    parser.add_argument("-vi", "--validacioninput", action="store_true", help="Run Validacion Input scanner")
    parser.add_argument("-xss", "--xss", action="store_true", help="Run XSS scanner")
    #parser.add_argument("-xxe", "--xxe", action="store_true", help="Run XXE scanner")

    

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
        file_input_validator = FileUploadValidator(file_input_urls)
        file_input_validator.run_tests()
        results["File Input Results"] = file_input_validator.results
    
    if args.filehashes:
        # Ejecutar File Hashes scanner
        file_hashes_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_file/index.html"]
        file_hashes_scanner = OnionFileAnalyzer(file_hashes_urls)
        file_hashes_results = file_hashes_scanner.analyze_files()
        results["File Hashes Results"] = {
            "File Hashes Results": file_hashes_results
        }
    
    if args.binarymetadata:
        # Ejecutar Binary Metadata scanner
        binary_metadata_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html']
        binary_metadata_scanner = BinaryFileScanner(binary_metadata_urls)
        binary_metadata_results = binary_metadata_scanner.scan_binary_files()
        results["Binary Metadata Results"] = {
            "Binary Metadata Results": binary_metadata_results
        }
    
    if args.excelmetadata:
        # Ejecutar Excel Metadata scanner
        excel_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        excel_metadata_scanner = OnionExcelScanner(excel_metadata_urls)
        excel_metadata_results = excel_metadata_scanner.scan_excel_files()
        results["Excel Metadata Results"] = {
            "Excel Metadata Results": excel_metadata_results
        }
    
    if args.gifmetadata:
        # Ejecutar GIF Metadata scanner
        gif_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        gif_metadata_scanner = OnionGifScanner(gif_metadata_urls)
        gif_metadata_results = gif_metadata_scanner.scan_gif_files()
        results["GIF Metadata Results"] = {
            "GIF Metadata Results": gif_metadata_results
        }
    
    if args.pdfmetadata:
        # Ejecutar PDF Metadata scanner
        pdf_metadata_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html"]
        pdf_metadata_scanner = OnionPdfScanner(pdf_metadata_urls)
        pdf_metadata_results = pdf_metadata_scanner.scan_pdf_files()
        results["PDF Metadata Results"] = {
            "PDF Metadata Results": pdf_metadata_results
        }
    
    if args.pptmetadata:
        # Ejecutar PPT Metadata scanner
        ppt_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        ppt_metadata_scanner = OnionPptScanner(ppt_metadata_urls)
        ppt_metadata_results = ppt_metadata_scanner.scan_ppt_files()
        results["PPT Metadata Results"] = {
            "PPT Metadata Results": ppt_metadata_results
        }
    
    if args.wordmetadata:
        # Ejecutar Word Metadata scanner
        word_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        word_metadata_scanner = OnionWordScanner(word_metadata_urls)
        word_metadata_results = word_metadata_scanner.scan_word_files()
        results["Word Metadata Results"] = {
            "Word Metadata Results": word_metadata_results
        }
    
    if args.mediametadata:
        # Ejecutar Media Metadata scanner
        media_metadata_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        media_metadata_scanner = OnionMediaScanner(media_metadata_urls)
        media_metadata_results = media_metadata_scanner.scan_media_files()
        results["Media Metadata Results"] = {
            "Media Metadata Results": media_metadata_results
        }
    
    if args.imagemetadata:
        # Ejecutar Image Metadata scanner
        image_metadata_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html']
        image_metadata_scanner = OnionImageScanner(image_metadata_urls)
        image_metadata_results = image_metadata_scanner.scan_images()
        results["Image Metadata Results"] = {
            "Image Metadata Results": image_metadata_results
        }
    
    if args.googleids:
        # Ejecutar Google IDs extractor
        google_ids_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/google_ap/google_ap.html']
        google_ids_extractor = GoogleIDsExtractor(google_ids_urls)
        google_ids = google_ids_extractor.scan_google_services()
        results["Google IDs Results"] = {
            "Google IDs": google_ids if google_ids else "No se encontraron IDs de Google."
        }
    
    if args.gzipheader:
        # Ejecutar Gzip Header scanner
        gzip_header_urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html']
        gzip_header_scanner = GzipHeaderScanner(gzip_header_urls)
        gzip_header_results = gzip_header_scanner.scan_gzip_headers()
        results["Gzip Header Results"] = {
            "Gzip Header Results": gzip_header_results
        }
    
    if args.hostname:
        # Ejecutar Hostname Hacking scanner
        hostname_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_hostname/prueba_hostname.html"]
        hostname_scanner = HostnameHackingScanner(hostname_urls)
        hostname_results = hostname_scanner.scan_hostnames()
        results["Hostname Results"] = {
            "Hostname Results": hostname_results
        }
    
    if args.htmlinfo:
        # Ejecutar HTML Info scanner
        html_info_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        html_info_scanner = HtmlInfo(html_info_urls)
        html_info_results = html_info_scanner.analyze_html()
        results["HTML Info Results"] = {
            "HTML Info Results": html_info_results
        }
    
    if args.mailextractor:
        # Ejecutar Mail extractor
        mail_extractor_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/mail/mail.html"]
        mail_extractor = HtmlEmailExtractor(mail_extractor_urls)
        mail_addresses = mail_extractor.extract_emails()
        results["Mail Results"] = {
            "Mail Addresses": mail_addresses if mail_addresses else "No se encontraron direcciones de correo."
        }
    
    if args.otherservices:
        # Ejecutar Other Services scanner
        other_services_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/services/services.html"]
        other_services_scanner = OnionServiceAnalyzer(other_services_urls)
        other_services_results = other_services_scanner.analyze_services()
        results["Other Services Results"] = {
            "Other Services Results": other_services_results
        }
    
    if args.phonescanner:
        # Ejecutar Phone scanner
        phone_scanner_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/phone/phone.html"]
        phone_scanner = HtmlPhoneExtractor(phone_scanner_urls)
        phone_numbers = phone_scanner.extract_phone_numbers()
        results["Phone Results"] = {
            "Phone Numbers": phone_numbers if phone_numbers else "No se encontraron números de teléfono."
        }
    
    if args.phpserver:
        # Ejecutar PHP Server Info scanner
        php_server_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        php_server_scanner = PHPServerInfoScanner(php_server_urls)
        php_server_info = php_server_scanner.scan_php_server_info()
        results["PHP Server Results"] = {
            "PHP Server Info": php_server_info
        }
    
    if args.serverinfo:
        # Ejecutar Server Info scanner
        server_info_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        server_info_scanner = InformacionServidor(server_info_urls)
        server_info = server_info_scanner.get_server_info()
        results["Server Info Results"] = {
            "Server Info": server_info
        }
    
    if args.serverstatus:
        # Ejecutar Server Status checker
        server_status_urls = ["http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"]
        server_status_checker = ServerStatusChecker(server_status_urls)
        server_status = server_status_checker.check_server_status()
        results["Server Status Results"] = {
            "Server Status": server_status
        }
    
    if args.socialnets:
        # Ejecutar Social Networks scanner
        socialnets_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/social/social.html"]
        socialnets_scanner = RedesSocialesScanner(socialnets_urls)
        socialnets_results = socialnets_scanner.extract_social_networks()
        results["Social Networks Results"] = {
            "Social Networks": socialnets_results if socialnets_results else "No se encontraron redes sociales."
        }
    
    if args.sqlinjection:
        # Ejecutar SQL Injection scanner
        sqli_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_sqli/prueba_sqli.html"]
        sqli_scanner = AdvancedSqlInjectionScanner(sqli_urls)
        sqli_results = sqli_scanner.scan_sql_injection()
        results["SQL Injection Results"] = {
            "SQL Injection Results": sqli_results
        }
    
    if args.validacioninput:
        # Ejecutar Validacion Input scanner
        validacion_input_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_validacion_input/prueba_validacion_input.html"]
        validacion_input_scanner = ValidacionInput(validacion_input_urls)
        validacion_input_results = validacion_input_scanner.run_tests()
        results["Validacion Input Results"] = validacion_input_results
    
    if args.xss:
        # Ejecutar XSS scanner
        xss_urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_xss/prueba_xss.html"]
        xss_scanner = XSSScanner(xss_urls)
        xss_results = xss_scanner.scan_xss()
        results["XSS Results"] = {
            "XSS Results": xss_results
        }
    


      
    # Imprimir los resultados en formato JSON
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()