import spacy  # https://spacy.io

MODEL_NAME = 'en_core_web_md'

try:
    nlp = spacy.load(MODEL_NAME)
except OSError:
    spacy.cli.download(MODEL_NAME)
    nlp = spacy.load(MODEL_NAME)
