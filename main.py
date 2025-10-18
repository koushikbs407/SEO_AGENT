import pandas as pd
import time
from llm_service import step1_generate_titles, step2_evaluate_titles, step3_select_best


def read_csv(filepath):
    """
    Reads a CSV file and returns a pandas DataFrame.
    """
    try:
        df = pd.read_csv(filepath)
        print(f"[SUCCESS] Successfully loaded {len(df)} keywords from {filepath}\n")
        return df
    except FileNotFoundError:
        print(f"[ERROR] File '{filepath}' not found")
        return None
    except Exception as e:
        print(f"[ERROR] Error reading CSV: {e}")
        return None


def save_results(results, output_file="output_results.csv"):
    """
    Saves results (list of dicts) to a CSV file.
    """
    try:
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        print(f"\n[SUCCESS] Results saved to {output_file}")
    except Exception as e:
        print(f"\n[ERROR] Error saving results: {e}")


if __name__ == "__main__":
    # 1️⃣ Read input file
    df = read_csv("blog_ideas.csv")

    if df is None:
        print("Error reading file. Please check if 'blog_ideas.csv' exists.")
        exit()

    # 2️⃣ Validate the column name
    if 'keyword' not in df.columns:
        print(f"[ERROR] 'keyword' column not found. Available columns: {list(df.columns)}")
        exit()

    print("First few rows of your data:")
    print(df.head())
    print("\n" + "="*70)
    print("[START] STARTING TITLE GENERATION AND EVALUATION")
    print("="*70)

    results = []

    # 3️⃣ Process each keyword one by one
    for idx, keyword in enumerate(df['keyword'], 1):
        print(f"\n[{idx}/{len(df)}] Processing keyword: {keyword}")
        print("-" * 70)

        # Step 1: Generate 3 candidate titles
        print("Step 1: Generating titles...")
        titles = step1_generate_titles(keyword)
        
        if not titles:
            print(f"[WARNING] No titles generated for '{keyword}'. Skipping...")
            results.append({
                'keyword': keyword,
                'title_1': '',
                'title_2': '',
                'title_3': '',
                'best_title': '',
                'best_score': 0,
                'status': 'failed'
            })
            continue
        
        print(f"Generated titles: {titles}")
        
        # Step 2: Evaluate each title
        print("Step 2: Evaluating titles...")
        evaluations = step2_evaluate_titles(keyword, titles)
        
        # Step 3: Select best title
        print("Step 3: Selecting best title...")
        best_title, selection_reason = step3_select_best(keyword, titles, evaluations)
        
        print(f"Selected: {best_title}")
        print(f"Reason: {selection_reason}")

        # Save results
        result = {
            'keyword': keyword,
            'title_1': titles[0] if len(titles) > 0 else '',
            'title_2': titles[1] if len(titles) > 1 else '',
            'title_3': titles[2] if len(titles) > 2 else '',
            'best_title': best_title,
            'best_score': evaluations[0]['score'] if evaluations else 0,
            'selection_reason': selection_reason,
            'status': 'success'
        }

        results.append(result)

        # Add 1-second delay between API calls (safety for rate limits)
        if idx < len(df):
            time.sleep(1)

    # 4️⃣ Save all results
    save_results(results)

    # 5️⃣ Print summary
    print("\n" + "="*70)
    print("[COMPLETE] PROCESSING COMPLETE - SUMMARY")
    print("="*70)
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = len(results) - successful
    print(f"Total keywords processed: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("="*70)
