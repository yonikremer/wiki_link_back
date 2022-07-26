"""The solution to the challenge.
run this file to use the program.
Read more at the readme file"""

from re import findall
from socket import timeout as socket_timeout_error
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib.parse import urlparse
from pathlib import PurePosixPath
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count as number_of_cores
import sys

default_num_workers = min(32, number_of_cores() + 4)


def connected_to_internet(known_active_url='https://google.com'):
    """Returns true if you are connected to internet and false otherwise."""
    try:
        urlopen(known_active_url)
    except URLError:
        return False
    return True


def url_is_active(url):
    """Returns true if you can get the content of the url and false otherwise."""
    try:
        return urlopen(url).getcode() == 200
    except (HTTPError, URLError, ValueError):
        return False


def url_is_file(url):
    """Returns true if url is a file (except for HTML) and false otherwise."""
    if url.endswith(".html"):
        return False
    extensions = PurePosixPath(url).suffixes
    return len(extensions) > 0


def url_is_web_page(url):
    """Returns true if url is an url to an existing web page and false otherwise."""
    if not isinstance(url, str):
        return False
    uses_http = url.startswith("http")
    is_file = url_is_file(url)
    return uses_http and (not is_file)


def create_have_link_func(url_to, decoding_method="utf-8", timeout=600):
    """Given a target url, returns a function that checks
    if an url has a link back to the target url.
    If that is the case, return True, otherwise return False."""
    relative_url_from = urlparse(url_to).path

    def have_link_to_input_url(url_from):
        are_the_same_page = (url_from in url_to) or (url_to in url_from)
        if are_the_same_page:
            return False
        try:
            from_page_html_str = urlopen(url_from, timeout=timeout).read().decode(decoding_method)
        except (HTTPError, URLError, ValueError):
            return False
        except (TimeoutError, socket_timeout_error) as original_exception:
            print(f"{url_from} caused a timeout error.")
            raise ValueError(f"Timeout of {timeout} seconds is not enough.") from original_exception
        return relative_url_from in from_page_html_str

    return have_link_to_input_url


def relative_to_absolute_urls(relative_urls, base_scheme, base_network_location):
    """Modifies relative to absolute urls and removes non-valid URLs
    examples: https://en.wikipedia.org/wiki/Israel, any -> https://en.wikipedia.org/wiki/Israel
    /wiki/Israel, en -> https://en.wikipedia.org/wiki/Israel"""
    absolute_urls = set([])
    for url in set(relative_urls):
        curr_url_parsed = urlparse(url)
        curr_network_location = curr_url_parsed.netloc
        curr_scheme = curr_url_parsed.scheme
        if curr_network_location == "":
            url = base_network_location + url
        if curr_scheme == "":
            url = f"{base_scheme}://{url}"
        if url_is_web_page(url):
            absolute_urls.add(url)
    return absolute_urls


def link_back_gen(input_url, num_workers=default_num_workers, decoding_method="utf-8"):
    """generates all the urls that satisfy the rules of the challenge as described in the README.md file
    """
    input_page_html = urlopen(input_url).read().decode(decoding_method)
    relative_urls = findall(pattern="href=[\"\'](.*?)[\"\']", string=input_page_html)
    parsed_input_url = urlparse(input_url)
    input_url_scheme = parsed_input_url.scheme
    input_url_network_location = parsed_input_url.netloc
    absolute_urls = relative_to_absolute_urls(relative_urls, input_url_scheme, input_url_network_location)
    have_link_to_input = create_have_link_func(input_url)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_url = {executor.submit(have_link_to_input, url): url for url in absolute_urls}
        for future in as_completed(future_to_url):
            curr_url = future_to_url[future]
            is_linked = future.result()
            if is_linked:
                yield curr_url


def get_input_url(command_line_arguments, first_call=True):
    """Returns the input url from the command line from the user."""
    if first_call and len(command_line_arguments) > 1:
        entered_url = command_line_arguments[1]
    else:
        entered_url = input("Enter your URL: \n")

    errors = []

    if not url_is_web_page(entered_url):
        errors += """
        The url must also be a working url to an active web page.
        The url must start with either http:// or https://,
        and not be have a file extension (except html).
        """

    if not url_is_active(entered_url):
        errors += f"The page in {entered_url} is not active or does not exist.\n"

    if not errors:
        return entered_url

    print("\n".join(errors))
    return get_input_url(command_line_arguments, False)


def get_max_num_workers(command_line_arguments):
    """Returns the max number of workers to use in the thread pool from the user."""
    if len(command_line_arguments) > 2:
        num_workers_str = command_line_arguments[2]
    else:
        input_message = f"""Enter the number of workers.
        The number of workers must be a literal positive int.
        The default value for your computer is: {default_num_workers} \n"""
        num_workers_str = input(input_message)

    while not num_workers_str.isnumeric():
        print(f"{num_workers_str} is not a literal int, please enter a literal int")
        num_workers_str = input("Please enter a literal int: \n")

    num_workers = int(num_workers_str)
    while num_workers < 1:
        print(f"{num_workers} is not positive")
        num_workers_str = input("Please enter a positive integer: \n")
        while not num_workers_str.isnumeric():
            print(f"{num_workers_str} is not a literal int, please enter a literal int")
            num_workers_str = input("Please enter a literal int: \n")
        num_workers = int(num_workers_str)
    return num_workers


def main():
    """The function called when running the file solution.py
       read more in the README.md file"""

    if not connected_to_internet():
        print("You are not connected to the internet, Internet is required to run this program.")
        print("Please connect to the internet and try to run the program again.")
        return

    command_line_arguments = sys.argv
    input_url = get_input_url(command_line_arguments, True)
    max_num_workers = get_max_num_workers(command_line_arguments)
    answer_generator = link_back_gen(input_url, max_num_workers)
    print(f"Those are the pages that satisfy the rules at README.md for the input {input_url}: \n")
    for output_url in answer_generator:
        print(output_url)


if __name__ == "__main__":
    main()
