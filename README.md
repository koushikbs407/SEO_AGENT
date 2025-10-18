# SEO Agent - Blog Title Generator

Automated SEO-friendly blog title generator using Google Gemini AI with 3-step intelligent evaluation system.

## Architecture

**Step 1**: Generate 3 candidate titles (≤60 chars) via LLM call
**Step 2**: Evaluate each title for CTR potential and keyword relevance via LLM call  
**Step 3**: Select best title based on evaluations via LLM call

## Features

- 3-step LLM pipeline for optimal title generation
- AI-powered CTR and relevance evaluation
- Batch processing from CSV input
- Detailed selection reasoning
- Export results to CSV

## Setup

1. Install dependencies:
```bash
pip install pandas requests
```

2. Add your Gemini API key in `llm_service.py`

3. Prepare input CSV with 'keyword' column

## Usage

```bash
python main.py
```

Input: `blog_ideas.csv` with keywords
Output: `output_results.csv` with all candidates and best selection

## Output Format

- `title_1`, `title_2`, `title_3` - Generated candidates
- `best_title` - AI-selected best title
- `best_score` - Evaluation score
- `selection_reason` - AI reasoning for selection

## Files

- `main.py` - Main execution script
- `llm_service.py` - 3-step LLM pipeline
- `evaluate_test.py` - Legacy evaluation logic
- `utility.py` - Helper functions