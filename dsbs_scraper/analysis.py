import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import re
nltk.download('stopwords')
nltk.download('wordnet')  
df = pd.read_csv("all_states.csv")
stop_words = set(stopwords.words('english'))

def is_word(word):
    return len(wordnet.synsets(word)) > 0


word_set = set()

for index, row in df.iterrows():
    paragraph = str(row['capabilities']).split(" ")
    for word in paragraph:
        phrase = re.sub(r'[^a-zA-Z]', ' ', word).split(" ")
        for w in phrase:
            if w == "":
                continue

            if is_word(w.lower()):
                word_set.add(w.lower())

clean_set = word_set-stop_words
for word in clean_set:
    print(word)


print(len(clean_set))

