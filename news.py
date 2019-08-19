import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path

data_folder = Path('data/train/')
file_to_open = data_folder / 'RedditNews_train.csv'

news = pd.read_csv(file_to_open)

max_features = 200 # note this hyperparameter

# Drop NAs
news.dropna(inplace=True)

# Change text to lower case
news['News'] = news['News'].apply(lambda x: x.lower())

# Concat stories by day
news = news.groupby(['Date'])['News'].apply(lambda x: ', '.join(x)).reset_index()

# Import CountVectorizer
# Note max features as a hyperparameter!!
vectorizer = CountVectorizer(max_features=max_features)
corpus = news['News'].values
news_vectors = vectorizer.fit_transform(corpus).toarray()

# Concat vectors with dates
news = pd.concat([news.Date, pd.DataFrame(news_vectors)], axis=1)

# Export csv
news.to_csv('data-interim/text_features.csv',index=False)