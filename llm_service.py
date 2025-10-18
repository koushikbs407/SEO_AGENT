import requests
import json
import re

API_KEY = "your_api_key_here"

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
    
    prompt = f"""
You are an intelligent SEO title generator trained to create catchy, high-performing blog titles.

Your goal is to generate exactly **3 SEO-friendly blog titles** for the provided keyword.

### Rules
- Each title must be **≤ 60 characters**.
- Each title must **include the keyword** (or a natural variation).
- Titles should be **catchy, readable, and encourage clicks (CTR)**.
- Avoid unnecessary punctuation, special symbols, or emojis.
- **Output must be a pure JSON array** of strings — no explanations, no numbering, no extra text.

### Input
keyword: "{keyword}"

### Example
Input:
keyword: "python tips"

Output:
[
  "Python Tips for Beginners: Start Fast",
  "Top 7 Python Tips Every Beginner Should Know",
  "Quick Python Hacks: Tips to Speed Learning"
]

Now, generate the JSON array of 3 optimized titles for the input above.
"""

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
    """Step 2: Evaluate each title for CTR and keyword relevance"""

    # Format titles for context
    titles_json = json.dumps(titles, ensure_ascii=False, indent=2)

    prompt = f"""
You are an SEO evaluation assistant. Your task is to analyze blog titles for **click-through potential (CTR)** 
and **keyword relevance**.

### Instructions
1. Evaluate each title for two metrics:
   - **CTR_score** (1–10): How likely the title is to attract clicks.
   - **Keyword_relevance** (1–10): How well the title includes or relates to the keyword.
2. Consider factors like emotional appeal, clarity, and keyword placement.
3. Keep explanations short (1–2 sentences).
4. Return the output **strictly as JSON**, following the exact format below.

### Input
keyword: "{keyword}"
titles: {titles_json}

### Example Output
{{
  "evaluations": [
    {{
      "title": "Python Tips for Beginners: Start Fast",
      "CTR_score": 9,
      "Keyword_relevance": 10,
      "reason": "Strong action phrase and exact keyword usage."
    }},
    {{
      "title": "Top 7 Python Tips Every Beginner Should Know",
      "CTR_score": 8,
      "Keyword_relevance": 9,
      "reason": "Numbered list drives clicks and keyword fits naturally."
    }},
    {{
      "title": "Quick Python Hacks: Tips to Speed Learning",
      "CTR_score": 7,
      "Keyword_relevance": 8,
      "reason": "Good CTR appeal but partial keyword match."
    }}
  ]
}}

Now, evaluate the titles and return only the JSON object in the same format.
"""
    response = call_gemini(prompt)
    if not response:
        return []

    try:
        parsed = json.loads(response)
        return parsed.get("evaluations", [])
    except Exception as e:
        print("[WARNING] Parsing error:", e)
        # fallback if Gemini returns plain text
        return [
            {"title": t, "CTR_score": 5, "Keyword_relevance": 5, "reason": "Default evaluation"}
            for t in titles
        ]


def step3_select_best(keyword, titles, evaluations):
    """Step 3: Select the best title"""
    eval_text = '\n'.join([
        f"{i+1}. {titles[i]} (CTR: {evaluations[i].get('CTR_score', 5)}, Relevance: {evaluations[i].get('Keyword_relevance', 5)}) — {evaluations[i].get('reason', 'No reason')}" 
        for i in range(min(len(titles), len(evaluations)))
    ])

    prompt = f"""
You are an SEO expert. Below are 3 evaluated blog titles for the keyword: "{keyword}".

Each title has a score and reasoning:

{eval_text}

Task:
1. Analyze all titles carefully.
2. Select the single best title that would perform best for SEO and reader engagement.
3. Provide your reasoning clearly.

Response format (strictly follow this):
Best: [number of the best title]
Reason: [1–2 sentence explanation why this title is the best]
"""
    
    response = call_gemini(prompt)
    if not response:
        return titles[0] if titles else "", "Default selection"
    
    try:
        best_num = int(re.search(r'Best:\s*(\d)', response).group(1))
        reason = re.search(r'Reason:\s*(.+)', response).group(1)
        return titles[best_num-1], reason
    except:
        return titles[0] if titles else "", "Default selection"
