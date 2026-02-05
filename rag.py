from agents import data_extractor, review_generator

def answer_question(question):

    try:
        if not question and not isinstance(question, str):
            return "Please enter a valid question."

        extracted_data = data_extractor(question)

        if not extracted_data or not isinstance(extracted_data, dict):
            return "Sorry, I couldn't extract any relevant information from your question."

        final_response = review_generator(extracted_data)
        
        if not final_response or not isinstance(final_response, str):
            return "Sorry, I encountered an error while generating the review."
        
        return final_response

    except Exception as e:
        return f"An error occurred: {str(e)}"
