#-----------------------------------------------------------------------------------------
# import libraries
import pandas as pd
from PIL import Image
import re
import sys
import nltk
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('vader_lexicon')

#-----------------------------------------------------------------------------------------

#set title
st.markdown("<h1 style='text-align: center; color: white;'>Sentiment Analyzer</h1>", unsafe_allow_html=True)

# creating objects for stopwords,lemmatizer and sentiment_analyzer
stop_words =set(stopwords.words('english'))
stop_words.remove('not')
stop_words.remove('no')
lemmatizer = WordNetLemmatizer()
sentiment_analyzer = SentimentIntensityAnalyzer()

#-----------------------------------------------------------------------------------------
# function to clean the text
def clean_data(text):
    text = re.sub(r'[^\w\s]','',str(text))
    text = re.sub(r'\d','',text)
    text_token = word_tokenize(text.lower().strip())
    text_no_stopwords = []
    for token in text_token:
        if token not in stop_words:
            token = lemmatizer.lemmatize(token)
            text_no_stopwords.append(token)
    clean_text = (' '.join(text_no_stopwords))
    return clean_text

# function to give the Sentiment score to reviews
def sentiment(ctext):
    score = sentiment_analyzer.polarity_scores(ctext)
    print(score)
    if score['pos'] > 0.6 or (score['neu'] > 0.4 and score['neg'] < 0.2) :
        return 'Positive'
    elif score['neg'] > 0.6 or (score['neu'] > 0.4 and score['pos'] < 0.2):
        return 'Negative'
    else:
        return 'Neutral'

image = Image.open('/img/S.png')
pos = Image.open('/img/1.jpg')
neu = Image.open('/img/2.jpg')
neg = Image.open('/img/3.jpg')
#--------------------------------------------------------------------------------------------------

st.image(image, caption='Sentiment analysis')
st.write("Hi, Nice to meet you")

# text input
text = st.text_input('Enter the Text', 'Have a great day')

# Main flow of the app
if st.button('Get Sentiment'):
    ctext = clean_data(text)
    tsentiment = sentiment(ctext)
    st.caption("'"+text+"' is a "+tsentiment+" text" )
    if tsentiment == 'Positive':
        st.image(pos,caption='Positive')
    if tsentiment == 'Neutral':
        st.image(neu,caption='Neutral')
    if tsentiment == 'Negative':
        st.image(neg,caption='Negative')
#---------------------------------------------------------------------------------------------------
