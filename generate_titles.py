import requests
import json
import re

# Your Gemini Pro API key
API_KEY = "AIzaSyD52atsJLgOx94avIYun3-gYYKn1Q160QM"

def generate_titles(keyword):
    """
    Calls Gemini Pro API to generate 3 SEO-friendly titles for a given keyword.
    Returns a list of titles.
    """
    # The prompt we send to the AI
    prompt = f"Generate exactly 3 SEO-friendly blog titles (max 60 chars) for the keyword: '{keyword}'. List them as simple numbered items."

    # Correct Gemini API endpoint
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
