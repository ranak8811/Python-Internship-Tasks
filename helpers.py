import re
import pandas as pd
from db import get_all_phones

def clean_price(price_str):

    if pd.isna(price_str) or price_str == "":
        return None
    try:
        first_val = str(price_str).split('/')[0].split(',')[0]
        cleaned = re.sub(r'[^\d.]', '', first_val)
        if cleaned:
            return float(cleaned)
        return None
    except ValueError:
        return None

def clean_battery(battery_str):

    if pd.isna(battery_str):
        return None
    match = re.search(r'(\d+)\s*mAh', str(battery_str), re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def clean_camera(camera_str):

    if pd.isna(camera_str):
        return "Unknown Camera"
    return str(camera_str).split(',')[0].strip()

def extract_models_from_question(question, all_models=None):

    if all_models is None:
        try:
            df_all = get_all_phones()
            if not df_all.empty and 'Model' in df_all.columns:
                all_models = df_all['Model'].tolist()
            else:
                all_models = []
        except Exception as e:
            print(f"Warning: Could not fetch models from DB: {e}")
            all_models = []

    found_models = []
    question_lower = question.lower()
    
    # sorting models by length (descending) to match longer specific names first
    all_models_sorted = sorted(all_models, key=len, reverse=True)

    for model in all_models_sorted:
        m_lower = model.lower()
        
        if m_lower in question_lower:
            found_models.append(model)
            continue

        short_name = m_lower.replace("samsung galaxy ", "").replace("samsung ", "").strip()
        
        if len(short_name) >= 2 and short_name in question_lower:
             found_models.append(model)
    
    final_models = []
    # sorting found by length (longest first)
    found_models.sort(key=len, reverse=True)
    
    for m in found_models:
        is_sub = False
        for existing in final_models:
            if m in existing: 
                is_sub = True
                break
        if not is_sub:
            final_models.append(m)
            
    return list(set(final_models))
