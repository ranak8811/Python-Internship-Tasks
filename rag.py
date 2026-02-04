from agents import data_extractor, review_generator

def answer_question(question):
    extraction = data_extractor(question)
    intent = extraction["intent"]
    data = extraction["data"]

    return review_generator(intent, data)
