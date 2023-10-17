import pandas as pd
from api.mapper.algos.openai import OpenAI


class RecursiveDataHarmonizer:
    def __init__(self, key):
        self.key = key

    def harmonize_data(self, df1, df2):
        """Recursively harmonizes two Pandas DataFrames."""
        openAi = OpenAI(self.key)
        openai_parts = None

        for column in df2.columns:
            column_df2 = pd.DataFrame(df2[column])
            if openai_parts is None: 
                openai_part = openAi.invoke(df1, column_df2)
            else:
                openai_part = openAi.invoke(openai_parts, column_df2)
            openai_part = pd.read_json(openai_part)
            openai_part.drop(columns=['index','Index'],inplace=True,errors='ignore')
            openai_part.reset_index(drop=True,inplace=True)

            openai_parts = pd.concat([openai_parts, openai_part],ignore_index=True,axis = 0)

        openai_parts.reset_index( inplace=True)
        openai_parts.drop(columns=['index'],inplace=True)
        openai_parts.drop_duplicates(inplace=True)
        return openai_parts.to_json()