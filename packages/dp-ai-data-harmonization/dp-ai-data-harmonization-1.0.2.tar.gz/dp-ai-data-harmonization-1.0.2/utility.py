import pandas as pd
from api.mapper.algo_functions import ( ai4_merge, ai_merge, fuzzy_merge,
                                rapid_fuzzy_merge, stringmetric_merge, stringmetric_with_chatgpt_merge,
                                stringmetric_with_gpt4_merge, fuzzywuzzy_with_gpt4_merge,
                                recursive_algo,openai_embedding,w2v_embed,openai_with_gpt4,word2vec_with_gpt4
                                )

from api.mapper.suggestion_based_algo_functions import (
                                sample_based_harmonization_service,
                                fuzzy_wuzzy_with_openai4,
                                jw_with_openai4,
                                jw_with_openai,
                                oai_with_openai4,
                                w2v_with_openai4
                                )
from api.mapper.algos.harmonization_with_suggestion_service import SampleBasedHarmonizationService
from api.mapper.algos.fw_with_openai4_with_sample import FWWithOpenAI4
from api.mapper.algos.jw_with_openai4_with_sample import JWWithOpenAI4
from api.mapper.algos.jw_with_openai_with_sample import JWWithOpenAI
from api.mapper.algos.oai_with_openai4_with_sample import OAIWithOpenAI4
from api.mapper.algos.w2v_with_openai4_with_sample import W2VWithOpenAI4

class DataHarmonizer:
    def __init__(self, key, file1_path, file2_path, option):
        self.key = key
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.option = option

    def merge_files(self):
        df1 = pd.read_csv(self.file1_path)
        df2 = pd.read_csv(self.file2_path)

        merge_options = {
            'ChatGPT': ai_merge,
            'GPT4': ai4_merge,
            'Fuzzy Wuzzy': fuzzy_merge,
            'Rapidfuzz': rapid_fuzzy_merge,
            'Jaro Winkler': stringmetric_merge,
            'JW Layered with ChatGPT': stringmetric_with_chatgpt_merge,
            'JW Layered with GPT4': stringmetric_with_gpt4_merge,
            'FW Layered with GPT4': fuzzywuzzy_with_gpt4_merge,
            'Recursive Data Harmonization': recursive_algo,
            'OpenAI Embedding' : openai_embedding,
            'Word2Vector Embedding' : w2v_embed,
            'OpenAI with GPT4' : openai_with_gpt4,
            'Word2Vector with GPT4' : word2vec_with_gpt4
        }

        merge_func = merge_options.get(self.option)
        if merge_func:
            merged_text = merge_func(self.key, df1, df2)
            return merged_text
        else:
            raise ValueError('Invalid merge option')


class DataHarmonizationWithSuggestion:
    def __init__(self, key, sample_file_path, file1_path, file2_path,option):
        self.key = key
        self.sample_file_path = sample_file_path
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.option = option

    def harmonize_data(self):
        # Read the sample harmonized data from the sample file
        sample_data = pd.read_csv(self.sample_file_path)

        # Read the two files that need to be harmonized
        data1 = pd.read_csv(self.file1_path)
        data2 = pd.read_csv(self.file2_path)
        print(1)
        print(data1.head())
        print(data2.head())
        print(self.option)
        # Invoke the SampleBasedHarmonizationService to harmonize the data
        harmonise_options = {
            "Default" : sample_based_harmonization_service,
            "Fuzzy Wuzzy with ChatGPT" : fuzzy_wuzzy_with_openai4,
            "Jaro Winkler with ChatGPT" : jw_with_openai4,
            "JW Layered with ChatGPT" : jw_with_openai,
            "OpenAI Layered with ChatGPT" : oai_with_openai4,
            "Word2Vec Layered with ChatGPT" : w2v_with_openai4

        }
        harmonize_func = harmonise_options.get(self.option)
        # harmonized_data = SampleBasedHarmonizationService(self.key).invoke(sample_data, data1, data2)
        if harmonize_func:
            harmonized_data = harmonize_func(self.key, sample_data, data1,data2)
            return harmonized_data
        else:
            raise ValueError('Invalid merge option')
