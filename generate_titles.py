import requests
import json
import re

# Your Gemini Pro API key
API_KEY = "AIzaSyD52atsJLgOx94avIYun3-gYYKn1Q160QM"

def generate_titles(keyword, original_title="", meta_description=""):
    """
    Calls Gemini Pro API to generate 3 SEO-friendly titles for a given keyword.
    Returns a list of titles.
    """
    # The prompt we send to the AI
    prompt = f"""
You are an expert SEO copywriter. Your task is to generate exactly 3 optimized blog titles 
for the given keyword and meta description.

### Rules:
1. Each title must be **SEO-friendly** and include the keyword or a natural variation.
2. Each title must be **≤ 60 characters**.
3. Avoid using excessive punctuation or emojis.
4. Be catchy but relevant — aim for high click-through potential.
5. Return the result as a **pure JSON array** of strings (no numbering, no explanation).

### Input:
keyword: "{keyword}"
original_title: "{original_title}"
meta_description: "{meta_description}"

### Example:
Input:
keyword: "python tips"
original_title: "Python tips for beginners"
meta_description: "Learn Python basics and practical tips to get started fast."

Output:
["Python Tips for Beginners: Start Fast",
 "Top 7 Python Tips Every Beginner Should Know",
 "Quick Python Hacks: Speed Up Your Learning"]

Now, produce the 3 optimized titles for the input above.
"""


    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    # Request payload for Gemini
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    # HTTP headers
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Make the API call
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return []
        
        # Convert response to JSON
        result = response.json()
        
        # Extract the text from Gemini's response structure
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        print(f"Raw response:\n{text}\n")  # Debug: see what we're getting
        
        # Split lines and clean them
        lines = text.split("\n")
        titles = []
        
        for line in lines:
            # Remove numbering (1., 2., 3., -, *, etc.) and clean whitespace
            cleaned = re.sub(r'^[\d\.\-\*\)]+\s*', '', line.strip())
            # Remove any markdown formatting like ** or quotes
            cleaned = re.sub(r'[\*\"]+', '', cleaned)
            
            # Only add non-empty lines
            if cleaned:
                titles.append(cleaned)
        
        # Return exactly 3 titles
        return titles[:3] if len(titles) >= 3 else titles
        
    except Exception as e:
        print(f"Error generating titles for {keyword}: {e}")
        return []
