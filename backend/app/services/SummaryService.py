from transformers import pipeline
from typing import List

def batch_generateSummary(articles: List[str]) -> List[str]:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summaries = summarizer(articles, batch_size=4, min_length=30, max_length=150, do_sample=True, truncation=True)
    return [x['summary_text'] for x in summaries]


