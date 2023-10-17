from api.mapper.algos.harmonization_with_suggestion_service import SampleBasedHarmonizationService
from api.mapper.algos.fw_with_openai4_with_sample import FWWithOpenAI4
from api.mapper.algos.jw_with_openai4_with_sample import JWWithOpenAI4
from api.mapper.algos.jw_with_openai_with_sample import JWWithOpenAI
from api.mapper.algos.oai_with_openai4_with_sample import OAIWithOpenAI4
from api.mapper.algos.w2v_with_openai4_with_sample import W2VWithOpenAI4

def sample_based_harmonization_service(key,sample_data, data1, data2):
    sample_based_harmonization = SampleBasedHarmonizationService(key)
    text = sample_based_harmonization.invoke(sample_data, data1, data2)
    return text

def fuzzy_wuzzy_with_openai4(key,sample_data, data1, data2):
    fuzzy_wuzzy_openai4 = FWWithOpenAI4(key)
    text = fuzzy_wuzzy_openai4.invoke(data1, data2,sample_data)
    return text

def jw_with_openai4(key,sample_data, data1, data2):
    jw_with_openai4 = JWWithOpenAI4(key)
    text = jw_with_openai4.invoke(data1, data2,sample_data)
    return text

def jw_with_openai(key,sample_data, data1, data2):
    jw_with_openai = JWWithOpenAI(key)
    text = jw_with_openai.invoke(data1, data2,sample_data)
    return text

def oai_with_openai4(key,sample_data, data1, data2):
    oai_openai4 = OAIWithOpenAI4(key)
    text = oai_openai4.invoke(data1, data2,sample_data)
    return text

def w2v_with_openai4(key,sample_data, data1, data2):
    w2v_openai4 = W2VWithOpenAI4(key)
    text = w2v_openai4.invoke(data1, data2,sample_data)
    return text