    for pid in good_reviews:
        # Create a list of space-separated tokens for each good review
        good_review_tokens = [' '.join(review['tokens']) for review in good_reviews[pid]]

        # Use CountVectorizer to vectorize the tokens
        vectorizer = CountVectorizer()
        doc_term_matrix = vectorizer.fit_transform(good_review_tokens)

        # Convert to binary presence/absence matrix
        binary_matrix = (doc_term_matrix > 0).astype(int)

        # Calculate counts of documents where each token appears
        token_counts = binary_matrix.sum(axis=0).A1

        # Get the feature names (tokens) and their counts
        token_to_count = dict(zip(vectorizer.get_feature_names_out(), token_counts))

        for review in good_reviews[pid]:
            sum_score = 0
            for token in review['tokens']:
                if token in token_to_count:
                    sum_score += token_to_count[token]  # Only add if token is present in token_to_count
            review['score'] = sum_score / len(review['tokens'])

        good_reviews[pid].sort(key = lambda x: -1 * x["score"])

        review_buffer = []
        for review in good_reviews[pid]:
            if len(review['tokens']) <= (1024 - len(review_buffer)):
                review_buffer += review['tokens']
            else:
                break

        out = {
            'PID': pid,
            'tokens': ' '.join(review_buffer)
        }


        json.dump(out, output_file)
        output_file.write('\n')