from xml.dom.minidom import parseString
import html_parser
import  urllib2


def run_query(term):

    results = []

    root_url = "https://wsearch.nlm.nih.gov/ws/query?db=healthTopics"
    quotesSign = "%22"
    term = quotesSign + term.replace(" ", "+") + quotesSign

    search_url = "{}&term={}&retmax=50".format(
        root_url,
        term
    )

    response = urllib2.urlopen(search_url).read()
    DOMTree = parseString(response)
    collection = DOMTree.documentElement
    documents = collection.getElementsByTagName("document")
    for document in documents:
        children = document.getElementsByTagName("content")

        title = ""
        summary = ""
        for child in children:
            if child.getAttribute("name") == "title":
                title = html_parser.strip_tags(child.childNodes[0].data)
            elif child.getAttribute("name") == "snippet":
                summary = html_parser.strip_tags(child.childNodes[0].data)
                break
        results.append({'url':document.getAttribute("url"),
                        "title":title,
                        "summary":summary,
                        "source": "medline"})

    return results

def main():
    # Query, get the results and create a variable to store rank.
    query = raw_input("Please enter a query: ")
    results = run_query(query)
    for result in results:
        print result

if __name__ == '__main__':
    main()

