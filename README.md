# SEO Agent - Blog Title Generator

Automated SEO-friendly blog title generator using Google Gemini AI with intelligent evaluation system.

## Features

- Generate 3 SEO-optimized titles per keyword using Gemini AI
- Intelligent title evaluation with scoring system
- Batch processing from CSV input
- Detailed evaluation reports
- Export results to CSV

## Setup

1. Install dependencies:
```bash
pip install pandas requests
```

2. Add your Gemini API key in `generate_titles.py`

3. Prepare input CSV with 'keyword' column

## Usage

```bash
python main.py
```

Input: `blog_ideas.csv` with keywords
Output: `output_results.csv` with generated titles and scores

## Scoring System

- +2 points: Contains target keyword
- +1 point: Optimal length (40-60 chars)
- +1 point: Contains power words
- +1 point: Includes numbers

## Files

- `main.py` - Main execution script
- `generate_titles.py` - Gemini AI integration
- `evaluate_test.py` - Title evaluation logic
- `utility.py` - Helper functions