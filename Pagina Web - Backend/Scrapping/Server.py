from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


app = Flask(__name__)
CORS(app)

@app.route('/Web', methods=['POST'])
def api_web():
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

        MODEL = "jy46604790/Fake-News-Bert-Detect"
        clf = pipeline("text-classification", model=MODEL, tokenizer=MODEL)

        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        inputs = tokenizer(content, return_tensors='pt', max_length=1024, truncation=True)
        summary_ids = model.generate(inputs['input_ids'], max_length=200, min_length=50, length_penalty=2.0, early_stopping=True)
        final_summary =tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        classification_result = clf(final_summary)[0]  
        label = classification_result['label'] 
        confidence = classification_result['score'] 
        # Interpretar el resultado
        if label == 'LABEL_1':
            classification_text = "Noticia verdadera"
        else:
            classification_text = "Noticia falsa"

        return jsonify({
            'titulo': title,
            'resumen': final_summary,
            'clasificacion': f"{classification_text} (Confianza: {confidence * 100:.2f}%)"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reddit', methods=['POST'])
def api_reddit():
    try:
        data = request.json
        url = data.get('url')
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        titulo = soup.find_all('h1',class_="font-semibold")
        Body = soup.find_all('div', class_="text-neutral-content")
        titulo_texto = titulo[0].get_text(strip=True)
        content = ""

        for div in Body:
            parrafos = div.find_all('p')
            for parrafo in parrafos:
                texto = parrafo.get_text(strip=True)
                if texto:
                    content += texto + "\n"
        
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    
        Resumen = content
        inputs = tokenizer([Resumen], return_tensors='pt', truncation=True)
        MODEL = "jy46604790/Fake-News-Bert-Detect"
        clf = pipeline("text-classification", model=MODEL, tokenizer=MODEL)
        summary_ids = model.generate(inputs['input_ids'], max_length=1024, early_stopping=False)
        final_summary = [tokenizer.decode(g, skip_special_tokens=True) for g in summary_ids]

        classification_result = clf(final_summary)
        if isinstance(classification_result, list):
            label = classification_result[0]['label']
            confidence = classification_result[0]['score']
        else:
            label = classification_result['label']
            confidence = classification_result['score']

        if label == 'LABEL_1':
            news_status = "Noticia verdadera"
        else:
            news_status = "Noticia falsa"
        

        return jsonify({
            'titulo': titulo_texto,
            'resumen': final_summary,
            'clasificacion': f"{news_status} (Confianza: {confidence * 100:.2f}%)"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)
