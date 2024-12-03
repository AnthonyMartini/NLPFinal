import json
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import string

# Initialize an empty list to store the grouped reviews
reviews = []

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')

file_path = './Data/Subscription_Boxes.jsonl'
out_path = './Data/Subscription_Boxes_Out.jsonl'

# Open the input JSON file and read line by line
with open(file_path, 'r') as file:
    for line in file:
        # Parse the JSON object from each line
        json_obj = json.loads(line)
        
        # Get the review parameter from the JSON object
        rating = json_obj.get('rating',None)
        title = json_obj.get('title',None)
        text = json_obj.get('text',None)
        PID = json_obj.get('asin',None)
        
        # If the review exists, add it to the grouped reviews list
        if rating:
            reviews.append({
                'PID' : PID,
                'rating': rating,
                'title': title,
                'text' : text,
                'tokens':[]
                })
            
# Prepare a translation table to remove punctuation
translator = str.maketrans('', '', string.punctuation)
            
# Tokenize and clean the reviews
words = []

for review in reviews:
    # Tokenize the review text
    tokens = word_tokenize(review['text'].lower())
    
    # Remove punctuation and keep only alphabetic words
    cleaned_tokens = [word.translate(translator) for word in tokens if word.isalpha()]

    review['tokens'] = cleaned_tokens
    
    # Add the cleaned tokens to the words list
    words.extend(cleaned_tokens)

# Use Counter to count the frequency of each word
word_counts = Counter(words)

# Get the 100 most common words --> becomes the stop list
most_common_words = [word for word,count in word_counts.most_common(10)]
print(most_common_words)

for review in reviews:
    review['tokens'] = [token for token in review['tokens'] if token not in most_common_words]



# Write the grouped reviews to a new file
with open(out_path, 'w') as output_file:
   # json.dump({'words:':word_counts},output_file)
    #output_file.write('\n')
    for review in reviews:
        if review['tokens'] != []:
            json.dump(review, output_file)
            output_file.write('\n')

print("Grouped reviews have been written to 'grouped_reviews.json'.")
