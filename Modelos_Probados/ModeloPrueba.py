import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, TFAutoModel
import tensorflow as tf
import re
from collections import Counter

# Cargar datos
true_news = pd.read_csv('True.csv')
fake_news = pd.read_csv('Fake.csv')

# Etiquetar datos
true_news['label'] = 1
fake_news['label'] = 0
df = pd.concat([true_news, fake_news], axis=0)
df = df.sample(frac=0.1, random_state=42).reset_index(drop=True)  # Tomar el 10% de los datos para eficiencia

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Tokenización con mBERT (multilingüe)
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
X_train_tokens = tokenizer(list(X_train), padding=True, truncation=True, max_length=256, return_tensors="tf")
X_test_tokens = tokenizer(list(X_test), padding=True, truncation=True, max_length=256, return_tensors="tf")

# Convertir etiquetas a tensores
y_train_tensor = tf.convert_to_tensor(y_train.values)
y_test_tensor = tf.convert_to_tensor(y_test.values)

# Cargar modelo preentrenado mBERT
mbert_model = TFAutoModel.from_pretrained("bert-base-multilingual-cased")

# Construcción del modelo con capa de clasificación
input_ids = tf.keras.layers.Input(shape=(256,), dtype=tf.int32, name="input_ids")
attention_mask = tf.keras.layers.Input(shape=(256,), dtype=tf.int32, name="attention_mask")
embeddings = mbert_model(input_ids, attention_mask=attention_mask)[0]
output = tf.keras.layers.Dense(1, activation="sigmoid")(embeddings[:, 0, :])

model = tf.keras.Model(inputs=[input_ids, attention_mask], outputs=output)
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Entrenamiento del modelo
print("Procesando el modelo...")
model.fit(
    {"input_ids": X_train_tokens["input_ids"], "attention_mask": X_train_tokens["attention_mask"]},
    y_train_tensor,
    validation_data=(
        {"input_ids": X_test_tokens["input_ids"], "attention_mask": X_test_tokens["attention_mask"]},
        y_test_tensor,
    ),
    epochs=1,
    batch_size=4,  # Reduce el tamaño del lote si es necesario
)

# Función para calcular puntaje basado en reglas heurísticas
def calculate_score(text):
    score = 0
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    # Condición 1: Sensacionalismo
    sensational_words = ["urgente", "increíble", "impactante", "escándalo", "última hora", "nunca visto",
                         "urgent", "incredible", "shocking", "scandal", "breaking news", "never seen"]
    sensational_count = sum(1 for word in words if word in sensational_words)
    score += sensational_count * 0.5

    # Condición 2: Enlaces sospechosos
    suspicious_links = re.findall(r'https?://\S+', text)
    score += len([link for link in suspicious_links if any(domain in link for domain in [".xyz", ".click", ".info"])]) * 0.8

    # Condición 3: Uso excesivo de signos de exclamación
    exclamations = text.count("!")
    score += min(exclamations, 5) * 0.2

    # Condición 4: Falta de fuentes
    if not any(word in text.lower() for word in ["según", "informa", "according to", "reports"]):
        score += 0.5

    # Condición 5: Errores gramaticales/ortográficos
    errors = len(re.findall(r'\b[^aeiou\s]{4,}\b', text.lower()))  # Palabras sin vocales
    score += errors * 0.2

    # Condición 6: Repetición de palabras clave
    repeated_words = sum(count for count in word_counts.values() if count > 3)
    score += repeated_words * 0.1

    # Condición 7: Eventos/personas no verificables
    if re.search(r'\b(sin confirmar|no verificado|se dice que|unverified|rumored)\b', text.lower()):
        score += 0.8

    # Condición 8: Promesas irrealistas
    unrealistic_phrases = ["gana dinero", "haz esto ahora mismo", "sin esfuerzo", "resultados garantizados",
                           "make money", "do this now", "effortless", "guaranteed results"]
    unrealistic_count = sum(1 for phrase in unrealistic_phrases if phrase in text.lower())
    score += unrealistic_count * 0.5

    # Condición 9: Uso de mayúsculas
    uppercase_words = len([word for word in words if word.isupper()])
    score += uppercase_words * 0.1

    # Condición 10: Emojis o caracteres especiales
    emojis = len(re.findall(r'[^\w\s,.!?]', text))
    score += emojis * 0.3

    return score

# Evaluar una nueva noticia
nueva_noticia = "Nikolas Cruz, 19, has been charged with 17 counts of premeditated murder. Cruz was expelled from Marjory Stoneman Douglas High School for disciplinary reasons.He took an Uber to the school and opened fire with an AR-15-style semi-automatic rifle"

# Calcular puntaje heurístico
extra_score = calculate_score(nueva_noticia)
print(f"Puntaje adicional basado en condiciones: {extra_score:.2f}")

# Predicción con el modelo
nueva_noticia_tokens = tokenizer(
    [nueva_noticia],  # Asegúrate de que el texto sea una lista
    padding="max_length",  # Forzar el padding al tamaño máximo
    truncation=True,
    max_length=256,
    return_tensors="tf"
)

# Realizar la predicción con el modelo
prediccion = model.predict(
    {"input_ids": nueva_noticia_tokens["input_ids"], "attention_mask": nueva_noticia_tokens["attention_mask"]}
)
credibilidad = prediccion[0][0]

# Combinar resultados de modelo y reglas heurísticas
final_score = credibilidad - extra_score

# Determinar resultado final
if final_score > 0.5:
    print(f"Noticia REAL con un índice final de credibilidad de {final_score:.2f}")
else:
    print(f"Noticia FALSA con un índice final de credibilidad de {1 - final_score:.2f}")
