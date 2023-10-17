import pandas as pd
from django.db import models
from api import settings
from api.mapper import algo_functions
# Create your models here.
# csv file that will be saved


class File(models.Model):
    file = models.FileField(upload_to='./files/')

    def save(self):
        # save file
        super().save()

    @classmethod
    def merge(cls, file1, file2, option):
        file1.save()
        file2.save()

        df1 = pd.read_csv(file1.file)
        df2 = pd.read_csv(file2.file)
        merged_text =""

        merge_options = {
            'ChatGPT': algo_functions.ai_merge,
            'GPT4': algo_functions.ai4_merge,
            'Fuzzy Wuzzy': algo_functions.fuzzy_merge,
            'Rapidfuzz': algo_functions.rapid_fuzzy_merge,
            'Jaro Winkler': algo_functions.stringmetric_merge,
            'JW Layered with ChatGPT': algo_functions.stringmetric_with_chatgpt_merge,
            'JW Layered with GPT4': algo_functions.stringmetric_with_gpt4_merge,
            'FW Layered with GPT4': algo_functions.fuzzywuzzy_with_gpt4_merge,
            'Recursive Data Harmonization': algo_functions.recursive_algo,
            'OPENAI Embedding':algo_functions.openai_embedding,
            'WORD2VEC Embedding':algo_functions.w2v_embed,
            'OAI Layered with GPT4':algo_functions.openai_with_gpt4,
            'W2V Layered with GPT4':algo_functions.word2vec_with_gpt4,
        }

        key = settings.OPENAI_KEY
        merge_func = merge_options.get(option, None)
        merged_text = merge_func(key, df1, df2)
        return merged_text
