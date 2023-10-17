import openai
import pandas as pd
from api import settings
import io


class SampleBasedHarmonizationService:
    def __init__(self, openai_key):
        openai.api_key = openai_key
    
    def invoke(self, sample_harmonized_data, data1,data2):
        # Prompt GPT-3 to harmonize the new data based on the sample harmonized data
        prompt = (
            f"Here is the sample of harmonized data:\n"
            f"{sample_harmonized_data}\n"
            f"Given the following two datasets\n\n"
            f"Dataset 1:\n{data1}\n\n"
            f"Dataset 2:\n{data2}\n"
            f"Map rows of Dataset 1 to Dataset 2 according to the sample harmonized data and put them in a single Table in a csv format with a same column order:\n"
            f"Make sure the final output has all the columns."
        )
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Harmonize the given datasets according to the sample harmonized data."
            },
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4-0314",
            messages=messages,
            n=1,
            stop=None,
            temperature=0.1,
        )
        output_df = pd.read_csv(io.StringIO(response.choices[0]['message']['content']), delimiter=",")
        output_df.reset_index(drop=True, inplace=True)
        return output_df.to_json()
