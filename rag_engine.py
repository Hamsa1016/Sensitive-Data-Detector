from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGEngine:

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.chunks = []
        self.matrix = None

    def chunk_text(self, text, chunk_size=250):

        words = text.split()

        self.chunks = [
            " ".join(words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size)
        ]

    def build_index(self, text):

        self.chunk_text(text)

        self.matrix = self.vectorizer.fit_transform(self.chunks)

    def search(self, query, top_k=2):

        query_vector = self.vectorizer.transform([query])

        similarity = cosine_similarity(query_vector, self.matrix).flatten()

        top_indices = similarity.argsort()[-top_k:][::-1]

        return [self.chunks[i] for i in top_indices]