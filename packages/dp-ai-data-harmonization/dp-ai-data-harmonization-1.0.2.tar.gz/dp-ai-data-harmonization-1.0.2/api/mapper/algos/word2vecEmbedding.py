import pandas as pd
from gensim.models import Word2Vec
import chromadb

class Word2VecEmbedding:
    def __init__(self, word2vec_model=None):
        if word2vec_model is None:
           
            self.word2vec_model = Word2Vec(min_count=1)
        else:
            self.word2vec_model = word2vec_model

    def train_word2vec_model(self, sentences):
        if self.word2vec_model.wv.key_to_index:
           
            self.word2vec_model.build_vocab(sentences, update=True)
            self.word2vec_model.train(sentences, total_examples=len(sentences), epochs=10)
        else:
            
            self.word2vec_model.build_vocab(sentences)
            self.word2vec_model.train(sentences, total_examples=len(sentences), epochs=10)

    def get_embedding(self, row):
        words = [str(val) for val in row.tolist() if not pd.isnull(val)]
        if not words:
            return None
        embedding = self.word2vec_model.wv[words]
        return embedding.mean(axis=0).tolist() if len(embedding) > 0 else None

    def invoke(self, df1, df2):
        sentences_df1 = [row.tolist() for _, row in df1.iterrows()]
        self.train_word2vec_model(sentences_df1)

        chroma_client = chromadb.Client()
        collection = chroma_client.create_collection(name="wordVec")

        embeddings_df1 = []
        documents_df1 = []
        metadatas_df1 = []
        ids_df1 = []
        for i, row in df1.iterrows():
            embedding = self.get_embedding(row)
            if embedding:
                embeddings_df1.append(embedding)
                documents_df1.append(' '.join(map(str, row.tolist())))
                metadatas_df1.append({"source": "my_source"})
                ids_df1.append(str(row.name))
        collection.add(embeddings=embeddings_df1, documents=documents_df1, metadatas=metadatas_df1, ids=ids_df1)

        sentences_df2 = [row.tolist() for _, row in df2.iterrows()]
        self.train_word2vec_model(sentences_df2)

        embeddings_df2 = []
        documents_df2 = []
        ids_df2 = []
        for i, row in df2.iterrows():
            embedding = self.get_embedding(row)
            if embedding:
                embeddings_df2.append(embedding)
                documents_df2.append(' '.join(map(str, row.tolist())))
                ids_df2.append(str(row.name))

        similarities = collection.query(
            query_embeddings=embeddings_df2,
            n_results=1,
        )
        similar_ids = similarities['ids']

        mapping = [int(item) for sublist in similar_ids for item in sublist]
        selected_rows_df1 = df1.loc[mapping]
        selected_rows_df1.reset_index(drop=True, inplace=True)

        if set(df1.columns) == set(df2.columns):
            df2.columns = [f"{col}_copy" for col in df2.columns]

        concatenated_df = pd.concat([df2, selected_rows_df1], axis=1)
        concatenated_df.reset_index(drop=True, inplace=True)
        return concatenated_df.to_json()
