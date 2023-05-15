# -*- coding: utf-8 -*-
"""multilingual analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-8qxdX5bPLG6Q7-8FsPmn70ixr8msFGw
"""

import os
from huggingface_hub import HfApi, HfFolder

token = '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'
os.environ["HUGGINGFACE_TOKEN"] = token

api = HfApi()
folder = HfFolder()
folder.save_token(token)
user = api.whoami()
print(user)



import streamlit as st
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

@st.cache(allow_output_mutation=True)
def load_model(language):
    if language == "English":
        model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_english"
    elif language == "French":
        model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_french"
    elif language == "German":
        model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_german"
    elif language == "Spanish":
        model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_spanish"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    return model, tokenizer

def clean_text(text, language):
    sentences = nltk.sent_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    cleaned_sentences = []
    stopwords = set(nltk.corpus.stopwords.words(language.lower()))
    stemmer = SnowballStemmer(language.lower())
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word not in stopwords]
        words = [stemmer.stem(word) for word in words]
        lem_words = [lemmatizer.lemmatize(word) for word in words]
        lem_words = [re.sub('\W+', ' ', word) for word in lem_words]
        lem_words = [re.sub('\s+', ' ', word).strip() for word in lem_words]
        lem_words = [re.sub(r'\d+', '', word) for word in lem_words]
        lem_words = [re.sub(r'[^\w\s]', '', word) for word in lem_words]
        cleaned_sentence = ' '.join(lem_words)
        cleaned_sentences.append(cleaned_sentence)
    cleaned_text = ' '.join(cleaned_sentences)
    return cleaned_text

def main():
    st.title("Multilingual Sentiment Analysis")
    language = st.selectbox("Select language", ["English", "French", "German", "Spanish"], key = 'language_select_4')
    text_input = st.text_input("Enter text to analyze:", key = 'text_input_4')

    if st.button("Analyze"):  # Corrected indentation
        if text_input:
            cleaned_text = clean_text(text_input, language)
            model, tokenizer = load_model(language)
            pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)
            result = pipeline(cleaned_text)[0]
            label = result['label']
            if label == 'LABEL_0':
                st.write("Sentiment: positive 😄")
            elif label == 'LABEL_2':
                st.write("Sentiment: neutral 😐")    
            else:
                st.write("Sentiment: negative ☹️")


if __name__ == "__main__":
    main()




