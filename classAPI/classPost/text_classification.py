import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Ma'lumotlar bazasini yuklash
data = pd.read_csv('classWords.csv')
data['text'] = data['text'].str.lower() # hamma so'zlar kichik harflarga o'tkaziladi

# matn va natija ustunlarini alohida listlarda saqlaymiz
texts = data['text'].tolist()
labels = data['label'].tolist()

# Matnni oldindan qayta ishlash
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(data['text'])
sequences = tokenizer.texts_to_sequences(data['text'])
padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=200)

# Label larni vektorlashtirish
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(data['label'].values)

# Label larni bitta kodlangan formatga aylantirish
num_classes = len(np.unique(labels))
labels = tf.keras.utils.to_categorical(labels, num_classes=num_classes)

# Ma'lumotlarni ajratish
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

# Modelni aniqlash
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=128),
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(32),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Modelni kompilyatsiya qilish
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Modelni o'qitish
history = model.fit(X_train, y_train, epochs=20, batch_size=64, validation_split=0.2)

# Modelni baholash
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Sinov yo'qotishi: {loss:.3f}, Sinov aniqligi: {accuracy:.3f}")

# Bashorat qilish (natijani olish)
text = input('Matn kiriting: ')
sequence = tokenizer.texts_to_sequences([text.lower()])
padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=200)
prediction = model.predict(padded_sequence)
label = np.argmax(prediction)
predicted_label = label_encoder.inverse_transform([label])[0]
print(f'Matn: {text}, Natija: {predicted_label}')
