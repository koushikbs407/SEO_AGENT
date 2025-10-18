import requests
import json
import re

API_KEY = "AIzaSyD52atsJLgOx94avIYun3-gYYKn1Q160QM"

def call_gemini(prompt):
    """Generic function to call Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            return None
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def step1_generate_titles(keyword):
    """Step 1: Generate 3 candidate titles"""
    prompt = f"Generate exactly 3 SEO-friendly blog titles (max 60 chars) for '{keyword}'. Return only the titles, numbered 1-3."
    
    response = call_gemini(prompt)
    if not response:
        return []
    
    titles = []
    for line in response.split('\n'):
        cleaned = re.sub(r'^[\d\.\-\*\)]+\s*', '', line.strip())
        cleaned = re.sub(r'[\*\"]+', '', cleaned)
        if cleaned:
            titles.append(cleaned)
    
    return titles[:3]

def step2_evaluate_titles(keyword, titles):
    """Step 2: Evaluate each title for CTR and relevance"""
    titles_text = '\n'.join([f"{i+1}. {title}" for i, title in enumerate(titles)])
    
    prompt = f"""Evaluate these titles for keyword '{keyword}' on CTR potential and relevance (score 1-10):

{titles_text}

Return format:
Title 1: [score] - [reason]
Title 2: [score] - [reason] 
Title 3: [score] - [reason]"""
    
    response = call_gemini(prompt)
    if not response:
        return []
    
    evaluations = []
    for line in response.split('\n'):
        if 'Title' in line and ':' in line:
            try:
                score_part = line.split(':')[1].strip()
                score = int(score_part.split()[0])
                reason = ' '.join(score_part.split()[2:])
                evaluations.append({'score': score, 'reason': reason})
            except:
                evaluations.append({'score': 5, 'reason': 'Default evaluation'})
    
    return evaluations[:3]

def step3_select_best(keyword, titles, evaluations):
    """Step 3: Select the best title"""
    eval_text = '\n'.join([f"{i+1}. {titles[i]} (Score: {evaluations[i]['score']}) - {evaluations[i]['reason']}" 
                          for i in range(len(titles))])
    
    prompt = f"""Based on these evaluations for keyword '{keyword}':

{eval_text}

Select the best title number (1, 2, or 3) and explain why. Return format:
Best: [number]
Reason: [explanation]"""
    
    response = call_gemini(prompt)
    if not response:
        return titles[0] if titles else "", "Default selection"
    
    try:
        best_num = int(re.search(r'Best:\s*(\d)', response).group(1))
        reason = re.search(r'Reason:\s*(.+)', response).group(1)
        return titles[best_num-1], reason
    except:
        return titles[0] if titles else "", "Default selection"