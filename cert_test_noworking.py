import socks
import socket
import ssl
import OpenSSL

class OnionTLSAnalyzer:
    def __init__(self, onion_url):
        self.onion_url = onion_url

    def get_tls_certificate(self):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            context = ssl.create_default_context()
            with socket.create_connection((self.onion_url, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.onion_url) as ssock:
                    cert_bin = ssock.getpeercert(binary_form=True)
                    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert_bin)
                    cert_info = {
                        "subject": dict(x509.get_subject().get_components()),
                        "issuer": dict(x509.get_issuer().get_components()),
                        "not_before": x509.get_notBefore().decode("utf-8"),
                        "not_after": x509.get_notAfter().decode("utf-8"),
                        "serial_number": x509.get_serial_number(),
                        "version": x509.get_version(),
                    }
                    return cert_info
        except Exception as e:
            print(f"Error al obtener el certificado TLS: {e}")
            return None

if __name__ == "__main__":
    onion_url = input("Ingrese el nombre del host de la página .onion para obtener su certificado TLS: ")
    analyzer = OnionTLSAnalyzer(onion_url)
    cert_info = analyzer.get_tls_certificate()
    if cert_info:
        print("Información del certificado TLS:")
        for key, value in cert_info.items():
            print(f"{key}: {value}")
    else:
        print("No se pudo obtener la información del certificado TLS.")

