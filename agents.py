from db import get_phone_by_model, get_all_phones

def extract_models_from_question(question):
    models = []
    words = question.replace("?", "").split()

    for i in range(len(words) - 1):
        candidate = words[i] + " " + words[i + 1]
        if "galaxy" in candidate.lower():
            models.append(candidate)

    models = list(set(models))
    
    if "Samsung Galaxy" in models and len(models) > 1:
        models.remove("Samsung Galaxy")
        
    return models


def data_extractor(question):
    question_lower = question.lower()

    if "compare" in question_lower:
        models = extract_models_from_question(question)
        data = [get_phone_by_model(m) for m in models]
        return {"intent": "compare", "data": data}

    elif "best battery" in question_lower:
        df = get_all_phones()
        return {"intent": "recommend_battery", "data": df}

    else:
        models = extract_models_from_question(question)
        if models:
            return {
                "intent": "specs",
                "data": get_phone_by_model(models[0])
            }

    return {"intent": "unknown", "data": None}


def review_generator(intent, data):
    if intent == "specs":
        row = data.iloc[0]
        return (
            f"{row['Model']} was released on {row['Release Date']}. "
            f"It has a {row['Display Size']} display, "
            f"{row['Battery']} battery, "
            f"main camera: {row['Main Camera']}, "
            f"memory: {row['Memory']}, "
            f"priced at {row['Price']}."
        )

    elif intent == "compare":
        phone1 = data[0].iloc[0]
        phone2 = data[1].iloc[0]

        better_battery = (
            phone1['Model']
            if phone1['Battery'] > phone2['Battery']
            else phone2['Model']
        )

        return (
            f"{phone1['Model']} and {phone2['Model']} have similar displays. "
            f"{better_battery} offers better battery performance. "
            f"For photography and long usage, "
            f"{better_battery} is recommended."
        )

    elif intent == "recommend_battery":
        data["Battery_mAh"] = (
            data["Battery"].str.extract(r"(\d+)").astype(float)
        )
        best = data.sort_values(
            "Battery_mAh", ascending=False
        ).iloc[0]

        return (
            f"The Samsung phone with the best battery is {best['Model']} "
            f"with a {best['Battery']} battery, priced at {best['Price']}."
        )

    return "Sorry, I couldn't understand your question."
