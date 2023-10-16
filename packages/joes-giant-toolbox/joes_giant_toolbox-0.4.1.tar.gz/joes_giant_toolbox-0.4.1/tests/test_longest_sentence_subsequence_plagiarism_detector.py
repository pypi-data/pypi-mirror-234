import joes_giant_toolbox.text


# run the tests:
def test_known_output_example():
    result = joes_giant_toolbox.text.longest_sentence_subsequence_plagiarism_detector(
        doc1_str="cd efg opq rs ab cd efg az by opq rs tu vw xy af gq errty h ijk l mn a b c d e",
        doc2_str="ab cd efg h ijk l mn opq rs tu vw xy z",
        min_seq_len=3,
    )
    assert result == [
        "opq rs tu vw xy",
        "h ijk l mn",
        "ab cd efg",
    ], f"unexpected result on known example: expected=['opq rs tu vw xy','h ijk l mn','ab cd efg'] but received={result}"
