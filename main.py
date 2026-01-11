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

def main():
    parser = argparse.ArgumentParser(description="Sentiment Intelligence System")
    parser.add_argument("--input", default="schemas/input_schema.json", help="Path to input JSON file")
    parser.add_argument("--output", default="output.json", help="Path to output JSON file")
    args = parser.parse_args()

    # Load input
    print(f"Loading input from {args.input}...")
    try:
        input_data = load_input(args.input)
    except FileNotFoundError:
        print(f"Error: Input file {args.input} not found.")
        return

    brand = input_data.get("brand")
    goal = input_data.get("company_goal")
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
