from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/reddit', methods=['POST'])
def api():
    try:
        data = request.json
        url = data.get('url')
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        titulo = soup.find_all('h1',class_="font-semibold")
        Body= soup.find_all('div',class_="text-neutral-content")
        titulo_texto= titulo[0].get_text(strip=True)
        content = ""

        for div in Body:
            parrafos= div.find_all('p')
            for parrafo in parrafos:
                texto=parrafo.get_text(strip=True)
                if texto:
                    content += texto + "\n"

        return jsonify({'titulo': titulo_texto, 'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)