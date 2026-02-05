from agents import data_extractor, review_generator

def answer_question(question):
    extraction = data_extractor(question)
    return review_generator(extraction)
