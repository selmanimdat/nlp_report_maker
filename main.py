import json
import os
import argparse
from pipelines.sentiment_pipeline import SentimentPipeline
from pipelines.aggregation_pipeline import AggregationPipeline
from pipelines.report_pipeline import ReportPipeline

def load_input(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_output(output, file_path):
    with open(file_path, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Output saved to {file_path}")

def main(args_list=None):
    parser = argparse.ArgumentParser(description="Sentiment Intelligence System")
    parser.add_argument("--input", default="schemas/input_schema.json", help="Path to input JSON file")
    parser.add_argument("--scraped-data", help="Path to scraped JSON file (e.g., 'web scraping /turk_telekom_sikayetler.json')")
    parser.add_argument("--output", default="output.json", help="Path to output JSON file")
    args = parser.parse_args(args_list)

    # Load input
    input_data = {}
    
    if args.scraped_data:
        print(f"Loading scraped data from {args.scraped_data}...")
        from services.data_loader import load_scraped_data
        scraped_data = load_scraped_data(args.scraped_data)
        if scraped_data:
             # Merge with default schema/overrides if needed
             # For now, we take the scraped comments and inferred brand
             input_data = scraped_data
             # Ensure defaults for missing fields
             if "company_goal" not in input_data:
                 input_data["company_goal"] = "Genel müşteri memnuniyeti ve şikayet analizi" # Default goal
    else:
        print(f"Loading input from {args.input}...")
        try:
            input_data = load_input(args.input)
        except FileNotFoundError:
            print(f"Error: Input file {args.input} not found.")
            return

    brand = input_data.get("brand", "Unknown Brand")
    goal = input_data.get("company_goal", "Genel Analiz")
    comments = input_data.get("comments", [])

    if not comments:
        print("No comments found in input.")
        return

    # Initialize pipelines
    sentiment_pipeline = SentimentPipeline()
    aggregation_pipeline = AggregationPipeline()
    report_pipeline = ReportPipeline()

    # 1. Sentiment & Topic Analysis
    print("Running Sentiment Pipeline...")
    processed_comments = sentiment_pipeline.run(comments)

    # 2. Aggregation
    print("Running Aggregation Pipeline...")
    stats = aggregation_pipeline.run(processed_comments)
    print(f"Stats: Avg Sentiment: {stats['avg_sentiment']:.2f}, Negative Ratio: {stats['negative_ratio']:.2f}")

    # 3. Report Generation
    print("Generating Report with Gemini...")
    final_report = report_pipeline.run(brand, goal, stats)

    # Save Output JSON
    save_output(final_report, args.output)
    
    # Save formatted markdown report
    report_content = final_report.get("report_markdown", "")
    if report_content:
        with open("report.md", "w") as f:
            f.write(report_content)
        print("Report saved to report.md")
        print("\n--- Report Preview ---")
        print(report_content[:500] + "...\n(See report.md for full content)")
        print("----------------------")
    else:
        print("Warning: No markdown report content generated.")


if __name__ == "__main__":
    main()
