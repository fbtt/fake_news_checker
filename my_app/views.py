from django.shortcuts import render
import sklearn
import pandas as pd
import pickle
import re


# loading model
with open('clf_logistic_regression.pickle', 'rb') as handle:
    clf_logistic_regression = pickle.load(handle)


# loading tokenizer
with open('vectorizer_logistic_regression.pickle', 'rb') as handle:
    vectorizer_tfidf = pickle.load(handle)


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
    """ This function receives a string containing the textual content and returns its veracity """

    df = pd.DataFrame({'text': [sample_text]})
    df_preprocessed = pre_processing(df)
    sample_preprocessed = vectorizer_tfidf.transform(df_preprocessed['text'])
    y_pred = clf_logistic_regression.predict(sample_preprocessed)[0]
    str_y_pred = 'FALSA' if (y_pred == 1) else 'VERDADEIRA'

    return str_y_pred


def home(request):
    return render(request, template_name='base.html')


def new_check(request):

    news_content = request.POST.get('news_content')
    veracity = predict(news_content)

    frontend_context = {
        'veracidade': veracity,
    }

    return render(request, 'my_app/new_check.html', frontend_context)
