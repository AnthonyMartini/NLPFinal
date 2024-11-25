import json

reviews = []


file_path = './Data/Subscription_Boxes.jsonl'
out_path = './Data/Subscription_Boxes_Out.jsonl'
words = []

# Open the input JSON file and read line by line
with open(file_path, 'r') as file:
    first = False
    for line in file:
        if(first == False):
            words = json.loads(line)['words']
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
    