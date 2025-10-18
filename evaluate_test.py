import re

def evaluate_titles(keyword, titles):
    """
    Evaluate a list of titles and return the best one with reasoning.
    Scoring criteria:
    - +2 if title contains the keyword (case-insensitive)
    - +1 if title length is optimal (40-60 chars for SEO)
    - +1 if title has power words (Ultimate, Essential, Guide, Best, etc.)
    - +1 if title includes numbers
    Returns: best_title, reasoning (dictionary)
    """
    if not titles:
        return "", {"error": "No titles provided"}
    
    # Power words that increase clickability
    power_words = ['ultimate', 'essential', 'guide', 'best', 'top', 'complete', 
                   'proven', 'expert', 'simple', 'easy', 'quick', 'secrets', 'tips']
    
    best_score = -1
    best_title = ""
    all_evaluations = []
    reasoning = {}  # Initialize reasoning to avoid UnboundLocalError
    
    for title in titles:
        score = 0
        reasons = []
        
        # Clean the title (remove any lingering formatting)
        clean_title = re.sub(r'[\*\"]+', '', title.strip())
        
        # Check if keyword is in title (case-insensitive)
        if keyword.lower() in clean_title.lower():
            score += 2
            reasons.append("Contains target keyword")
        else:
            reasons.append("Missing target keyword")
        
        # Check length (optimal SEO length is 40-60 chars)
        title_length = len(clean_title)
        if 40 <= title_length <= 60:
            score += 1
            reasons.append(f"Optimal length ({title_length} chars)")
        elif title_length < 40:
            reasons.append(f"Too short ({title_length} chars)")
        else:
            reasons.append(f"Too long ({title_length} chars)")
        
        # Check for power words
        has_power_word = any(word in clean_title.lower() for word in power_words)
        if has_power_word:
            score += 1
            reasons.append("Contains power words")
        
        # Check for numbers (increases CTR)
        if re.search(r'\d+', clean_title):
            score += 1
            reasons.append("Includes numbers")
        
        # Store evaluation for this title
        evaluation = {
            "title": clean_title,
            "score": score,
            "length": title_length,
            "keyword_included": keyword.lower() in clean_title.lower(),
            "has_power_words": has_power_word,
            "has_numbers": bool(re.search(r'\d+', clean_title)),
            "reasons": reasons
        }
        all_evaluations.append(evaluation)
        
        # Update best title if score is higher
        if score > best_score:
            best_score = score
            best_title = clean_title
            reasoning = evaluation
    
    # If no clear winner, use first title as fallback
    if not best_title and titles:
        best_title = re.sub(r'[\*\"]+', '', titles[0].strip())
        reasoning = {
            "title": best_title,
            "score": 0,
            "length": len(best_title),
            "keyword_included": keyword.lower() in best_title.lower(),
            "has_power_words": False,
            "has_numbers": bool(re.search(r'\d+', best_title)),
            "reasons": ["Fallback selection - no scoring applied"]
        }
    
    # Add all evaluations to reasoning
    reasoning["all_evaluations"] = all_evaluations
    
    return best_title, reasoning


def print_evaluation_report(keyword, titles, best_title, reasoning):
    """
    Prints a formatted evaluation report for all titles.
    """
    print(f"\n{'='*70}")
    print(f"TITLE EVALUATION REPORT for keyword: '{keyword}'")
    print(f"{'='*70}\n")
    
    if "all_evaluations" in reasoning:
        for i, eval_data in enumerate(reasoning["all_evaluations"], 1):
            is_best = eval_data["title"] == best_title
            marker = " [BEST]" if is_best else ""
            
            print(f"{i}. {eval_data['title']}{marker}")
            print(f"   Score: {eval_data['score']}/5")
            print(f"   Length: {eval_data['length']} chars")
            print(f"   Analysis:")
            for reason in eval_data['reasons']:
                print(f"     • {reason}")
            print()
    
    print(f"{'='*70}")
    print(f"WINNER: {best_title}")
    print(f"Final Score: {reasoning.get('score', 0)}/5")
    print(f"{'='*70}\n")


# Test the function
if __name__ == "__main__":
    # Example usage
    test_keyword = "artificial intelligence"
    test_titles = [
        "AI Revolution: Understanding Artificial Intelligence",
        "The Ultimate Guide to Artificial Intelligence in 2025",
        "10 Essential AI Tips for Beginners"
    ]
    
    best, reasoning = evaluate_titles(test_keyword, test_titles)
    print_evaluation_report(test_keyword, test_titles, best, reasoning)