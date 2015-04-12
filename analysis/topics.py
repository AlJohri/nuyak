from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'\w+')
stop = stopwords.words('english')

from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nuyak.firebaseio.com', None)
yaks = firebase.get("/yaks", None)

texts = []
for message_id, yak in yaks.iteritems():
	# tokens = [word for sent in sent_tokenize(yak['message']) for word in word_tokenize(sent)]
	tokens = [token.lower() for token in tokenizer.tokenize(yak['message'])]
	text = [token for token in tokens if token not in stop]
	texts.append(text)

from gensim import corpora, models, similarities

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
corpus_lsi = lsi[corpus_tfidf]

for i, topic in enumerate(lsi.print_topics()):
	print "Topic {} -".format(i), topic

# for doc in corpus_lsi:
# 	print(doc)