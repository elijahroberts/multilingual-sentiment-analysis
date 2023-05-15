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
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def get_model_and_tokenizer(language):
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

def main():
    st.title("Multilingual Review Sentiment Analysis")

    language = st.selectbox('Select language', ['English', 'French', 'German', 'Spanish'])
    model, tokenizer = get_model_and_tokenizer(language)

    text_to_analyze = st.text_input('Enter text to analyze')

    if st.button('Analyze'):
        # Here you would use your model and tokenizer to analyze the input text
        # I'm just printing the model and tokenizer to demonstrate
        st.write(f'Model: {model}')
        st.write(f'Tokenizer: {tokenizer}')

if __name__ == "__main__":
    main()

import streamlit as st
from transformers import BertForSequenceClassification, BertTokenizer

def get_model_and_tokenizer(language):
    if language == "English":
        model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_english"
    elif language == "French":
        model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_french"
    elif language == "German":
        model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_german"
    elif language == "Spanish":
        model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_spanish"
    
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

    return model, tokenizer

def classify_text(text, language):
    model, tokenizer = get_model_and_tokenizer(language)
    inputs = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors="pt")
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(axis=1)
    return predictions.item()

st.title("Language Specific Sentiment Analysis")

language = st.selectbox("Select language", ["English", "French", "German", "Spanish"])
text = st.text_input("Enter text to analyze")

if st.button("Analyze"):
    sentiment = classify_text(text, language)
    st.write(f"Sentiment: {sentiment}")

import streamlit as st
import nltk
import re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline

@st.cache(allow_output_mutation=True)
def load_model():
    model_name = "Worgu/Final_Project_finetuned_bert-base-multilingual-cased_english"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

def clean_english_text(text):
    if isinstance(text, dict):
        values = list(text.values())
        text = ' '.join(str(val) for val in values)
    sentences = nltk.sent_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    cleaned_sentences = []
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        stopwords = set(nltk.corpus.stopwords.words('english'))
        words = [word for word in words if word not in stopwords]
        stemmer = SnowballStemmer('english')
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
    st.title("Text Sentiment Analysis")
    text_input = st.text_input("Enter your text here:")
    if text_input:
        cleaned_text = clean_english_text(text_input)
        tokenizer, model = load_model()
        classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)
        result = classifier(cleaned_text)
        label = result[0]['label']
        if label == 'LABEL_0':
            st.write("Sentiment: positive 😄")
        elif label == 'LABEL_2':
            st.write("Sentiment: neutral 😐")    
        else:
            st.write("Sentiment: negative ☹️")

if __name__ == "__main__":
    main()

import streamlit as st
import nltk
import re
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
    language = st.selectbox("Select language", ["English", "French", "German", "Spanish"])
    text_input = st.text_input("Enter text to analyze:")
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

