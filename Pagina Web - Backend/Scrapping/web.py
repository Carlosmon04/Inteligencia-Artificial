from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app) 
@app.route('/Web', methods=['POST'])

def api():
    try:
         data = request.json
         url = data.get('url')
         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
         response = requests.get(url, headers=headers)
         response.raise_for_status()  
         soup = BeautifulSoup(response.text, 'html.parser')
         title = soup.find('h1').get_text(strip=True)

         paragraphs = soup.find_all('p')
         content = ' '.join(p.get_text(strip=True) for p in paragraphs)

         return jsonify({'title': title, 'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)


