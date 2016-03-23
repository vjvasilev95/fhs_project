CHANGES MADE:

1) In the three files where we use the search APIs: I extract the contents from healthgov and medline plus results, and the description from bing results. I add their scores as key/value pairs in the dictionaries inside the results list
2) I therefore display the scores into search_forms.html.
3) In search_ajax.js I extract them as well, and pass them to the Ajax request
4) Check the very minor changes in the save_page() view. 
