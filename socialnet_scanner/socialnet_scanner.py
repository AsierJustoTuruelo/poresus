import requests
import re
import socks
import socket

class RedesSocialesScanner:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def escanear_redes_sociales(self):
        try:
            # Configurar el proxy para las solicitudes
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            # Realizar la solicitud HTTP para obtener el contenido de la página
            response = requests.get(self.url, proxies=self.proxies)
            if response.status_code == 200:
                # Utilizar expresiones regulares para buscar enlaces a redes sociales
                patrones_redes_sociales = {
                    'twitter': r'(https?://(?:www\.)?twitter\.com/[\w-]+)|\btwitter\b',
                    'facebook': r'(https?://(?:www\.)?facebook\.com/[\w-]+)|\bfacebook\b',
                    'instagram': r'(https?://(?:www\.)?instagram\.com/[\w-]+)|\binstagram\b',
                    'reddit': r'(https?://(?:www\.)?reddit\.com/r/[\w-]+)|\breddit\b',
                    'youtube': r'(https?://(?:www\.)?youtube\.com/[\w-]+)|\byoutube\b',
                    'whatsapp': r'(https?://(?:www\.)?wa\.me/[\w-]+)|\bwhatsapp\b',
                    'wechat': r'(https?://(?:www\.)?weixin\.qq\.com/[\w-]+)|\bwechat\b',
                    'tiktok': r'(https?://(?:www\.)?tiktok\.com/@[\w-]+)|\btiktok\b',
                    'linkedin': r'(https?://(?:www\.)?linkedin\.com/in/[\w-]+)|\blinkedin\b',
                    'telegram': r'(https?://(?:www\.)?t\.me/[\w-]+)|\btelegram\b',
                    'snapchat': r'(https?://(?:www\.)?snapchat\.com/add/[\w-]+)|\bsnapchat\b',
                    'pinterest': r'(https?://(?:www\.)?pinterest\.com/[\w-]+)|\bpinterest\b',
                    'quora': r'(https?://(?:www\.)?quora\.com/profile/[\w-]+)|\bquora\b',
                    'twitch': r'(https?://(?:www\.)?twitch\.tv/[\w-]+)|\btwitch\b',
                    'discord': r'(https?://(?:www\.)?discord\.gg/[\w-]+)|\bdiscord\b',
                }

                # Almacenar el texto de la respuesta en una lista de líneas
                lineas = response.text.split('\n')

                redes_sociales_encontradas = {}
                for nombre_red_social, patron in patrones_redes_sociales.items():
                    for i, linea in enumerate(lineas):
                        if re.search(patron, linea):
                            if nombre_red_social not in redes_sociales_encontradas:
                                redes_sociales_encontradas[nombre_red_social] = []
                            redes_sociales_encontradas[nombre_red_social].append((i+1, linea.strip()))

                return redes_sociales_encontradas
            else:
                print(f'Error al obtener la página. Código de estado: {response.status_code}')
                return None
        except Exception as e:
            print(f'Error al escanear las redes sociales: {e}')
            return None

if __name__ == "__main__":
    url_pagina = input("Ingrese la URL de la página que desea escanear en busca de redes sociales: ")
    scanner = RedesSocialesScanner(url_pagina)
    redes_sociales_encontradas = scanner.escanear_redes_sociales()
    
    if redes_sociales_encontradas:
        print("Redes sociales encontradas:")
        for red_social, enlaces in redes_sociales_encontradas.items():
            if enlaces:
                print(f"{red_social.capitalize()}:")
                for num_linea, linea in enlaces:
                    print(f"Línea {num_linea}: {linea}")
            else:
                pass
                #print(f"No se encontraron enlaces a {red_social.capitalize()}.")
    else:
        pass
        print("No se encontraron redes sociales en la página.")
