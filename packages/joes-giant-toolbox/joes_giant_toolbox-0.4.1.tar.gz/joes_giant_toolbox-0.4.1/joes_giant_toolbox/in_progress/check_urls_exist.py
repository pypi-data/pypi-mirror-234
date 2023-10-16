import concurrent.futures
import re
import httpx


def check_urls_exist(
    doc_text: str,
    url_regex_pattern: str = r"(https?://[\w\/\_\.\-]+)",
) -> dict[str, tuple[int, str]]:
    """DOCSTRING TODO

    with open("/Users/josephbolton/Documents/mom_phd/Dissertation draft 3.txt","r",encoding="unicode_escape") as file:
        doc_text = file.read()
    """
    result_dict = {}
    find_urls = re.findall(url_regex_pattern, doc_text)
    if find_urls:
        for idx, url in enumerate(find_urls):
            if url[-1] == ".":
                find_urls[idx] = find_urls[idx][:-1]

        def head_request_response(url) -> tuple[int, str]:
            """DOCSTRING TODO"""
            try:
                url_response = httpx.head(url, timeout=10)
                response_code = url_response.status_code
                response_explain_text = url_response.reason_phrase
            except httpx.HTTPError as exc:
                response_code = None
                response_explain_text = str(exc)
            print(f"completed {url}")
            return url, response_code, response_explain_text

        find_urls = tuple(set(find_urls))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(head_request_response, find_urls)

        for url, status_code, response_explain_text in results:
            result_dict[url] = (status_code, response_explain_text)

    return result_dict
