import io
import logging

import openai
import pandas as pd
logger = logging.getLogger(__name__)


class OpenAIGPT4:
    def __init__(self, key) -> None:
        self.key = key    
    engine = "gpt-4-0314"
    header1 = ""
    header2 = ""
    data1 = ""
    data2 = ""
    prompt = (
        f"This is Table 1:\n{header1}\n{data1}\nThis is Table 2:\n{header2}\n{data2}\nMap rows of Table 1 to Table 2 and put them in a single Table and add a column of confidence in this between 0 and 1.\n\n")

    def invoke(self, df1, df2, sample_harmonized_data):
        # print("type of df1", type(df1))
        # print("type of df2", type(df2))
        self.header1 = df1.columns.str.cat(sep=',')
        self.header2 = df2.columns.str.cat(sep=',')
        self.data1 = df1.apply(lambda x: ' , '.join(x.astype(str)), axis=1).to_string(index=False)
        self.data2 = df2.apply(lambda x: ' , '.join(x.astype(str)), axis=1).to_string(index=False)
        self.prompt = (
            f"Here is the sample of harmonized data:\n"
            f"{sample_harmonized_data}\n"
            f"Given the following two datasets\n\n"
            f"This is Dataset 1:\n{self.header1}\n{self.data1}\nThis is Dataset 2:\n{self.header2}\n{self.data2}\n."
            f"Map rows of Dataset 1 to Dataset 2 according to the sample harmonized data and put them in a single Table in a csv format with a same column order:\n"
        )
        openai.api_key = self.key
        # print("prompt: ", self.prompt)
        messages = [
            {"role": "system",
             "content": "You are a data analyst. Just give only output not extra text with that."},
            {"role": "user", "content": self.prompt}

        ]

        response = openai.ChatCompletion.create(
            model="gpt-4-0314",
            messages=messages,
            n=1,
            stop=None,
            temperature=0.5,
            # top_p=0.9,
            # frequency_penalty=0,
            # presence_penalty=0
        )

        # print("Response: ", response.choices[0].text.split(":")[-1])
        # print("Response: ", response.choices[0].text.split(":")[-1])
        # print(response)
        output_df = pd.read_csv(io.StringIO(response.choices[0]['message']['content']), delimiter=",")
        output_df.reset_index(drop=True, inplace=True)
        # print(output_df.to_json())
        return output_df.to_json()
