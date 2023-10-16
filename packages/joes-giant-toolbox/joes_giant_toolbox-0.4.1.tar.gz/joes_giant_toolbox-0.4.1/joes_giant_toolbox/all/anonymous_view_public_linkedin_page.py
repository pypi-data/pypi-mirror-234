import time
import random
from typing import Tuple, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def anonymous_view_public_linkedin_page(
    url_str: str,
    inter_sleep_n_secs: dict = {
        "after_initial_page_load": {"MIN": 4.5, "MAX": 5.5},
        "hover_over_button": {"MIN": 3.0, "MAX": 3.0},
        "after_button_click": {"MIN": 1.0, "MAX": 1.0},
    },
    click_popup_close_button: bool = True,
    verbose: bool = True,
    browser_options: List[str] | None = None,
    validation_search_strings: List[str] | None = None,
) -> Tuple[dict, str | None]:
    """Extracts the information (HTML) from a public LinkedIn web page (e.g. person or company) using a virtual browser

    (refer to "Example Usage" later in this documentation)

    Parameters
    ----------
    url_str: str
        The URL of the public LinkedIn page
    inter_sleep_n_secs: dict, optional (default: <see description below>)
        The process pauses for a random number of seconds (between "MIN" and "MAX") between subsequent actions in the virtual browser
        The default behaviour is:
        {
            "after_initial_page_load": {"MIN": 4.5, "MAX": 5.5},    # pause after page is first loaded
            "hover_over_button": {"MIN": 3.0, "MAX": 3.0},          # pause while hovering over popup close button
            "after_button_click": {"MIN": 1.0, "MAX": 1.0},         # pause after clicking popup close button
        }
    click_popup_close_button: bool, optional (default: True)
        Whether to close the popup window that opens by default when you view a company page and you are not logged in to LinkedIn
    verbose: bool, optional (default: True)
        If verbose=True, progress reporting is printed to the console
    browser_options: List[str] | None, optional (default: None)
        Flags to pass to selenium.webdriver.chrome.options.Options()
    validation_search_strings: List[str] | None, optional (default: None)
        If included, checks which of the strings in [validation_search_strings] are present within the extracted html (this is case sensitive)
        This can be used to identify whether the returned html is the actual desired page, or some kind of authorization wall returned by LinkedIn
        These results are written to the process logging dictionary returned by this function

    Returns
    -------
    Tuple[str, str | None]
        Returns a tuple of strings
        The first element of the tuple is a dictionary containing logging information collected during the running of the process
        The second element of the tuple is either a string containing the extracted page HTML (if function was successful) or else None (if the function was unsuccessful)

    Notes
    -----
    Selenium is used to locate the [X] close button on the initial pop-up window in order to make the full public page html visible
    Some pausing is required in order to wait for elements on the page to appear
    This sort of code relies closely on precise html structure, and so will definitely stop working at some point (as the LinkedIn website is modified)
    At the moment, this function uses ChromeDriver for the browser. You need to install this manually on your system in order for the function to work

    Example Usage
    -------------
    >>> from pprint import pprint
    >>> logging_dict, extracted_person_html = anonymous_view_public_linkedin_page(
    ...     url_str="https://www.linkedin.com/in/williamhgates/",
    ...     inter_sleep_n_secs = {
    ...         "after_initial_page_load": {"MIN": 4.5, "MAX": 5.5},
    ...         "hover_over_button": {"MIN": 3.0, "MAX": 3.0},
    ...         "after_button_click": {"MIN": 1.0, "MAX": 1.0},
    ...     },
    ...     click_popup_close_button=True,
    ...     verbose=True,
    ...     validation_search_strings=["authwall","og:description","could not be found","we can’t seem to find the page you’re looking for"],
    ... )
    >>> pprint(logging_dict, underscore_numbers=True)
    {   'close_button_found': True,
        'html_character_length': {  '1_initial': 20_557,
                                    '2_after_first_pause': 217_544,
                                    '3_after_button_click': 217_238,
                                    '4_final': 217_238
                                },
        'initial_popup_successfully_closed': True,
        'validation_search_strings': {  'authwall': False,
                                        'og:description': True,
                                        'could not be found': False,
                                        'we can’t seem to find the page you’re looking for': False,
                                    }
    }
    >>> print(extracted_person_html)
    <html lang="en"><head>
        <meta name="pageKey" content="public_profile_v3_desktop">
          <meta name="linkedin:pageTag" content="nonCanonical">
        <meta name="locale" content="en_US">
        ...
    >>> logging_dict, extracted_company_html = anonymous_view_public_linkedin_page(
    ...     url_str="https://www.linkedin.com/company/18000429",
    ...     verbose=True,
    ...     browser_options=["--headless","--disable-dev-shm-usage","--no-sandbox"],
    ... )
    >>> pprint(logging_dict, underscore_numbers=True)
    {   'close_button_found': False,
        'html_character_length': {  '1_initial': 45_410,
                                    '2_after_first_pause': 46_661,
                                    '3_after_button_click': 46_661,
                                    '4_final': 46_661
                                },
        'initial_popup_successfully_closed': False,
        'validation_search_strings': {'authwall': False, 'og:description': True}
    }
    >>> print(extracted_company_html)
    <html lang="en-US" class="artdeco " ...
    """
    logging_info_dict = {
        "close_button_found": None,
        "initial_popup_successfully_closed": None,
        "html_character_length": {
            "1_initial": None,
            "2_after_first_pause": None,
            "3_after_button_click": None,
            "4_final": None,
        },
        "validation_search_strings": {},
    }

    def if_verbose_print(*args, **kwargs) -> None:
        """if verbose=True, behaves identically to the print function (otherwise does nothing)"""
        if verbose:
            print(*args, **kwargs)

    if_verbose_print("opening browser..", end="")
    if browser_options is not None:
        browser_args = Options()
        for opt in browser_options:
            browser_args.add_argument(opt)
        auto_browser = webdriver.Chrome(options=browser_args)  # webdriver.Safari()
    else:
        auto_browser = webdriver.Chrome()  # webdriver.Safari()
    if_verbose_print("..done")

    if_verbose_print("loading page..", end="")
    auto_browser.get(url_str)
    if_verbose_print("..done")

    logging_info_dict["html_character_length"]["1_initial"] = len(
        auto_browser.page_source
    )

    random_n_secs = random.uniform(
        inter_sleep_n_secs["after_initial_page_load"]["MIN"],
        inter_sleep_n_secs["after_initial_page_load"]["MAX"],
    )
    if_verbose_print(f"waiting {random_n_secs:.4f} seconds..", end="")
    time.sleep(random_n_secs)
    if_verbose_print("..done")

    logging_info_dict["html_character_length"]["2_after_first_pause"] = len(
        auto_browser.page_source
    )

    if click_popup_close_button:
        random_n_secs = random.uniform(
            inter_sleep_n_secs["hover_over_button"]["MIN"],
            inter_sleep_n_secs["hover_over_button"]["MAX"],
        )
        if_verbose_print(
            f"clicking close [X] button (after hovering for {random_n_secs:.4f} seconds prior to click)..",
            end="",
        )
        try:
            actions = ActionChains(auto_browser)
            x_button = auto_browser.find_element(
                By.XPATH,
                "//icon[contains(@class,'contextual-sign-in-modal__modal-dismiss-icon lazy-loaded')]",
            )
            actions.move_to_element_with_offset(
                auto_browser.find_element(By.TAG_NAME, "body"), 0, 0
            )
            # actions.move_by_offset(100, 25).pause(5).click().perform()
            actions.move_to_element_with_offset(
                x_button, random.uniform(-5, 5), random.uniform(-5, 5)
            ).pause(random_n_secs).click().perform()
            logging_info_dict["close_button_found"] = True
            if_verbose_print("..done")
        except NoSuchElementException:
            if_verbose_print("\nNo close [X] button found, so no button was clicked")
            logging_info_dict["close_button_found"] = False

        if (
            len(auto_browser.page_source)
            == logging_info_dict["html_character_length"]["2_after_first_pause"]
        ):
            # if page content has not changed after attempted button click
            logging_info_dict["initial_popup_successfully_closed"] = False
            if_verbose_print("did not close initial popup window (or it did not exist)")
            logging_info_dict["html_character_length"]["3_after_button_click"] = len(
                auto_browser.page_source
            )
        else:
            # if page content has changed after attempted button click
            logging_info_dict["initial_popup_successfully_closed"] = True
            if_verbose_print("successfully closed initial popup window")
            logging_info_dict["html_character_length"]["3_after_button_click"] = len(
                auto_browser.page_source
            )

        random_n_secs = random.uniform(
            inter_sleep_n_secs["after_button_click"]["MIN"],
            inter_sleep_n_secs["after_button_click"]["MAX"],
        )
        if_verbose_print(
            f"pausing for {random_n_secs:.4f} seconds..",
            end="",
        )
        time.sleep(random_n_secs)
        if_verbose_print("..done")

    logging_info_dict["html_character_length"]["4_final"] = len(
        auto_browser.page_source
    )

    if_verbose_print("extracting html..", end="")
    page_html_str = auto_browser.page_source
    auto_browser.close()
    if_verbose_print("..done")

    if validation_search_strings is not None:
        for search_str in validation_search_strings:
            logging_info_dict["validation_search_strings"][search_str] = (
                search_str in page_html_str
            )

    return logging_info_dict, page_html_str
