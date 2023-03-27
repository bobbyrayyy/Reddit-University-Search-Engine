import requests
import pandas as pd

solr_url = "http://localhost:8983/solr/new_core/select"

schools = ['ntu', 'nus', 'smu', 'sit', 'sutd']

def search(query):
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

    # Define the Solr API URL and query parameters
    params = {
        'q': formatted_query,
        'rows': 5,  # Top k=5 results
        'boost': 'product(Total_Score, score)' # Boost query by multiplying score with Post Score field

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
    return results
