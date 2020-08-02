from django.shortcuts import render
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import pickle
import re


# loading model
model = tf.keras.models.load_model("my_keras_model.h5")

# loading tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# ------------------ temp code ------------------


# lower case all data
def lowerize_text(df):
    df = df.copy()
    df['text'] = df['text'].apply(lambda x: x.lower())
    return df


# Dummy feature: numerals
def numeral_to_dummy(df):
    df = df.copy()
    df['text'] = df['text'].apply(lambda x: re.sub(
        r'(\d+[\d\.\,]{1,}\d|\d{1,})', '0', x))
    return df


# Dummy feature: URLs
def url_to_dummy(df):
    df = df.copy()
    pattern = r"""(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))?"""
    df['text'] = df['text'].apply(lambda x: re.sub(pattern, 'URL', x))
    return df


# Dummy feature: emails
def email_to_dummy(df):
    df = df.copy()
    df['text'] = df['text'].apply(lambda x: re.sub(
        r"""[\w\+\.\-\~]+@[\w\.\-]+\.\w+""", 'EMAIL', x))
    return df


# remove special chars
def remove_special_chars(df):
    df = df.copy()
    df['text'] = df['text'].apply(lambda x: re.sub(r"“|”|‘|’|–|…|'", '', x))
    return df


def pre_processing(df):
    df = df.copy()
    df = lowerize_text(df)
    df = numeral_to_dummy(df)
    df = url_to_dummy(df)
    df = email_to_dummy(df)
    df = remove_special_chars(df)
    return df


def predict(sample_text):

    df = pd.DataFrame({'text': [sample_text]})

    df_preprocessed = pre_processing(df)

    encoded_doc = tokenizer.texts_to_sequences(df_preprocessed['text'])

    sample_preprocessed = pad_sequences(encoded_doc,
                                        padding='post',
                                        truncating='post',
                                        maxlen=1941
                                        )

    y_pred = model.predict(sample_preprocessed)
    y_pred_rounded = y_pred[0][0].round()

    if y_pred_rounded == 1.0:
        str_y_pred = 'VERDADEIRA'
    else:
        str_y_pred = 'FALSA'

    return str_y_pred


def home(request):
    return render(request, template_name='base.html')


def new_check(request):

    news_content = request.POST.get('news_content')

    # Consulta modelo e retornar veracidade
    veracity = predict(news_content)

    frontend_context = {
        'veracidade': veracity,
    }

    return render(request, 'my_app/new_check.html', frontend_context)
