# your_library_name/__init__.py (empty)
# your_library_name/your_library.py (contains the library code)

import cv2
import numpy as np
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
import nltk
from nltk.stem import WordNetLemmatizer

class hashtagger:
    def __init__(self):
        # Load the pre-trained InceptionV3 model
        self.model = InceptionV3(weights="imagenet")
        
        # Initialize WordNet Lemmatizer
        self.lemmatizer = WordNetLemmatizer()
    
    def recognize_objects(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (299, 299))  # InceptionV3 expects 299x299 images
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)  # Preprocess input as required by InceptionV3
        predictions = self.model.predict(image)
        decoded_predictions = decode_predictions(predictions, top=5)[0]
        return decoded_predictions
    
    def generate_tags(self, decoded_predictions):
        tags = set()  # Use a set to store unique tags
        for prediction in decoded_predictions:
            label = prediction[1].replace("_", " ").lower()
            
            # Lemmatize the label (you can skip the POS tagging step)
            lemma = self.lemmatizer.lemmatize(label)
            
            # Add to the set
            tags.add(lemma)
        
        return tags
