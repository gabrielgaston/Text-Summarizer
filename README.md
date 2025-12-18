# TextSummarizer (Python)

A command-line text and website summarization tool that combines **classical NLP techniques** with an **OpenAI language model** to generate concise, coherent summaries from long-form content.

---

## Overview

TextSummarizer extracts meaningful sentences from large bodies of text using word frequency scoring and sentence weighting, then optionally refines the result using an OpenAI model to produce a more natural, readable summary.

The program supports:

* Summarizing **entire websites** (by scraping paragraph text)
* Summarizing **manually entered text**
* Producing both a **raw extractive summary** and an **AI-refined summary**

---

## Features

* Website scraping via `urllib` and `BeautifulSoup`
* Tokenization, stemming, and stop-word removal using **NLTK**
* Sentence scoring based on word frequency
* Adaptive thresholding to target a summary length of **8–12 sentences**
* Optional OpenAI-powered rewriting for improved coherence
* Interactive command-line interface

---

## How It Works

### 1. Text Collection

* Website mode: Extracts text from all `<p>` tags on a given URL
* Manual mode: Accepts raw text input from the user

### 2. Extractive Summarization (NLTK)

* Removes stop words
* Applies Porter stemming
* Builds a word frequency table
* Scores sentences based on weighted word presence
* Selects sentences above a dynamic threshold

### 3. AI Refinement (Optional)

* Sends the extracted summary to an OpenAI fine-tuned model
* Rewrites the summary for clarity, flow, and coherence
* Maintains similar sentence count and meaning

---

## Requirements

* Python 3.8+
* NLTK
* BeautifulSoup4
* OpenAI Python SDK

Install dependencies:

```bash
pip install nltk beautifulsoup4 openai
```

NLTK setup (run once):

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

---

## Configuration

An OpenAI API key is required for AI refinement.

Insert your key in the script:

```python
client = OpenAI(api_key="YOUR_API_KEY_HERE")
```

The program will still run without AI refinement, but only the raw extractive summary will be meaningful.

---

## Usage

Run the program:

```bash
python text_summarizer.py
```

### Options

* **W** - Summarize a website
* **M** - Manually enter text
* **N** - Quit the program

You may also choose whether to display:

* Raw extractive summary
* AI-refined summary

---

## Notes & Limitations

* Input text must contain **at least ~15 sentences**
* Manual input must be **single-line text** (no line breaks)
* Very short articles cannot be summarized reliably
* Website scraping depends on page accessibility and structure

---

## Example Use Cases

* Summarizing news articles
* Condensing academic or technical writing
* Quickly understanding long web pages
* NLP coursework or experimentation

---

## Author

Gabriel Gaston

---

## Disclaimer

This project is intended for educational and personal use. Website content is summarized as-is, and users are responsible for complying with website terms of service.
