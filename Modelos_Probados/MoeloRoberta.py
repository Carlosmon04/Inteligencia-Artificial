from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Cargar el modelo y el tokenizador
tokenizer = AutoTokenizer.from_pretrained("hamzab/roberta-fake-news-classification")
model = AutoModelForSequenceClassification.from_pretrained("hamzab/roberta-fake-news-classification")

def predict_fake(title, text):
    input_str = "<title>" + title + "<content>" + text + "<end>"
    input_ids = tokenizer.encode_plus(input_str, max_length=512, padding="max_length", truncation=True, return_tensors="pt")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    with torch.no_grad():
        output = model(input_ids["input_ids"].to(device), attention_mask=input_ids["attention_mask"].to(device))
    return dict(zip(["Fake", "Real"], [x.item() for x in list(torch.nn.Softmax(dim=1)(output.logits)[0])]))

# Ejemplo de prueba
title = "James Webb Space Telescope captures stunning image of 'Pillars of Creation "
content = "The James Webb Space Telescope has captured an awe-inspiring image of the 'Pillars of Creation,' a famous region within the Eagle Nebula where new stars are forming. The image, taken in unprecedented detail using Webb's near-infrared camera, showcases the dense, gaseous clouds and newly forming stars. Scientists hope these observations will provide insights into star formation and the evolution of galaxies. The Pillars of Creation were previously imaged by the Hubble Space Telescope, but Webb's advanced technology has revealed new details, making it a historic milestone in astronomy."

print(predict_fake(title, content))
