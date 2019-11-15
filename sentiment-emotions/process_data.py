'''
Preprocess data for advanced NLP and model training.
'''

# Import necessary modules
import pandas as pd
import numpy as np
import re
import fasttext

def preprocess_tweet(tweet):
    
#     # To lowercase (not good for VADER)
#     tweet = tweet.lower()
    
    # Remove HTML special entities (e.g. &amp;)
    tweet = re.sub(r'\&\w*;', '', tweet)
    
    #Convert @username to "@user"
    tweet = re.sub('@[^\s]+','@user',tweet)
    
    # Remove whitespace (including new line characters)
    tweet = re.sub(r'\s\s+', ' ', tweet)
    
    # Remove single space remaining at the front of the tweet.
    tweet = tweet.lstrip(' ')
    
    # Remove characters beyond Basic Multilingual Plane (BMP) of Unicode:
    tweet = ''.join(c for c in tweet if c <= '\uFFFF')
    
    # Convert hyperlinks ->>>> For now just replace with http
    tweet = re.sub(r'https?:\/\/.*\/\w*', 'http', tweet)

    return tweet

# Preprocess "content"
df['content'] = df.content.apply(preprocess_tweet)

# Drop rows with sentiment "empty"
df = df[df.sentiment != 'empty']

# Drop rows with one or less characters in the tweet
df.drop(df[df.content.str.len()<2].index, inplace=True)

# Change sentiment of the tweets with only mentions to "neutral"
df.loc[df.content.str.replace("@[^\s]+", "").str.len()<3, 'sentiment'] = "neutral"


# Create a sentiment dictionary to map EMOTIONS to SENTIMENTS.
sentiment_dict = {'boredom': 'negative',
                  'hate': 'negative',
                  'sadness': 'negative',
                  'anger': 'negative',
                  'worry': 'negative',
                  'relief': 'positive',
                # 'empty': 'neutral',
                  'happiness': 'positive',
                  'love': 'positive',
                  'enthusiasm': 'positive',
                  'neutral': 'neutral',
                  'surprise':'positive',
                  'fun': 'positive'
                 }

# Create a feature "polarity"
df['polarity'] = df.sentiment.map(sentiment_dict)

def count_mentions(text):
    '''Returns number of mentions in a string.'''
    
    # Split the string into words
    words = text.split()
    
    # Create a list of words that are mentions
    mentions = [word for word in words if word.startswith("@")]
    
    # Return number of mentions
    return(len(mentions))

# Create a feature "mention_count"
df['mention_count'] = df['content'].apply(count_mentions)

def count_hashtags(text):
    '''Returns number of hashtags in a text.'''
    
    # Split the string into words
    words = text.split()
    
    # Create a list of words that are hashtags
    hashtags = [word for word in words if word.startswith("#")]
    
    # Return number of hashtags
    return(len(hashtags))

# Create a feature "hashtag_count"
df['hashtag_count'] = df['content'].apply(count_hashtags)

# Create a feature char_count
df['char_count'] = df['content'].apply(len)

# Create a new column "has_link"
df['has_link'] = df.content.str.contains("http")*1

# Load pretrained language model
language_model = fasttext.load_model('data/lid.176.bin')

# Load pretrained language model
language_model = fasttext.load_model('data/lid.176.bin')

def detect_fasttext(tweet):
    # Predict language
    prediction = language_model.predict(tweet)
    label = prediction[0][0].split("__label__")[1]
    return label

# Create a feature "language"
df['language'] = df.content.apply(detect_fasttext)

# Create a DataFrame only with english text
df = df[df['language'] == 'en']

# Drop the language column
df.drop('language', axis=1, inplace=True)