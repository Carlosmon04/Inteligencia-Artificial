from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig


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
        
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    
        
        Resumen = content
        inputs = tokenizer([Resumen], return_tensors='pt',truncation=True)


        summary_ids = model.generate(inputs['input_ids'], max_length=1024, early_stopping=False)
        final_summary = [tokenizer.decode(g, skip_special_tokens=True) for g in summary_ids]


        resultado_final = " ".join(final_summary)

        return jsonify({'titulo': titulo_texto, 'content': resultado_final})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)