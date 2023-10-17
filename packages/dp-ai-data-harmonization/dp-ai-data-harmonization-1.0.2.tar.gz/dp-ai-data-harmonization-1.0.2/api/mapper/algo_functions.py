from api.mapper.algos.fuzzywuzzy import FuzzyWuzzy
from api.mapper.algos.fw_with_openai4 import FWWithOpenAI4
from api.mapper.algos.jw_with_openai4 import JWWithOpenAI4
from api.mapper.algos.openai import OpenAI
from api.mapper.algos.openaiGPT4 import OpenAIGPT4
from api.mapper.algos.rapidfuzz import RapidFuzz
from api.mapper.algos.stringmetric import Stringmetric
from api.mapper.algos.jw_with_openai import JWWithOpenAI
from api.mapper.algos.recursive_harmonization import RecursiveDataHarmonizer
from api.mapper.algos.openai_embedding import OpenAIEmbedding
from api.mapper.algos.OAI_with_openai4 import OAIWithOpenAI4
from api.mapper.algos.w2V_with_openai4 import W2VWithOpenAI4


from api.mapper.algos.word2vecEmbedding import Word2VecEmbedding

def ai_merge(key, df1, df2):
    ########### AI code goes here ############
    openAI = OpenAI(key)
    text = openAI.invoke(df1, df2)
    ########### AI code ends here ############
    return text

def ai4_merge(key, df1, df2):
    ########### AI code goes here ############
    openAI4 = OpenAIGPT4(key)
    text = openAI4.invoke(df1, df2)
    ########### AI code ends here ############
    return text


def fuzzy_merge(key, df1, df2):
    fuzzywuzzy = FuzzyWuzzy()
    text = fuzzywuzzy.invoke(df1, df2)

    return text


def rapid_fuzzy_merge(key, df1, df2):
    fuzz = RapidFuzz()
    text = fuzz.invoke(df1, df2)

    return text


def stringmetric_merge(key, df1, df2):
    stringmetric = Stringmetric()
    text = stringmetric.invoke(df1, df2)

    return text


def stringmetric_with_chatgpt_merge(key, df1, df2):
    jw_with_openai = JWWithOpenAI(key)
    text = jw_with_openai.invoke(df1, df2)
    return text


def stringmetric_with_gpt4_merge(key, df1, df2):
    jw_with_openai = JWWithOpenAI4(key)
    text = jw_with_openai.invoke(df1, df2)
    return text


def fuzzywuzzy_with_gpt4_merge(key, df1, df2):
    fw_with_openai = FWWithOpenAI4(key)
    text = fw_with_openai.invoke(df1, df2)
    return text

def recursive_algo(key, df1, df2):
    rec_algo = RecursiveDataHarmonizer(key)
    text = rec_algo.harmonize_data(df1, df2)
    return text

def openai_embedding(key, df1, df2):
    embedding = OpenAIEmbedding(key)
    text = embedding.invoke(df1, df2)
    return text

def w2v_embed(key, df1, df2):
    word2vec = Word2VecEmbedding()
    text = word2vec.invoke(df1, df2)
    return text


def openai_with_gpt4(key, df1, df2):
    oai_gpt4 = OAIWithOpenAI4(key)
    text = oai_gpt4.invoke(df1, df2)
    return text

def word2vec_with_gpt4(key, df1, df2):
    w2v_gpt4 = W2VWithOpenAI4(key)
    text = w2v_gpt4.invoke(df1, df2)
    return text
