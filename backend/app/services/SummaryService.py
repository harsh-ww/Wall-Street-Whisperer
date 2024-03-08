from transformers import pipeline

def generateSummary(text: str) -> str:
    article_text = text
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(article_text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']