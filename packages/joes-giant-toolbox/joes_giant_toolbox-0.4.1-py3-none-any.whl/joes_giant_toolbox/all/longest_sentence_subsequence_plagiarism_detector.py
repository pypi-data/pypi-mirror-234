from typing import List

from joes_giant_toolbox.all.print_progress_bar import print_progress_bar


def longest_sentence_subsequence_plagiarism_detector(
    doc1_str: str,
    doc2_str: str,
    min_seq_len: int,
) -> List[str]:
    """
    Finds phrases (sequences of consecutive words) common to two documents (e.g. to act as a naive plagiarism detector)

    I had to produce this function in a short space of time so it is:
        *   slow
        *   memory inefficient
        *   working reliably, even for fairly large documents (e.g. 200 pages)

    Notes
    -----
    The word matching is case-sensitive and exact, so the input text should be preprocessed prior to being used in this function (e.g. all text to lower case, and possibly remove certain punctuation)

    Parameters
    ----------
    doc1_str: str
        The text of the first document
    doc2_str: str
        The text of the second document
    min_seq_len:
        Will only return sequences containing at least this many words

    Returns
    -------
    List[str]
        A list containing the phrases (sequences of consecutive words) common to both documents
        Sorted from longest (most words) to shortest (least words)

    Example Usage
    -------------
    >>> longest_sentence_subsequence_plagiarism_detector(
    ...     doc1_str="keith allen haring may 4 1958 february 16 1990 was an american artist whose pop art emerged from the new york city graffiti subculture of the 1980s1 his animated imagery has become a widely recognized visual language much of his work includes sexual allusions that turned into social activism by using the images to advocate for safe sex and aids awareness3 in addition to solo gallery exhibitions he participated in renowned national and international group shows such as documenta in kassel the whitney biennial in new york the são paulo biennial and the venice biennale the whitney museum held a retrospective of his art in 1997",
    ...     doc2_str="widely recognized american artist whose art emerged from new york city graffiti subculture",
    ...     min_seq_len=2,
    ... )
    ['new york city graffiti subculture',
     'american artist whose',
     'art emerged from',
     'widely recognized']
    """
    seq_found: list = []
    doc1_words: list = doc1_str.split()
    doc2_words: list = doc2_str.split()
    common_seq_progress_printer = print_progress_bar(
        base_message="collecting common sequences"
    )
    remove_subseq_progress_printer = print_progress_bar(
        base_message="removing subsequences in result set"
    )

    current_seq = []
    for doc2_word_idx in range(len(doc2_words)):
        common_seq_progress_printer.print_progress(
            percent_complete=(doc2_word_idx + 1) / len(doc2_words)
        )
        for doc1_word_idx in range(len(doc1_words)):
            if doc2_words[doc2_word_idx] == doc1_words[doc1_word_idx]:
                current_seq.append(doc2_words[doc2_word_idx])
                temp_add = 1
                while 1 == 1:
                    if (
                        doc2_word_idx + temp_add < len(doc2_words)
                        and doc1_word_idx + temp_add < len(doc1_words)
                        and doc2_words[doc2_word_idx + temp_add]
                        == doc1_words[doc1_word_idx + temp_add]
                    ):
                        current_seq.append(doc2_words[doc2_word_idx + temp_add])
                        temp_add += 1
                    else:
                        if len(current_seq) >= min_seq_len:
                            seq_found.append(current_seq)
                        current_seq = []
                        break

    final_seq_found: list = []
    joined_seq_found: list = ["|".join(x) for x in seq_found]
    for idx, seq in enumerate(seq_found):
        remove_subseq_progress_printer.print_progress(
            percent_complete=(idx + 1) / len(seq_found)
        )
        join_seq = "|".join(seq)
        if sum([join_seq in x for x in joined_seq_found]) == 1:
            final_seq_found.append(seq)

    return [" ".join(x) for x in sorted(final_seq_found, key=len, reverse=True)]


# if __name__ == "__main__":
#     with open("/Users/josephbolton/Downloads/thesis_text", "r") as f:
#         thesis_text = f.read()

#     with open("/Users/josephbolton/Downloads/paper_text", "r") as f:
#         paper_text = f.read()

#     thesis_text = re.sub("[^\w ]", "", thesis_text).lower()
#     paper_text = re.sub("[^\w ]", "", paper_text).lower()

#     test = longest_sentence_subsequence_plagiarism_detector(
#         doc1_text=thesis_text,
#         doc2_text=paper_text,
#         n_seq=200,
#     )

#     for x in test:
#         print(x)
#         print()
