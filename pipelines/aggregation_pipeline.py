from collections import Counter

class AggregationPipeline:
    def run(self, processed_comments):
        if not processed_comments:
            return {
                "avg_sentiment": 0,
                "negative_ratio": 0,
                "top_topics": []
            }

        scores = [c["sentiment"]["score"] for c in processed_comments]
        topics = [c["topic"] for c in processed_comments]
        
        # Calculate stats
        avg_sentiment = sum(scores) / len(scores)
        negative_count = len([s for s in scores if s < -0.2]) # Threshold can be from config
        negative_ratio = negative_count / len(scores)
        
        # Get top topics
        top_topics = Counter(topics).most_common(5)
        # Format top topics as a list of strings for easier consumption or passed as dict
        # The prompt expects something readable.
        
        return {
            "avg_sentiment": avg_sentiment,
            "negative_ratio": negative_ratio,
            "top_topics": top_topics,
            "total_comments": len(processed_comments)
        }
