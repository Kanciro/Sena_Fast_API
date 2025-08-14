# app.py
from flask import Flask

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define una ruta y una función asociada
@app.route('/')
def home():
    return '¡Hola, Flask se encuentra funcionando!'

# Esta parte asegura que el servidor solo se ejecute cuando el script es el principal
if __name__ == '__main__':
    # Inicia el servidor
    app.run(debug=True)