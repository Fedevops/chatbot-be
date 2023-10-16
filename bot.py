import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time
from tools.tools import load_training_data, add_to_training_data


class SimpleSpacyBot:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")
        self.questions = []
        self.answers = []
        self.vectorizer = TfidfVectorizer()

    def train(self, qa_pairs):
        for pair in qa_pairs:
            if len(pair) != 2:
                print(f"Skipping problematic pair: {pair}")
                continue
            q, a = pair
            self.questions.append(q)
            self.answers.append(a)
        self.vectorizer.fit(self.questions)


    def respond(self, user_input):
        user_input_vectorized = self.vectorizer.transform([user_input])
        cosine_similarities = linear_kernel(user_input_vectorized, self.vectorizer.transform(self.questions)).flatten()
        closest_question_idx = cosine_similarities.argsort()[-1]
        return self.answers[closest_question_idx]
    
