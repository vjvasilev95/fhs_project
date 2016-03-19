
def merge(results_from_bing, results_from_healthgov, results_from_medline):
    i_bing = 0
    i_healthgov = 0
    i_medline = 0
    l_bing = len(results_from_bing)
    l_healthgov = len(results_from_healthgov)
    l_medline = len(results_from_medline)
    merged = []

    while (i_bing < l_bing and i_healthgov < l_healthgov and i_medline < l_medline):
        merged.append(results_from_bing[i_bing])
        merged.append(results_from_healthgov[i_healthgov])
        merged.append(results_from_medline[i_medline])
        i_bing += 1
        i_healthgov += 1
        i_medline += 1

    while ( i_bing < l_bing ):
        merged.append(results_from_bing[i_bing])
        i_bing += 1

    while (i_medline < l_medline ):
        merged.append(results_from_medline[i_medline])
        i_medline += 1

    while (i_healthgov < l_healthgov ):
        merged.append(results_from_healthgov[i_healthgov])
        i_healthgov += 1

    return merged








