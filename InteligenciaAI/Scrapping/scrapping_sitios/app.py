from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        #Obtener la URL 
        data = request.json
        url = data.get('url')
        response = requests.get(url)
        response.raise_for_status()  

       #obtener el contenido con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()

        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


