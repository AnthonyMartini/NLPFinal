import pandas as pd
from collections import Counter
from itertools import islice

# Function to generate trigrams
def generate_trigrams(text):
    words = text.split()
    trigrams = zip(words, islice(words, 1, None), islice(words, 2, None))
    return [' '.join(trigram) for trigram in trigrams]

def clean_string(text):
    return (text.lower()
            .replace("\n", " ")
            .replace(",","")
            .replace(";"," ")
            .replace("(","")
            .replace(")","")
            .replace("-"," ")
            .replace("—"," ")
            .replace('"','')
            .replace("“","")
            .replace("'",'')
            .replace("’s","")
            .replace("s’","")
            .replace(":","")
            .replace("!", "")
            .replace(".", "")
            .replace("?", "")
            .replace("[user]", "")
            .replace("[url]", "")
    )
# Load the CSV file
file_path = "./SexismDetector/Data/train.csv"  # Replace with the path to your CSV file
df = pd.read_csv(file_path)

# Initialize counters for trigrams
sexist_trigrams = Counter()
non_sexist_trigrams = Counter()

# Iterate through the rows and count trigrams based on the label
for _, row in df.iterrows():
    label = row["label_sexist"]
    
    trigrams = generate_trigrams(clean_string(row["text"]))
    if label == "sexist":
        sexist_trigrams.update(trigrams)
    elif label == "not sexist":
        non_sexist_trigrams.update(trigrams)

# Display the results
print("Top 10 trigrams in 'not sexist' comments:")
print(non_sexist_trigrams.most_common(10))

print("\nTop 10 trigrams in 'sexist' comments:")
print(sexist_trigrams.most_common(10))
