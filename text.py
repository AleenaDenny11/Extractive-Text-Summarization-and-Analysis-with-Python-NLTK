import nltk
import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from tkinter import Tk, filedialog


def ensure_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')


def choose_file():
    root = Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=[("Text files", "*.txt")]
    )
    return file_path


def load_text(file_path):
    if not os.path.exists(file_path):
        print(" File not found.")
        return ""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def clean_tokens(tokens):
    stop_words = set(stopwords.words('english'))
    return [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

def analyze_text(text):
    if not text.strip():
        print(" Text is empty.")
        return

    print("\n Sentence Tokenization:")
    sentences = sent_tokenize(text)
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")

    print("\n Word Tokenization:")
    words = word_tokenize(text)
    print(words)

    print("\n Cleaned Words (no stopwords/punctuation):")
    cleaned = clean_tokens(words)
    print(cleaned)

    print("\n Top 5 Most Common Words:")
    freq = Counter(cleaned)
    for word, count in freq.most_common(5):
        print(f"{word}: {count}")

    summary = generate_summary(sentences, freq)
    print("\n Summary:")
    for sent in summary:
        print(sent)

def generate_summary(sentences, word_freq, summary_ratio=0.3):
    stop_words = set(stopwords.words('english'))
    sentence_scores = {}

    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        score = 0
        for word in words:
            if word in word_freq and word not in stop_words:
                score += word_freq[word]
        sentence_scores[sentence] = score

   
    ranked_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)


    select_count = max(1, int(len(sentences) * summary_ratio))
    selected = [sent for sent, score in ranked_sentences[:select_count]]

   
    summary = [sent for sent in sentences if sent in selected]
    return summary

if __name__ == "__main__":
    ensure_nltk_data()
    print("Please select a .txt file from the dialog box...")
    file_path = choose_file()
    if file_path:
        text = load_text(file_path)
        analyze_text(text)
    else:
        print(" No file was selected.")
