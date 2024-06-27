#importing libraries
from openai import OpenAI
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup
import urllib.request  

client = OpenAI(
  api_key= '' #an API key needs to be entered here so it will work leaving my API key here would be a security risk
)

def _create_frequency_table(text_string) -> dict:   
    #removing stop words
    stop_words = set(stopwords.words("english"))
    
    words = word_tokenize(text_string)
    
    #reducing words to their root form
    stem = PorterStemmer()
    
    #creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table

def _calculate_sentence_scores(sentences, frequency_table) -> dict:   
    #algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        if(sentence_wordcount > 5): #in order to prevent very short sentences from being used in the summary (typically the "All Rights Reserved" or "Copyright of...")
            sentence_wordcount_without_stop_words = 0
            for word_weight in frequency_table:
                if word_weight in sentence.lower():
                    sentence_wordcount_without_stop_words += 1
                    if sentence[:99] in sentence_weight:
                        sentence_weight[sentence[:99]] += frequency_table[word_weight]
                    else:
                        sentence_weight[sentence[:99]] = frequency_table[word_weight]

            sentence_weight[sentence[:99]] = sentence_weight[sentence[:99]] / sentence_wordcount_without_stop_words

    return sentence_weight

def _calculate_average_score(sentence_weight) -> int:  
    #calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]
    #getting sentence average value from source text
    if(sum_values > 0):
        average_score = (sum_values / len(sentence_weight))
    else:
        average_score = 0
    return average_score

def _get_article_summary(sentences, sentence_weight, threshold, sentence_counter):
    article_summary = ''
    total_sentences = 0
    for sentence in sentences:
        if sentence[:99] in sentence_weight and sentence_weight[sentence[:99]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1
        total_sentences += 1
    output = [article_summary, sentence_counter, total_sentences]

    return output

def _run_article_summary(article, sentence_counter, threshold_multiplier):
    #creating a dictionary for the word frequency table
    frequency_table = _create_frequency_table(article)

    #tokenizing the sentences
    sentences = sent_tokenize(article)
    
    #algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    #getting the threshold
    threshold = _calculate_average_score(sentence_scores)
    default_threshold = threshold
    threshold *= threshold_multiplier
    #producing the summary
    while(sentence_counter < 8 or sentence_counter > 12): #range and method generates variability for the summary length it would be more efficient to just pick n most weighted sentences but this adds variability to make it seem more natural.
        output = _get_article_summary(sentences, sentence_scores, threshold, 0)
        total_sentences = output[2]
        if(output[2] < 8):
            article_summary = ""
            break
        article_summary = output[0]
        sentence_counter = output[1]
        if(sentence_counter < 8):
            threshold = default_threshold
            threshold_multiplier -= 0.001
            threshold *= threshold_multiplier
            sentence_counter = 0
        elif(sentence_counter > 12): 
            threshold = default_threshold
            threshold_multiplier += 0.001
            threshold *= threshold_multiplier
            sentence_counter = 0
    results = [article_summary, total_sentences]
    return results

if __name__ == '__main__':
    run_again = "Y"
    while (run_again.upper() == "Y"):
        too_short = False
        answer = input("Do you want to summarize a website or insert raw the text manually? (W = website, M = manual, N = quit)")
        inaccessible_website = False
        if(answer.upper() == "W"):
            website = input("Enter website url here:")
            raw_summary = input("Do you want to get the raw summary printed too? (Y/N)")
            #fetching the content from the URL
            try:
                fetched_data = urllib.request.urlopen(website)
                article_read = fetched_data.read()

                #parsing the URL content and storing in a variable
                article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')

                #returning <p> tags
                paragraphs = article_parsed.find_all('p')

                article_content = ''
                #looping through the paragraphs and adding them to the variable
                for p in paragraphs:  
                    article_content += p.text + " "
            
            except:
                inaccessible_website = True
                print("\n\nWebsite cannot be accessed try entering the text manually or using a different website.")
    
        elif(answer.upper() == "M"): #allows user to manually enter text to be summarized if the website is inaccessible
            article_content = input("Input what you want to summarize here: (At least 15 sentences and remove ALL line breaks [or it will not work] using this website: https://www.textfixer.com/tools/remove-line-breaks.php)")
            raw_summary = input("Do you want to get the raw summary printed too? (Y/N)")

        elif(answer.upper() == "N"): #quits the program if the user changes their mind before picking a website or text to summarize
            break

        else: #if the website is inaccessible it will notify the user and bring them back to the beginning 
            inaccessible_website = True
        
        if(inaccessible_website == False):
            summary_results = _run_article_summary(article_content, 0, 1.5)
            total_sentences = summary_results[1]
            if(total_sentences < 8):
                print("\n\nThe website or text you are requesting to summarize is too short.")
                too_short = True
            if(raw_summary.upper() == "Y" and too_short == False):
                print("\n\n Raw Summary: \n\n" + summary_results[0])

            #Calling the AI model to clean up the summary
            if(too_short==False):
                print("\n\nAI Summary: \n\n")
                completion = client.chat.completions.create(
                    model="ft:gpt-3.5-turbo-1106:personal::8hUN2ApV",
                    messages=[
                        {"role": "system", "content": "Rewrite the following summary to make it as coherent as possible while maintaining its meaning and similar sentence count (make sure to make the summary as concise as possible) Remember to make it coherent so it sounds natural and not just like a bunch of sentences put next to each other. Make sure it has smooth transitions."},
                        {"role": "user", "content": summary_results[0]}
                    ],
                    max_tokens=512,
                    temperature=1,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0)
                print(completion.choices[0].message.content)
            
            run_again = input("\n\nDo you want to summarize again? (Y/N)")
    print("\n\n\n\n\n\nThank you for using TextSummarizer!")
