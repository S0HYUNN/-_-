import json
from gensim.models import Word2Vec

keyword = ["봄", "셔츠"]
negative = ['직장인']
# 모델
model = Word2Vec.load("data_working/model/Word2Vec.model")
result = model.wv.most_similar(positive=keyword, negative=negative, topn=10)
ranking = json.dumps(result, ensure_ascii=False)
# print(ranking)
print(result[0][0])