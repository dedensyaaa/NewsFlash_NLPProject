# Group Name: ComputerVisionaries
# Members:
#   Bacus, Nicole Angel
#   Garciano Isaiah
#   Morales, Denisse Claire
#   Opleda, Melchiah

import streamlit as st
import nltk
from textblob import TextBlob
from newspaper import Article
from summarizer import Summarizer
import re
from datetime import datetime

# Download nltk data
nltk.download('punkt')

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.polarity

# Function to summarize article using BERT Extractive Summarizer
def summarize_article(text):
    model = Summarizer()
    summary = model(text)
    return summary

# Improved function to extract metadata from text
def extract_metadata(text):
    # Split text into lines
    lines = text.split('\n')
    
    # Initialize metadata
    title = "N/A"
    authors = ["N/A"]
    publish_date = "N/A"
    
    # Extract title (assuming the first line is the title)
    if lines:
        title = lines[0].strip()
    
    # Regular expressions for matching dates and authors
    date_patterns = [
        r'\b\d{2}/\d{2}/\d{4}\b',  # Matches dates in format DD/MM/YYYY
        r'\b\d{2}-\d{2}-\d{4}\b',  # Matches dates in format DD-MM-YYYY
        r'\b\d{4}/\d{2}/\d{2}\b',  # Matches dates in format YYYY/MM/DD
        r'\b\d{4}-\d{2}-\d{2}\b',  # Matches dates in format YYYY-MM-DD
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b',  # Matches dates like "Jan 1, 2020"
    ]
    author_patterns = [
        r'By ([A-Za-z\s]+)',  # Matches "By John Doe"
        r'Author: ([A-Za-z\s]+)'  # Matches "Author: John Doe"
        r'By: ([A-Za-z\s]+)'  
    ]
    
    # Check each line for dates and authors
    for line in lines[1:]:
        line = line.strip()
        # Check for date
        for pattern in date_patterns:
            match = re.search(pattern, line)
            if match:
                publish_date = match.group(0)
                # Convert publish date to a standard format
                try:
                    publish_date = datetime.strptime(publish_date, '%m/%d/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    try:
                        publish_date = datetime.strptime(publish_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                    except ValueError:
                        pass
                break

        # Check for author
        for pattern in author_patterns:
            match = re.search(pattern, line)
            if match:
                authors = [match.group(1)]
                break

    return title, authors, publish_date

# Main function
def main():
    # Set up sidebar and main content
    st.sidebar.title("NewsFlash")
    st.title("Welcome to NewsFlash!")

    # Welcome message
    st.write("Type in your news article URL or paste the article directly in the sidebar to start.")

    # Initialize session state to store results
    if 'results' not in st.session_state:
        st.session_state.results = []

    # Option to add URL or paste article
    option = st.sidebar.radio("Select Input Method", ("URL", "Paste Article"))

    if option == "URL":
        # Input URL
        url = st.sidebar.text_input("Enter URL")

        # Check if URL is provided
        if url:
            # Load article
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            # Analyze sentiment
            sentiment = analyze_sentiment(article.text)

            # Extract article information
            title = article.title
            authors = article.authors
            publish_date = article.publish_date
            summary = article.summary

            # Add result to session state
            result = {
                'url': url,
                'title': title,
                'authors': authors,
                'publish_date': publish_date,
                'summary': summary,
                'sentiment': sentiment
            }
            st.session_state.results.append(result)
    else:
        # Input article text
        article_text = st.sidebar.text_area("Paste Article")

        if st.sidebar.button("Analyze"):
            if article_text:
                # Summarize article
                summary = summarize_article(article_text)

                # Extract metadata
                title, authors, publish_date = extract_metadata(article_text)

                # Analyze sentiment
                sentiment = analyze_sentiment(article_text)

                # Add result to session state
                result = {
                    'url': "N/A",
                    'title': title,
                    'authors': authors,
                    'publish_date': publish_date,
                    'summary': summary,
                    'sentiment': sentiment
                }
                st.session_state.results.append(result)

    st.markdown("""
        <style>
        .result-box {
            border: 1px solid gray;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display previous results
    if st.session_state.results:
        for result in st.session_state.results:
            st.subheader("Results")
            if result['url'] != "N/A":
                st.write(f"**URL:** {result['url']}")
            if result['title'] != "N/A":
                st.write(f"**Title:** {result['title']}")
            if result['authors'] != ["N/A"]:
                st.write(f"**Authors:** {', '.join(result['authors'])}")
            if result['publish_date'] != "N/A":
                st.write(f"**Publication Date:** {result['publish_date']}")
            if result['summary'] != "N/A":
                st.write(f"**Summary:** {result['summary']}")
            st.write(f"**Sentiment:** {'positive' if result['sentiment'] > 0 else 'negative' if result['sentiment'] < 0 else 'neutral'}")
            st.markdown('<hr>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
