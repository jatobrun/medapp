from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from io import BytesIO
from PIL import Image as PILImage
from pathlib import Path
import cloudinary as Cloud
#from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'c81dac792846c247acb200f1b0a7eab4'
client = MongoClient(
    "mongodb+srv://jatobrun:jatobrun@cluster0-hx8rh.mongodb.net/test?retryWrites=true&w=majority")
#client = MongoClient("mongodb://localhost:2717")
db = client['MedScan']
tabla_usuarios = db['Usuarios']
tabla_estudios = db['Estudios']
tabla_examenes = db['Examenes']
tabla_paquetes = db['Paquetes']
tabla_empresas = db['Empresas']
tabla_archivos = db['Archivos']
bcrypt = Bcrypt(app)
Cloud.config(
    cloud_name="dscvja8yk",
    api_key="134245124854917",
    api_secret='N8mD3-3nLFVjItRfM_oexclt35I'
)
#login_manager = LoginManager(app)
from src import routes