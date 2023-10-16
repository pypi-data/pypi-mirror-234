import joes_giant_toolbox.text

string_cleaner = joes_giant_toolbox.text.StringCleaner()

# # run the tests:
# def test_remove_words_or_phrases():
#     """Confirms that the remove_words_or_phrases() function works as expected, both in isolation and within a chained sequence of cleaning operations"""
#     string_cleaner = StringCleaner()

#     # test 1 #
#     func_output = string_cleaner.operations["remove_words_or_phrases"](
#         raw_str="remove me text delete meremove me that delete me we want remove me",
#         remove_list=["remove me", "delete me"],
#         enforce_word_boundaries=False,
#     )
#     assert (
#         func_output == " text  that  we want "
#     ), f"""
# --test case failed--
# Input:               raw_str="remove me text delete meremove me that delete me we want remove me",
#                     remove_list=["remove me", "delete me"],
#                     enforce_word_boundaries=False,
# Expected Output:    " text  that  we want "
# Observed Output:    "{func_output}"
# """

#     # test 2 #
#     func_output = string_cleaner.operations["remove_words_or_phrases"](
#         raw_str="remove me text delete meremove me that delete me we want remove me",
#         remove_list=["remove me", "delete me"],
#         enforce_word_boundaries=True,
#     )
#     assert (
#         func_output == " text delete meremove me that  we want "
#     ), f"""
# --test case failed--
# Input:              raw_str="remove me text delete meremove me that delete me we want remove me",
#                     remove_list=["remove me", "delete me"],
#                     enforce_word_boundaries=True,
# Expected Output:    " text delete meremove me that  we want "
# Observed Output:    "{func_output}"
# """

#     # test 3 #
#     func_output = string_cleaner.apply_sequential_operations(
#         raw_str="company name is Stinc Inc S.L.T.D. Ltd",
#         operation_names_list=[
#             "to_lowercase",
#             "remove_punctuation",
#             "remove_words_or_phrases",
#             "multiple_spaces_to_single_spaces",
#         ],
#         operation_params_dict={
#             "remove_words_or_phrases": {
#                 "remove_list": ["inc", "ltd"],
#                 "enforce_word_boundaries": False,
#             }
#         },
#     )
#     assert (
#         func_output == "company name is st s "
#     ), f"""
# --test case failed--
# Input:  string_cleaner.apply_sequential_operations(
#             raw_str="company name is Stinc Inc S.L.T.D. Ltd",
#             operation_names_list=[
#                 "to_lowercase",
#                 "remove_punctuation",
#                 "remove_words_or_phrases",
#                 "multiple_spaces_to_single_spaces",
#             ],
#             operation_params_dict={{
#                 "remove_words_or_phrases": {{
#                     "remove_list": ["inc", "ltd"],
#                     "enforce_word_boundaries": False,
#                 }}
#             }},
#         )
# Expected Output:    "company name is st s "
# Observed Output:    "{func_output}"
# """

#     # test 4 #
#     func_output = string_cleaner.apply_sequential_operations(
#         raw_str="company name is Stinc Inc S.L.T.D. Ltd",
#         operation_names_list=[
#             "to_lowercase",
#             "remove_punctuation",
#             "remove_words_or_phrases",
#             "multiple_spaces_to_single_spaces",
#         ],
#         operation_params_dict={
#             "remove_words_or_phrases": {
#                 "remove_list": ["inc", "ltd"],
#                 "enforce_word_boundaries": True,
#             }
#         },
#     )
#     assert (
#         func_output == "company name is stinc sltd "
#     ), f"""
# --test case failed--
# Input:  string_cleaner.apply_sequential_operations(
#             raw_str="company name is Stinc Inc S.L.T.D. Ltd",
#             operation_names_list=[
#                 "to_lowercase",
#                 "remove_punctuation",
#                 "remove_words_or_phrases",
#                 "multiple_spaces_to_single_spaces",
#             ],
#             operation_params_dict={{
#                 "remove_words_or_phrases": {{
#                     "remove_list": ["inc", "ltd"],
#                     "enforce_word_boundaries": True,
#                 }}
#             }},
#         )
# Expected Output:    "company name is stinc sltd "
# Observed Output:    "{func_output}"
# """


# # def test_apply_sequential_operations():
# #    pass
