from setuptools import setup, find_packages

setup(
    name='deanonymize',  # Nombre de tu paquete
    version='0.1',  # Versión de tu paquete
    description='Una librería para deanonymize',  # Descripción corta
    packages=find_packages(),  # Esto encuentra todos los paquetes (directorios con __init__.py) automáticamente
    install_requires=[
        'requests',
        'PySocks',
        'pillow',
        'mmh3',
        'beautifulsoup4',
        'tqdm',
        'stem',
        'pandas',
        'PyPDF2',
        'python-docx',
        'python-pptx',
        'mutagen',
        
    ]
)
