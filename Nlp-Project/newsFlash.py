# before running the app, install these first:
# pip install nltk
# pip install textblob
# pip install newspaper3k
# pip install lxml_html_clean

import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

nltk.download('punkt')

# there's no actual NLP happening because the libraries are doing the work already

url = 'https://www.sunstar.com.ph/cebu/7-cebu-schools-4-others-in-central-visayas-seek-tuition-hike'

# pass the url into an article

article = Article(url)

article.download()
article.parse()

article.nlp()

print(f'Title: {article.title}')
print(f'Author/s: {article.authors}')
print(f'Publication Date: {article.publish_date}')
print(f'Summary: {article.summary}')

analysis = TextBlob(article.text)
print(analysis.polarity)
print(f'Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}')

