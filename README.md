This program scans the entered website for its p elements and then uses an extraction-based summarization algorithm to pick the most important sentences as a raw summary. This raw summary is then sent to a fine-tuned OpenAI gpt 3.5 turbo 1106 model that then cleans up the summary and makes it more coherent.

The program also allows for raw user input in the case that the website is inaccessible where the user can manually type or copy and paste the text for it to summarize.
