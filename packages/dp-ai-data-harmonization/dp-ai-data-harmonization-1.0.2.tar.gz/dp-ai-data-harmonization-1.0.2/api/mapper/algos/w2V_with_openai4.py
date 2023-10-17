import numpy as np
import pandas as pd

from api import settings
from api.mapper.algos.word2vecEmbedding import Word2VecEmbedding
from api.mapper.algos.openaiGPT4 import OpenAIGPT4

class W2VWithOpenAI4:
    def __init__(self, key):
        self.key = key
        self.table1_parts = None
        self.table2_parts = None
        self.parts_dict = {}

    def create_dict(self,table1_parts,table2_parts):
        ''' take dataframe from both the tables and create a dictionary of the columns
        '''

        for i in range(len(table1_parts)):

            self.parts_dict[i] = (table1_parts[i],table2_parts[i])

        return self.parts_dict

    def apply_openai(self):
        '''
        apply openai on the dictionary
        '''
        openAi = OpenAIGPT4(self.key)
        openai_parts = pd.DataFrame()
        columns = []
        for part in self.parts_dict:
            openai_part = openAi.invoke(self.parts_dict[part][0],self.parts_dict[part][1])
            openai_part = pd.read_json(openai_part)
            #drop index column
            openai_part.drop(columns=['index','Index'],inplace=True,errors='ignore')
            openai_part.reset_index(drop=True,inplace=True)
            
            openai_parts = pd.concat([openai_parts,openai_part],ignore_index=True,axis = 0)
            
        
        # n = len(openai_parts.columns) - n_columns
        # print(n)
        # print(openai_parts)
        print(openai_parts.columns)
        openai_parts.reset_index( inplace=True)
        # openai_parts = openai_parts.iloc[:, :-n]
        print(openai_parts.columns)

        openai_parts.drop(columns=['index'],inplace=True)
        # openai_parts.drop_duplicates(inplace=True)
        return openai_parts.to_json()


    def invoke(self,df1,df2):
        
        W2VEmbed = Word2VecEmbedding()
        df = pd.read_json(W2VEmbed.invoke(df1,df2))
        print("original",df)
        # split df into parts on the basis of the column length of df1 and df2
        table1_parts = df.iloc[:, :len(df2.columns)]
        table2_parts = df.iloc[:, len(df2.columns):]
        #split df into parts as per split size
        # print("\n\nt1parts\n",table1_parts)
        # print("\n\nt2parts\n",table2_parts)

        table1_parts = np.array_split(table1_parts,W2VWithOpenAI4.__get_split_size(len(table1_parts)))
        table2_parts = np.array_split(table2_parts, W2VWithOpenAI4.__get_split_size(len(table2_parts)))

        self.create_dict(table1_parts,table2_parts)

        # apply openai on the dictionary
        openai_parts = self.apply_openai()

        return openai_parts

    @staticmethod
    def __get_split_size(length):
        if length > 2*settings.SPLIT_SIZE:
            return settings.SPLIT_SIZE
        elif length >= settings.SPLIT_SIZE and length <= 2*settings.SPLIT_SIZE:
            return length//2
        else:
            return length//3
