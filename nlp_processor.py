import spacy


nlp = spacy.load("en_core_web_sm")

def perform_nlp(text):
    # Process the text using spaCy NLP pipeline
    doc = nlp(text)
    
    # Tokenization
    tokens = [token.text for token in doc]
    
    # Part-of-speech tagging
    pos_tags = [(token.text, token.pos_) for token in doc]
    
    # Named entity recognition
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    
    return tokens, pos_tags, entities
