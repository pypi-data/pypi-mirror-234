import pandas as pd
import chromadb
import openai


class OpenAIEmbedding:
    def __init__(self, key):
        self.key = key
        openai.api_key = self.key

    def get_embeddings(self, texts, model="text-embedding-ada-002"):
        embeddings = openai.Embedding.create(input=texts, model=model)['data']
        return [embedding['embedding'] for embedding in embeddings]

    def process_with_token_limit(self, df, max_tokens=4096, model="text-embedding-ada-002"):
        total_rows = len(df)
        embeddings = []
        processed_texts = []
        batch_texts = []

        for _, row in df.iterrows():
            text = ' '.join(map(str, row.tolist()))
            if len(' '.join(batch_texts)) + len(text) < max_tokens:
                batch_texts.append(text)
            else:
                embeddings.extend(self.get_embeddings(batch_texts, model=model))
                processed_texts.extend(batch_texts)
                batch_texts = [text]

        if batch_texts:
            embeddings.extend(self.get_embeddings(batch_texts, model=model))
            processed_texts.extend(batch_texts)

        return embeddings, processed_texts

    def invoke(self, df1, df2, max_tokens=4096):
        print("ENTERED IN OPENAI EMBEDDING")

        chroma_client = chromadb.Client()
        collection = chroma_client.create_collection(name="temp")



        embeddings1, documents1 = self.process_with_token_limit(df1, max_tokens=max_tokens)
        embeddings2, documents2 = self.process_with_token_limit(df2, max_tokens=max_tokens)

        metadatas1 = [{"source": "my_source"}] * len(documents1)
        ids1 = [str(row.name) for _, row in df1.iterrows()]

        collection.add(embeddings=embeddings1, documents=documents1, metadatas=metadatas1, ids=ids1)

        similarities = collection.query(
            query_embeddings=embeddings2,
            n_results=1,
        )

        similar_ids = similarities['ids']
        mapping = [int(item) for sublist in similar_ids for item in sublist]

        selected_rows_df1 = df1.loc[mapping].reset_index(drop=True)

        if set(df1.columns) == set(df2.columns):
            df2.columns = [f"{col}_copy" for col in df2.columns]

        concatenated_df = pd.concat([df2, selected_rows_df1], axis=1).reset_index(drop=True)

        return concatenated_df.to_json()
