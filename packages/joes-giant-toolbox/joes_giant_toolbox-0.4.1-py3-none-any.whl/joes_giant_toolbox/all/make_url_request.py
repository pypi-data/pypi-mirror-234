import urllib.request


def make_url_request(
    url: str,
    headers: dict = None,
    timeout: int = 10,
    decode_format: str = None,
    max_bytes: int = None,
) -> dict:
    """A convenience function for making API requests using the urllib library

    A lot of this code is stolen from the (amazing) article https://realpython.com/urllib-request/

    Parameters
    ----------
    url: str
        The URL to send the request to
    headers: dict, optional
        Headers to include in the request
    timeout: int = 10
        Timeout (in seconds) for blocking operations like the connection attempt
        This parameter is passed directly to the urllib.request.urlopen() function
        From urllib documentation: if not specified, the global default timeout setting will be used. This actually only works for HTTP, HTTPS and FTP connections.
    decode_format: str = None, optional
        Format to encode the returned result string to
        This parameter is passed directly to the core python decode() string method
        By default, the returned content is binary
    max_bytes: int = None, optional
        Limits the returned result to the first [max_bytes] bytes
        (can be used to deal with large websites)

    Returns
    -------
    dict
        {
          'returned_content': str       <content returned by URL>,
          'response_status_code': int   <response code returned by URL>,
          'status_desc': str            <string description of URL response>
        }

    Examples
    --------
    ## Normal Request ##
    >> make_url_request(url="https://example.com", decode_format="utf-8")
    { 'returned_content': '<!doctype html>\n<html>\n<head>\n ...',
      'response_status_code': 200,
      'status_desc': 'success'
    }

    ## Only load the first part of a large website ##
    >> make_url_request(url="https://hastie.su.domains/Papers/ESLII.pdf", max_bytes=10)
    { 'returned_content': b'%PDF-1.6\r%',
      'response_status_code': 200,
      'status_desc': 'success'
    }

    ## Forbidden ##
    >> make_url_request(url="https://realpython.com/urllib-request/", decode_format="utf-8")
    { 'returned_content': None,
      'response_status_code': 403,
      'status_desc': 'Forbidden'
    }

    ## URL that does not exist ##
    >> make_url_request(url="https://www.g6h9f4b2n0d.co.uk")
    { 'returned_content': None,
      'response_status_code': None,
      'status_desc': socket.gaierror(8,'nodename nor servname provided, or not known')
    }

    ## specify headers so that website will let us in ##
    >> make_url_request(url="https://www.amazon.com")
    { 'returned_content': None, 'response_status_code': 503, 'status_desc': 'Service Unavailable'}
    >> make_request(url="https://www.amazon.com", headers={"User-Agent":"let me in please"})
    { 'returned_content': b'<!doctype html><html lang=...', 'response_status_code': 200, 'status_desc': 'success'}

    ## website that takes too long to respond ##
    >> make_url_request(url="https://www.google.com", timeout=0.01)
    { 'returned_content': None,
      'response_status_code': None,
      'status_desc': TimeoutError('timed out')
    }
    """
    request = urllib.request.Request(url, headers=headers or {})
    try:
        if max_bytes is None:
            with urllib.request.urlopen(request, timeout=timeout) as url_response:
                returned_content = url_response.read()
        else:
            with urllib.request.urlopen(request, timeout=timeout) as url_response:
                returned_content = url_response.read(max_bytes)
        if decode_format is not None:
            returned_content = returned_content.decode("utf-8")
        response_status_code = url_response.status
        status_desc = "success"
    except urllib.error.HTTPError as error:
        returned_content = None
        response_status_code = error.status
        status_desc = error.reason
    except urllib.error.URLError as error:
        returned_content = None
        response_status_code = None
        status_desc = error.reason
    except TimeoutError:
        returned_content = None
        response_status_code = None
        status_desc = "request timed out"

    return {
        "returned_content": returned_content,
        "response_status_code": response_status_code,
        "status_desc": status_desc,
    }
