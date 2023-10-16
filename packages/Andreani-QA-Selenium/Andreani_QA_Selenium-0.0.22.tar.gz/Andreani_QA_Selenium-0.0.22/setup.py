import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.22'
PACKAGE_NAME = 'Andreani_QA_Selenium'  # Debe coincidir con el nombre de la carpeta
AUTHOR = 'AndreaniTesting'
AUTHOR_EMAIL = 'user_appglatest@andreani.com'
URL = ''

LICENSE = 'MIT'  # Tipo de licencia
DESCRIPTION = 'SeleniumFramework para ejecución de casos automatizados'  # Descripción corta
LONG_DESCRIPTION = ""  # Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"

# Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
    'allure-behave', 'allure-pytest', 'allure-python-commons', 'Andreani-QA-Parameters',
    'Andreani-QA-Functions', 'Andreani-QA-Debugger', 'requests', 'selenium==4.11.2', 'webdriver_manager', 'pywin32'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
