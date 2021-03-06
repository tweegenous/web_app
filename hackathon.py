import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import string
import nltk
from nltk import FreqDist
import warnings 
from nltk.stem.porter import  *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from nltk.collocations import *
from sklearn.feature_extraction.text import TfidfVectorizer

#stop_words = set(stopwords.words('english'))



train = pd.read_csv('/home/rrahul/Desktop2/Till_August/Project_sem_5/kerala_flood/nepal.csv')
#print (train['text'])
tweets=train['text']



train['text'] = train['text'].str.replace("[^a-zA-Z#]", " ") 

#Removing Short Words

train['text'] = train['text'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))



#tokenization
tokenized_tweet = train['text'].apply(lambda x: x.split())


#print (tokenized_tweet)
#Stemming is done in this part
stemmer = PorterStemmer()

#tokenized_tweet = tokenized_tweet.apply(lambda x:[stemmer.stem(i) for i in x])
#print(tokenized_tweet)
new_tweet=tokenized_tweet
#print(new_tweet)


#join all tokenized and stemmed tokens together
for i in range(len(tokenized_tweet)):
    tokenized_tweet[i]=' '.join(tokenized_tweet[i])
train['text'] = tokenized_tweet
#print(train['text'].head())

# removing https:// and URLs


   
    

#creating a .csv file storing values




#print(tweets)
def hashtag_extract(x):
    hashtag=[]
    for i in x:
        ht =re.findall(r"(\w+)", i)
        hashtag.append(ht)
        
    return hashtag

# extracting hashtags from tweets
HT_regular = hashtag_extract(train['text'])

cleaned_tweet=HT_regular
#print(cleaned_tweet)



HT_regular = sum(HT_regular,[])
import goslate
HT1_regular=list()
for word in HT_regular:
    #print(word)
    gs = goslate.Goslate()
    #new.append(gs.translate(word,'en'))
    HT1_regular.append(word)
    
#print(HT1_regular)

#Plotting  hastag
a = nltk.FreqDist(HT_regular)
a.plot(30)
d = pd.DataFrame({'Hashtag': list(a.keys()),
                  'Count': list(a.values())})
# selecting top 10 most frequent hashtags     
d = d.nlargest(columns="Count", n = 10) 
plt.figure(figsize=(15,5))
ax = sns.barplot(data=d, x= "Hashtag", y = "Count")
ax.set(ylabel = 'Count')

plt.savefig('/home/rrahul/Desktop/figure_1.png',dpi=100)
plt.show()

#Location
location=train['id']
#print(location)


bigram = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(new_tweet,5)
finder.apply_freq_filter(5)


#print(finder.nbest(bigram.likelihood_ratio, 10))


#applying tf-idf vectorizer

tfidf_vector=TfidfVectorizer(use_idf=True,ngram_range=(1,3))
tfidf_matrix = tfidf_vector.fit_transform(new_tweet)
feature_names = tfidf_vector.get_feature_names()
from sklearn.metrics.pairwise import cosine_similarity

#dist=1-cosine_similarity(tfidf_matrix)
#print(dist)

#clustering is done here
from sklearn.cluster import KMeans 
num_clusters=5
km=KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()
train['cluster_id']=clusters
print(train['cluster_id'].value_counts())

order_clusters = km.cluster_centers_.argsort()[:, ::-1]

from sklearn.cluster import KMeans 
num_clusters=5
km=KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()
train['cluster_id']=clusters
print(km)
print(train['cluster_id'].value_counts())

order_clusters = km.cluster_centers_.argsort()[:, ::-1] 

count2=0
for i in range(num_clusters):
    
    
    print("Clusters {}:Words ".format(i))
    for j in order_clusters[i, :10]: 
        count2=count2+1
        print(' %s' % feature_names[j])
        
print(count2)
