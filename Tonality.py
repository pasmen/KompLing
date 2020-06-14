import pymongo
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
from itertools import chain
import re, string, random


def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def Read_Date_base(base):
    person = [i['Person'] for i in base.find()]
    attraction = [i['Attraction'] for i in base.find()]
    return ' '.join(person) + ' '.join(attraction)


def Obtain(txt):
    lst = txt.split('.')
    lst_offer = []
    for i in lst:
        i = ' '.join(list(filter(None, re.split('\W', i))))
        lst_offer.append(i)
    return lst_offer


if __name__ == "__main__":

    stop_words = stopwords.words('english')
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []
    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)
    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset
    print(*dataset, sep='\n')
    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]
    classifier = NaiveBayesClassifier.train(train_data)

    client = pymongo.MongoClient("localhost", 27017)

    database = client['Mention']
    mention = database.mention

    text = Read_Date_base(mention)

    offer = Obtain(text)
    vocabulary = set(chain(*[i[0] for i in dataset))
    tweet_offer = {key_name: {i: i in vocabulary for i in key_name.lower().split()} for key_name in offer}
    file = open('Files\\output.txt', 'w', encoding='utf-8')
    for string in tweet_offer.keys():
        file.write(string + ': ' + classifier.classify(tweet_offer[string]) + '\n')
    file.close()
