from transformers import pipeline

def generateSummary(text: str) -> str:
    article_text = text
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(article_text, min_length=30, do_sample=False, truncation=True)
    return summary[0]['summary_text']