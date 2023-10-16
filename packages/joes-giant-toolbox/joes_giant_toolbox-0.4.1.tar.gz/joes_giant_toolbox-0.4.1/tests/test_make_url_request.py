# # add the root project directory to the system path:
# import sys
# import pathlib
# import json
# import time

# parent_dir_path = pathlib.Path(__file__).parent.parent
# sys.path.append(str(parent_dir_path))

# # import the function to be tested:
# from joes_giant_toolbox.make_url_request import make_url_request

# # run the tests:
# def test_successful_request_with_known_output():
#     """test if expected content can be successfully pulled from a known response URL"""
#     url_response = make_url_request(url="https://jsonplaceholder.typicode.com/todos/1")
#     output = json.loads(url_response["returned_content"])
#     expected_output = {
#         "userId": 1,
#         "id": 1,
#         "title": "delectus aut autem",
#         "completed": False,
#     }
#     assert (
#         output == expected_output
#     ), f"request to known URL produced unexpected result \nReturned: {output}. \nExpected: {expected_output}"


# def test_url_does_not_exist():
#     """request to a non-existent URL must return no content and no status code"""
#     url_response = make_url_request(url="https://non.existent.website.name/")
#     assert (
#         url_response["returned_content"] is None
#     ), "non-existent website must return no content"
#     assert (
#         url_response["response_status_code"] is None
#     ), "non-existent website must return no status code"


# def test_request_timeout():
#     """timeout parameter must quickly force the request to stop"""
#     start_time = time.perf_counter()
#     url_response = make_url_request(
#         url="https://hastie.su.domains/Papers/ESLII.pdf", timeout=0.1
#     )
#     end_time = time.perf_counter()
#     assert (
#         end_time - start_time
#     ) < 1.0, "timeout parameter must quickly force the request to stop"


# def test_efficient_stream_content_from_large_request():
#     """max_bytes parameter must allow quick download of a small amount of information from a large request
#     ..and must stream exactly the right amount
#     """
#     start_time = time.perf_counter()
#     url_response = make_url_request(
#         url="https://hastie.su.domains/Papers/ESLII.pdf", max_bytes=100
#     )
#     end_time = time.perf_counter()
#     assert (
#         url_response["response_status_code"] == 200
#     ), "straightforward request must not be rejected by server"
#     assert (
#         end_time - start_time
#     ) < 5, "small number of requested bytes from large request must complete quickly"
#     assert (
#         len(url_response["returned_content"]) == 100
#     ), "exactly [max_bytes] must be returned"
