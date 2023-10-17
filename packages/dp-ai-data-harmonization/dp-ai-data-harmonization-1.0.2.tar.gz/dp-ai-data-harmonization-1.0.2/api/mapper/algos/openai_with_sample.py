import io
import logging

import openai
import pandas as pd
from django.conf import settings

logger = logging.getLogger(__name__)


class OpenAI:
    def __init__(self, key) -> None:
        self.key = key
    engine = "text-davinci-003"
    header1 = ""
    header2 = ""
    data1 = ""
    data2 = ""
    prompt = (
        f"This is Table 1:\n{header1}\n{data1}\nThis is Table 2:\n{header2}\n{data2}\nMap rows of Table 1 to Table 2 and put them in a single Table and add a column of confidence in this between 0 and 1.\n\n")

    def invoke(self, df1, df2,sample_harmonized_data):
        # print("type of df1", type(df1))
        # print("type of df2", type(df2))
        self.header1 = df1.columns.str.cat(sep=',')
        self.header2 = df2.columns.str.cat(sep=',')
        self.data1 = df1.apply(lambda x: ' , '.join(x.astype(str)), axis=1).to_string(index=False)
        self.data2 = df2.apply(lambda x: ' , '.join(x.astype(str)), axis=1).to_string(index=False)
        self.prompt = (
            f"Here is the sample of harmonized data:\n"
            f"{sample_harmonized_data}\n"
            f"This is Table 1:\n{self.header1}\n{self.data1}\nThis is Table 2:\n{self.header2}\n{self.data2}\nMap rows of Table 1 to Table 2 according to the sample harmonized data and put them in a single Table in csv format with same column order.\n"
            )
        openai.api_key = self.key
        # print("prompt: ", self.prompt)
        response = openai.Completion.create(
            engine=self.engine,
            prompt=self.prompt,
            temperature=0.1,
            max_tokens=2048,
            top_p=0.7,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            stop=["\n\n"]
        )

        # print("Response: ", response.choices[0].text.split(":")[-1])
        # print("Response: ", response.choices[0].text.split(":")[-1])
        output_df = pd.read_csv(io.StringIO(response.choices[0].text), delimiter=",")
        output_df.reset_index(drop=True, inplace=True)
        # print(output_df.to_json())
        return output_df.to_json()
