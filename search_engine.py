import requests
import pandas as pd
import contextualSpellCheck
import spacy

nlp = spacy.load("en_core_web_sm") 
contextualSpellCheck.add_to_pipe(nlp)

solr_url = "http://localhost:8983/solr/new_core/select"

schools = ['ntu', 'nus', 'smu', 'sit', 'sutd']

def search(query):
    # Get misspelt words
    doc = nlp(query)
    recommendation_spelling = doc._.suggestions_spellCheck
    # print(doc._.suggestions_spellCheck)
    
    original_sentence = query.split(' ')
    
    for key in recommendation_spelling:
        if str(key) not in schools:   
            for index, word in enumerate(original_sentence):
                if word == str(key):
                    original_sentence[index] = recommendation_spelling[key]
    
    print(' '.join(original_sentence))
    recommendation = ' '.join(original_sentence)

    # Search in both post title and comments
    formatted_query = "(Post_Title:" + str(query) + " OR Comment_Body:" + str(query) +")"  # to search in both posts and comments

    # Decide which subreddits to include in the search
    subs_to_include = []
    for school in schools:
        if school in query:
            subs_to_include.append(school)

    formatted_query += " AND (Subreddit:'sgexams'"
    if len(subs_to_include) > 0:
        for i in range(0, len(subs_to_include)):
            formatted_query += " OR Subreddit:" + subs_to_include[i]
    formatted_query += ")"

    # Define the query parameters
    params = {
        "defType": "edismax",
        'q': formatted_query,
        'rows': 5,  # Top k=5 results
        'fl': '*, score',
        "boost": "Total_Score"
    }

    try:
        # Send a GET request to the Solr API with the query parameters
        response = requests.get(solr_url, params=params)
        # Check the response status code
        if response.status_code == 200:
            # The request was successful
            # Parse the JSON response
            response_json = response.json()
            # Extract the search results from the response
            results = response_json.get("response", {}).get("docs", [])
        else:
            # The request failed
            print("Solr request failed with status code:", response.status_code)
            results = ['Failed']

    except requests.exceptions.RequestException as e:
        # An error occurred while sending the request
        print("Error sending Solr request:", e)
        results = ['Failed']
        
    print(pd.DataFrame(results))
    return results, recommendation
