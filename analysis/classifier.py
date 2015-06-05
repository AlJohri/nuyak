from __future__ import division

import unicodecsv as csv

from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split

import numpy as np

np.set_printoptions(suppress=True)

class Yak(Bunch):
    def __init__(self, **kwargs):
        super(Yak, self).__init__(**kwargs)

yaks = None
with open("yaks.csv") as f:
    reader = csv.DictReader(f)
    yaks = [Yak(**row) for row in reader]

def known(x): return True if x != "?" and x != None and x != "" else False

def process(group, predict_unlabled_data=False):

    print group[0].upper() + group[1:]
    print "-----------------------"
    naive_bayes = BernoulliNB(alpha=1.0, fit_prior=True)
    vectorizer = TfidfVectorizer(min_df=2, max_df=.95, ngram_range=(1,2,), stop_words='english')
    text = [yak.message for yak in yaks if known(yak[group])]
    data = vectorizer.fit_transform(text)
    target = np.array([int(yak[group]) for yak in yaks if known(yak[group])])
    print "Shape:", data.shape
    print "Number of non-zero labels in target:", np.count_nonzero(target)
    print "5 Fold Cross Validation:", cross_val_score(naive_bayes, data, target, scoring='accuracy', cv=5, verbose=0, n_jobs=1)

    naive_bayes.fit(data, target) # train on all data
    terms = vectorizer.get_feature_names()
    t0 = [(naive_bayes.feature_log_prob_[0][i] * (naive_bayes.class_count_[0] / naive_bayes.class_count_.sum())) for i in range(len(terms))] # P(x_i|y0)
    t1 = [(naive_bayes.feature_log_prob_[1][i] * (naive_bayes.class_count_[1] / naive_bayes.class_count_.sum())) for i in range(len(terms))] # P(x_i|y1)
    for term, score in [(terms[i],t1[i]) for i in (-np.array(t1)).argsort()][:30]: print term, score

    print "-----------------------------------------"

    if predict_unlabled_data:
        new_ids = [yak.id for yak in yaks if not known(yak[group])]
        new_text = [yak.message for yak in yaks if not known(yak[group])]
        new_data = vectorizer.transform(new_text)
        predicted =  naive_bayes.predict(new_data)
        predicted_proba = naive_bayes.predict_proba(new_data)
        max_predicted_proba = [max(probas) for probas in predicted_proba]
        max_predicted_class = [probas.argmax() for probas in predicted_proba]

        # Psuedo Active Learning

        print "Lowest Probability Documents"

        for index in np.array(max_predicted_proba).argsort()[:20]:
            print predicted_proba[index], max_predicted_class[index], new_text[index][:60] + "..." # new_ids[index]

        print "-----------------------------------------"

        print "Highest Probability Documents that are %s" % group

        counter = 0
        for index in (-np.array(max_predicted_proba)).argsort():
            if counter > 20: break
            if max_predicted_class[index] == 1:
                counter += 1
                print predicted_proba[index], max_predicted_class[index], new_text[index][:60] + "..." # new_ids[index]

        print "-----------------------------------------"

if __name__ == '__main__':
    process('racist', predict_unlabled_data=True)
    process('depressed', predict_unlabled_data=True)
    process('horny', predict_unlabled_data=True)
    process('sexist', predict_unlabled_data=True)
    process('greek', predict_unlabled_data=True)