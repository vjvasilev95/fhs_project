import json
import urllib, urllib2
import keys
from save_page_helper import calculate_stats

# Add your BING_API_KEY

BING_API_KEY = keys.BING_API_KEY

def run_query(search_terms):
    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'

    # Specify how many results we wish to be returned per page.
    # Offset specifies where in the results list to start from.
    # With results_per_page = 10 and offset = 11, this would start from page 2.
    results_per_page = 10
    offset = 0

    # Wrap quotes around our query terms as required by the Bing API.
    # The query we will then use is stored within variable query.
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    # Construct the latter part of our request's URL.
    # Sets the format of the response to JSON and sets other properties.
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query)

    # Setup authentication with the Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''


    # Create a 'password manager' which handles authentication for us.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    # Create our results list which we'll populate.
    results = []

    try:
        # Prepare for connecting to Bing's servers.
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        # Connect to the server and read the response generated.
        response = urllib2.urlopen(search_url).read()

        # Convert the string response to a Python dictionary object.
        json_response = json.loads(response)
        # Loop through each page returned, populating out results list.

        for result in json_response['d']['results']:

            stats = calculate_stats(result['Description'])
            results.append({
            'title': result['Title'],
            'url': result['Url'],
            'summary': result['Description'],
            'source': "bing",
            'polarity':stats['polarity'],
            'subjectivity':stats['subjectivity'],
            'flesh_score':stats['flesh_score']})

    # Catch a URLError exception - something went wrong when connecting!
    except urllib2.URLError as e:
        print "Error when querying the Bing API: ", e

    return results


def main():
    # Query, get the results and create a variable to store rank.
    query = raw_input("Please enter a query: ")
    results = run_query(query)
    rank = 1

    # Loop through our results.
    for result in results:
        # Print details.
        print "Rank {0}".format(rank)
        print result['title']
        print result['link']
        print result['summary']
        print

        # Increment our rank counter by 1.
        rank += 1

if __name__ == '__main__':
    main()
