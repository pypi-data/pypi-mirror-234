import random
import time
from typing import List, Tuple
import bs4

from joes_giant_toolbox.all.make_url_request import make_url_request
from joes_giant_toolbox.all.string_cleaner import StringCleaner


def scrape_webpage_and_all_linked_webpages(
    url: str,
    max_additional_urls: int,
    scrape_pause_seconds: Tuple[float, float],
    url_pref_regex: List[str] = None,
    verbose: bool = True,
    **kwargs,
) -> dict:
    """Extracts HTML from given web page, and also follows all of the hyperlinks on that page and scrapes those too

    Parameters
    ----------
    url: str
        The base URL - to scrape, and also to extract hyperlinks from
    max_additional_urls: int
        The maximum number of additional pages to attempt to scrape
        (i.e. number of hyperlinks to follow)
    scrape_pause_seconds: Tuple[float, float]
        (min_secs, max_secs)
        Between sending requests, the process will pause for a random number of seconds between [min_secs] and [max_secs]
    url_pref_regex: List[str], optional (default=None)
        <This is not yet implemented>
        A list of regex strings
        The position of the first regex string matched in this list by a particular URL defines the priority rank of the hyperlink
        Higher priority hyperlinks are scraped first
        If set to None (default), then hyperlinks are scraped in a random order
    verbose: bool, optional (default=True)
        If set to True, the function will print logging information while it is running
    **kwargs
        Additional named parameters to pass to the make_url_request() function
    Returns
    -------
    dict
        A dictionary containing the HTML from each scraped page, as well as the status of the request
        Example:
        {
            '<url-1>': {
                'returned_content': '<!DOCTYPE html><html la...',
                'response_status_code': 200,
                'status_desc': 'success'
            },
            '<url-2>': {
                'returned_content': None,
                'response_status_code': 403,
                'status_desc': 'Forbidden'
            },
            ...etc
        }

    Example Usage
    -------------
    >>>scrape_webpage_and_all_linked_webpages(
    ...     url="https://www.imdb.com",
    ...     max_additional_urls=5,
    ...     scrape_pause_seconds=(1.0, 5.0),
    ...     # parameters passed to make_url_request() function #
    ...     headers={"User-Agent": "open sesame"},
    ...     timeout=10,
    ...     decode_format="utf-8",
    ...     max_bytes=2_000_000,
    ...)
    started request: https://www.imdb.com ...
    ..completed request (status code: 200)
    extracting hyperlinks.....110 hyperlinks found
    pausing for 4.25 seconds.....done
    started request: https://www.imdb.com/superheroes/streaming-stars/rg3853097728/mediaviewer/rm389100801?ref_=hm_edcft_ft_g_streamtan_3_t ...
    ..completed request (status code: 200)
    pausing for 4.30 seconds.....done
    started request: https://www.imdb.com/privacy/adpreferences/ ...
    ..completed request (status code: 200)
    pausing for 2.72 seconds.....done
    started request: https://www.imdb.com/calendar/?ref_=nv_mv_cal ...
    ..completed request (status code: 200)
    pausing for 3.44 seconds.....done
    started request: https://www.imdb.com/video/vi2436219929/?listId=ls025720609&ref_=hm_edcio_og_ots_ted_5_t ...
    ..completed request (status code: 200)
    pausing for 2.28 seconds.....done
    started request: https://help.imdb.com/article/imdb/general-information/imdb-site-index/GNCX7BHNSPBTFALQ#so ...
    ..completed request (status code: 200)
    """
    string_cleaner_inst = StringCleaner(verbose=False)
    base_url = string_cleaner_inst.operations["extract_domain_from_url"](url)

    # request initial HTML #
    if verbose:
        print(f"started request: {url} ...")
    url_response = make_url_request.make_url_request(url=url, **kwargs)
    if verbose:
        print(
            f"..completed request (status code: {url_response['response_status_code']})"
        )
    all_results_dict = {url: url_response}

    # fetch hyperlinks in initial HTML #
    if verbose:
        print("extracting hyperlinks...", end="")
    soup_obj = bs4.BeautifulSoup(url_response["returned_content"], "html.parser")
    hyperlinks_found_list = [x["href"] for x in soup_obj.findAll("a", href=True)]
    clean_hyperlinks_list = []
    for hyperlink in hyperlinks_found_list:
        if hyperlink[:4] != "http":
            if hyperlink[0] == "/":
                clean_hyperlinks_list.append(f"{base_url}{hyperlink}")
            else:
                clean_hyperlinks_list.append(f"{base_url}/{hyperlink}")
        else:
            clean_hyperlinks_list.append(hyperlink)
    clean_hyperlinks_list = list(set(clean_hyperlinks_list))  # remove duplicates
    if verbose:
        print(f"..{len(clean_hyperlinks_list)} hyperlinks found")
    random.shuffle(clean_hyperlinks_list)

    # scrape hyperlink pages #
    for hyperlink_url in clean_hyperlinks_list[:max_additional_urls]:
        pause_secs = random.uniform(scrape_pause_seconds[0], scrape_pause_seconds[1])
        if verbose:
            print(f"pausing for {pause_secs:.2f} seconds...", end="")
        time.sleep(pause_secs)
        if verbose:
            print("..done")
        if verbose:
            print(f"started request: {hyperlink_url} ...")
        hyperlink_url_response = make_url_request.make_url_request(
            url=hyperlink_url, **kwargs
        )
        if verbose:
            print(
                f"..completed request (status code: {hyperlink_url_response['response_status_code']})"
            )
        all_results_dict[hyperlink_url] = hyperlink_url_response

    return all_results_dict
