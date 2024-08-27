import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# URL de la carpeta donde se encuentran los archivos
base_url = 'https://caddexpert.com/wp-content/uploads/2020/05/'

# Directorio donde se guardarán los archivos descargados
download_dir = ''

# Crea el directorio si no existe
os.makedirs(download_dir, exist_ok=True)

# Realiza la petición GET para obtener el contenido de la página
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Encuentra todos los enlaces en la página
links = soup.find_all('a')

# Filtra los enlaces que parecen ser archivos
for link in links:
    file_name = link.get('href')
    if file_name.endswith(('.zip', '.rar', '.pdf', '.dwg', '.dxf', '.png', '.jpg', '.jpeg', '.stl')):
        file_url = urljoin(base_url, file_name)
        parsed_url = urlparse(file_url)
        file_name = os.path.basename(parsed_url.path)  # Solo obtiene el nombre del archivo

        print(f'Descargando {file_name}...')

        # Descarga el archivo y lo guarda en el directorio especificado
        file_path = os.path.join(download_dir, file_name)
        with requests.get(file_url, stream=True) as r:
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f'{file_name} descargado exitosamente.')

print('Descarga completada.')
