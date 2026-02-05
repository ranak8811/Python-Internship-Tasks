import re
from db import get_phone_by_model, get_all_phones
from helpers import clean_price, clean_battery, clean_camera, extract_models_from_question

# Agent 1 – Data Extractor
def data_extractor(question):
    try:
        question_lower = question.lower()
        
        # Intent: recommendation based on price
        if "best" in question_lower and ("under" in question_lower or "budget" in question_lower or "cheap" in question_lower):

            currency_match = re.search(r'(?:under|below|budget)\s*\$?\s*(\d+)', question_lower)
            limit = float(currency_match.group(1)) if currency_match else 10000.0
            
            target = "price"
            if "battery" in question_lower:
                target = "battery"
            elif "camera" in question_lower or "photography" in question_lower:
                target = "camera"
            
            df = get_all_phones()
            return {
                "intent": "recommendation",
                "target": target,
                "limit": limit,
                "data": df
            }

        # Intent: find best battery phone
        elif "best battery" in question_lower:
             df = get_all_phones()
             return {"intent": "recommendation", "target": "battery", "limit": None, "data": df}

        # Intent: comparison
        if "compare" in question_lower or "vs" in question_lower or "better" in question_lower:
             models = extract_models_from_question(question)
             
             data = [get_phone_by_model(m) for m in models if not get_phone_by_model(m).empty]
             if len(data) >= 2:
                 return {"intent": "compare", "data": data}
        
        # Intent: specific Specs
        models = extract_models_from_question(question)
        if models:
            phone_data = get_phone_by_model(models[0])
            if not phone_data.empty:
                return {
                    "intent": "specs",
                    "data": phone_data
                }

        return {"intent": "unknown", "data": None}

    except Exception as e:
        print(f"Error in data_extractor: {e}")
        return {"intent": "error", "error": str(e)}

# Agent 2 – Review Generator
def review_generator(intent_data):
    try:
        if isinstance(intent_data, str):
             return intent_data
             
        intent = intent_data.get("intent")
        data = intent_data.get("data")
        
        if intent == "error":
            return "Sorry, I encountered an error while processing your request."

        if intent == "unknown" or data is None:
            return "Sorry, I couldn't understand your question or find the specific model you mentioned."

        # specs
        if intent == "specs":
            row = data.iloc[0]
            price = clean_price(row.get('Price($)', ''))
            battery = clean_battery(row.get('Battery', ''))
            camera = clean_camera(row.get('Main Camera', ''))
            model_name = row.get('Model', 'Unknown Model')
            
            return (
                f"Here are the specs for the **{model_name}**:\n"
                f"- **Release Date**: {row.get('Release Date', 'N/A')}\n"
                f"- **Display**: {row.get('Display Size', 'N/A')}\n"
                f"- **Battery**: {battery} mAh\n"
                f"- **Main Camera**: {camera}\n"
                f"- **Price**: ${price if price else 'N/A'}"
            )

        # compare
        elif intent == "compare":
            p1 = data[0].iloc[0]
            p2 = data[1].iloc[0]
            
            p1_bat = clean_battery(p1.get('Battery', '')) or 0
            p2_bat = clean_battery(p2.get('Battery', '')) or 0
            
            p1_price = clean_price(p1.get('Price($)', '')) or 0
            p2_price = clean_price(p2.get('Price($)', '')) or 0

            comparison_text = f"Comparing **{p1['Model']}** and **{p2['Model']}**:\n"
            
            p1_cam = clean_camera(p1.get('Main Camera', ''))
            p2_cam = clean_camera(p2.get('Main Camera', ''))
            comparison_text += f"- **Camera**: **{p1['Model']}** has {p1_cam}, while **{p2['Model']}** has {p2_cam}.\n"
            
            comparison_text += f"- **Battery**: {p1['Model']} ({p1_bat} mAh) vs {p2['Model']} ({p2_bat} mAh).\n"
            comparison_text += f"- **Price**: ${p1_price} vs ${p2_price}.\n"
            
            if abs(p1_bat - p2_bat) > 500:
                better = p1['Model'] if p1_bat > p2_bat else p2['Model']
                comparison_text += f"-> For battery life, **{better}** is the clear winner.\n"
                
            return comparison_text

        # recommendation
        elif intent == "recommendation":
            df = data.copy()
            target = intent_data.get("target")
            limit = intent_data.get("limit")
            
            df['clean_price'] = df['Price($)'].apply(clean_price)
            df['clean_battery'] = df['Battery'].apply(clean_battery)
            
            if limit:
                df = df[df['clean_price'] <= limit]
                if df.empty:
                    return f"I couldn't find any Samsung phones under ${limit}."

            if target == "battery":
                df = df.dropna(subset=['clean_battery'])
                if df.empty:
                     return "No phones found with battery data."
                     
                best = df.sort_values('clean_battery', ascending=False).iloc[0]
                return (
                    f"The best Samsung phone for battery {'under $' + str(limit) if limit else ''} is the **{best['Model']}**.\n"
                    f"It packs a **{int(best['clean_battery'])} mAh** battery and costs **${best['clean_price']}**."
                )
            
            else:
                 df = df.dropna(subset=['clean_price'])
                 if df.empty:
                     return "No phones found with price data."

                 best = df.sort_values('clean_price', ascending=False).iloc[0]
                 cam_spec = clean_camera(best.get('Main Camera', ''))
                 return (
                    f"My recommendation {'under $' + str(limit) if limit else ''} is the **{best['Model']}**.\n"
                    f"- **Price**: ${best['clean_price']}\n"
                    f"- **Camera**: {cam_spec}\n"
                    f"- **Battery**: {clean_battery(best.get('Battery', ''))} mAh"
                )

        return "I'm not sure how to answer that request."

    except Exception as e:
        return f"Error generating review: {e}"