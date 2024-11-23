import nltk
from nltk.corpus import stopwords
import json
import string
import unicodedata
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('punkt')
import pandas as pd
import numpy as np
from nltk.tokenize import TweetTokenizer # use this one because the other one struggles with words like "don't"
from sklearn.feature_extraction.text import CountVectorizer
from argparse import ArgumentParser


def filter_sentence(sentence, stop_words, tokenizer):
    word_tokens = tokenizer.tokenize(sentence)
    word_tokens = filter(lambda x: len(x) > 1 and x != '...', word_tokens) # removes all punctuation/symbols found by tokenizer
    filtered_sentence = ' '.join([w for w in word_tokens if (not w.lower() in stop_words) and not w.isdigit()]) # remove stop words and numbers
    return filtered_sentence

def pre_process_descriptions(df):
    stop_words = set(stopwords.words('english'))
    tokenizer = TweetTokenizer()
    df['description_processed'] = df['description'].map(lambda x: filter_sentence(x, stop_words, tokenizer))

def load_df(fname):
    df = pd.read_csv(fname, sep='\t')
    df['valid'] = df['description'].map(lambda x: type(x) == str) # remove NaN
    df = df[df['valid']]
    # TODO: Delete this line later...
    df['topic'] = np.random.randint(0,9, size=len(df))
    pre_process_descriptions(df)
    return df

def get_corpus_by_category(df):
  corpus_dict = dict()
  for topic in df.topic.unique():
    filtered_df = df[df.topic == topic]
    sentence = ' '.join(filtered_df['description_processed'])
    corpus_dict[topic] = sentence
  return corpus_dict

def get_top_n_tfidf(df, n):
    out_dict = dict()
    vectorizer = CountVectorizer()
    corpus_by_category = get_corpus_by_category(df)
    categories = list(corpus_by_category.keys())
    result = vectorizer.fit_transform(corpus_by_category.values())
    tf = result.toarray()
    feature_names = vectorizer.get_feature_names_out()
    
    N = len(corpus_by_category) # numerator of idf
    document_counts = (tf > 0).sum(axis=0) # denominator of idf
    idf_scores = np.log(N / document_counts) # compute idf scores y
    tf_idf_scores = tf * idf_scores # tf-idf

    for i in range(len(tf)):
        row = tf_idf_scores[i,:]
        indices = np.argsort(row)[::-1][:n]
        words = feature_names
        out_dict[categories[i].item()] = [[words[i], row[i]] for i in indices]
    
    return out_dict

def main():
   parser = ArgumentParser()
   parser.add_argument('-n', help='Number of words to return per category', required=False, default=10)
   parser.add_argument('-i', help='Input TSV file')
   parser.add_argument('-o', help='Output JSON file')
   args = parser.parse_args()

   n = int(args.n)
   tsv_file = args.i
   output_file = args.o

   df = load_df(tsv_file)

   tf_idf_dict = get_top_n_tfidf(df, n)

   with open(output_file, 'w') as f:
      json.dump(tf_idf_dict, f)


if __name__ == "__main__":
   main()