import requests
import pymorphy2
import gensim
import gensim.corpora as corpora
import pyLDAvis.gensim
 
code = """return API.wall.get({
   "owner_id": "",
   "domain": "itmoru",
   "offset": 0,
   "count": 100,
   "filter": "owner",
   "extended": 0,
   "fields": "",
   "v": "5.103"
});"""
 
response = requests.post(
    url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": vk['access_token'],
            "v": "5.103"
        }
)
 
items = response.json()['response']['items']
wall_texts = []
for item in items:
    wall_texts.append(item['text'])
 
def pos(word, morph=pymorphy2.MorphAnalyzer()):
    'Возвращает часть речи полученного слова'
    return morph.parse(word)[0].tag.POS
 
def form(word, morph = pymorphy2.MorphAnalyzer()):
    'Возвращает начальную форму полученного слова'
    p = morph.parse(word)[0]
    return(p.normal_form)
 
functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'} # Список обозначений частей речи стоп-слов
alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
ready_texts = []
for text in wall_texts:
    clean = []
    words = text.split()
    for word in words:
        word = "".join(sym for sym in word if sym in alph)
        if pos(word) not in functors_pos and word != '':
            clean.append(form(word))
    ready_texts.append(clean)
 
 
# Create Dictionary
id2word = corpora.Dictionary(ready_texts)
 
# Create Corpus: Term Document Frequency
corpus = [id2word.doc2bow(text) for text in ready_texts]
 
# Build LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=5,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=10,
                                           passes=10,
                                           alpha='symmetric',
                                           iterations=100,
                                           per_word_topics=True)
