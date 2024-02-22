import os
import re

from promptsource.templates import Template, TemplateCollection

DS_TO_ENG_PROMPT = {
    "xcopa": "en",
    "Muennighoff/xstory_cloze": "en",
    "Muennighoff/xwinograd": "en",
    'GEM/wiki_lingua': 'en_en', # Contains correct language names
    'xnli': 'en',
    "paws-x": "en",
    "mlqa": "mlqa.en.en",
    "xquad": "xquad.en",
    "khalidalt/tydiqa-primary": "english",
    "khalidalt/tydiqa-goldp": "english",
    "pasinit/xlwic": "en",
    "GEM/xlsum": "english",
    "GEM/BiSECT": "en",
}

### ZH Datasets

"""
DATASETS = [
    ('xquad', 'xquad.zh'),
    # Context & Answer is in ZH
    ('mlqa', 'mlqa.zh.ar'),
    ('mlqa', 'mlqa.zh.vi'),
    ('mlqa', 'mlqa.zh.es'),
    ('mlqa', 'mlqa.zh.en'),
    ('mlqa', 'mlqa.zh.hi'),
    ('paws-x', 'zh'),
    ('clue', 'c3'),
    ('clue', 'cmrc2018'),
    ('clue', 'csl'),
    ('clue', 'drcd'),
    ('clue', 'tnews'),
    ('pasinit/xlwic', "xlwic_en_zh"),
    ('GEM/xlsum', "chinese_simplified"),
    # ('GEM/xlsum', "chinese_traditional"),
    # For WikiLingua there are already ZH prompts (except for xp3long prompts)
    ("xquad", )
]

LANG = "zh"
"""

### ES Datasets

"""
DATASETS = [
    ('xquad', 'xquad.es'),
    # Context & Answer is in ZH
    ('mlqa', 'mlqa.es.es'),
    ('paws-x', 'es'),
    ('GEM/xlsum', "spanish"),
    ('GEM/BiSECT', "es"),
    #('GEM/wiki_lingua', 'es'),
]
"""

LANG = "es"


### FR Datasets

"""
DATASETS = [
    #('xquad', 'xquad.fr'),
    # Context & Answer is in ZH
    #('mlqa', 'mlqa.es.es'),
    ('paws-x', 'fr'),
    ('GEM/xlsum', "french"),
    ('GEM/BiSECT', "fr"),
    #('GEM/wiki_lingua', 'fr'),
    ('pasinit/xlwic', "xlwic_fr_fr"),
]
"""

LANG = "fr"

### VI Datasets

"""
DATASETS = [
    ('xquad', 'xquad.vi'),
    # Context & Answer is in ZH
    ('mlqa', 'mlqa.vi.vi'),
    #('paws-x', 'vi'),
    ('GEM/xlsum', "vietnamese"),
    #('GEM/wiki_lingua', 'vi'),
LANGS = [
    #"id",
    #"sw",
    #"ta",
    #"vi",
    #"zh",
    "tr",
    "et",
    "ht",
    "th",
    "it",
    "qu",
]
"""

LANG = "vi"

### AR Datasets
"""
DATASETS = [
    ('xquad', 'xquad.ar'),
    # Context & Answer is in ZH
    ('mlqa', 'mlqa.ar.ar'),
    #('paws-x', 'vi'),
    #('GEM/BiSECT', "fr"),
    #('GEM/wiki_lingua', 'es'),
    ('khalidalt/tydiqa-primary', 'arabic'),
    ('khalidalt/tydiqa-goldp', 'arabic'),
]
LANGS = [
    "ar",
    "es",
    "eu",
    "hi",
    "id",
    "zh",
    "my",
    "ru",
    "sw",
    "te",
]

SOURCE_DATASET = TARGET_DATASET = "Muennighoff/xstory_cloze"
SOURCE_LANG = "en"

### XWINOGRAD
PROMPTS = [
    "Replace",
    "stand for",
    "True or False",
    "does underscore refer to",
    "underscore refer to",
]
LANG = "ar"
"""


# Choose datasets & lang, e.g.

DATASETS = [('GEM/xlsum', "chinese_traditional"),]
LANG = "zh-Hant"


# Path to key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/niklasmuennighoff/Desktop/gcp_translate_key.json"


def translate(target, text):
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    (pip install --upgrade google-api-python-client)
    pip install google-cloud-translate
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    # By default format_ is html, which would return &quot; instead of "
    result = translate_client.translate(text, source_language="en", target_language=target, format_="text")
    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    # If not providing source_language
    # print("Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]


def normalize_string(zh_string, en_string):
    """
    This is not specific to zh just to give an example & help Codex understand it :-)
    Replaces the content in brackets in zh_string with the content in brackets from en_string.
    All else is left the same in zh_string.
    Args:
        zh_string: {{前提}} 问题：{{假设}} 对、错或两者都不是？ ||| {{ answer_choices[标签] }}
        en_string: {{premise}} Question: {{hypothesis}} True, False, or Neither? ||| {{ answer_choices[label] }}
    Returns:
        zh_string_normalized: {{premise}} 问题：{{hypothesis}} 对、错或两者都不是？ ||| {{ answer_choices[label] }}
    """
    zh_string_normalized = zh_string
    # Find all the content in brackets in zh_string
    # For only double brackets {{(.*?)}}, but we do single brackets as well
    zh_bracket_content = re.findall(r"{(.*?)}", zh_string)
    # Find all the content in brackets in en_string
    # For only double brackets {{(.*?)}}, but we do single brackets as well
    en_bracket_content = re.findall(r"{(.*?)}", en_string)
    # Replace the content in brackets in zh_string with the content in brackets from en_string
    for i in range(len(zh_bracket_content)):
        zh_string_normalized = zh_string_normalized.replace(zh_bracket_content[i], en_bracket_content[i])
    return zh_string_normalized


template_collection = TemplateCollection()

for (ds_name, subset_name) in DATASETS:

    subset_name_eng = subset_name
    if ds_name in DS_TO_ENG_PROMPT:
        subset_name_eng = DS_TO_ENG_PROMPT[ds_name]

    source_templates = template_collection.get_dataset(ds_name, subset_name_eng)
    #for lang in LANGS:
    target_templates = template_collection.get_dataset(ds_name, subset_name)
    for uid, template in source_templates.templates.items():
        #if not("xp3long" in template.name.strip()):# not in PROMPTS:
        #    continue
        print(f"Translating {template.name.strip()} to {LANG}")
        answer_choices = []
        if template.answer_choices is not None:
            choices = template.answer_choices.split("|||")
            for c in choices:
                answer_choices.append(normalize_string(translate(LANG, c.strip()), c.strip()))
        or_jinja = template.jinja.strip()
        jinja = normalize_string(translate(LANG, or_jinja), or_jinja)
        template_name = template.name.strip() + f"_{LANG}mt"
        target_template = Template(
            template_name, jinja=jinja, reference="", answer_choices=" ||| ".join(answer_choices)
        )
        target_templates.add_template(target_template)
