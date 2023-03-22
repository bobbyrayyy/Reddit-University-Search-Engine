import requests

solr_url = "http://localhost:8983/solr/new_core/select"

def search(query):
    # Define the Solr API URL and query parameters

    params = {
        'q': "Post_Title:" + query + " OR Commment_Body:" + query,  # to search in both posts and comments
        'rows': 100
        # 'fl': 'title, content',
        # 'wt': 'json'
    }

    # Send a POST request to the Solr API with the query parameters
    # response = requests.post(url, params=params)
    response = requests.get(solr_url, params=params)
    print(response)

    results = ['Failed']
    # Check the response status code
    if response.status_code == 200:
        # The request was successful
        # Parse the JSON response
        response_json = response.json()
        # Extract the search results from the response
        results = response_json.get("response", {}).get("docs", [])
        # Print the first search result
        if len(results) > 0:
            print(results[0])
    else:
        # The request failed
        print("Solr request failed with status code:", response.status_code)

    return results



