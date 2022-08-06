"""The solution to the challenge.
run this file to use the program.
Read more at the readme file"""


from re import findall
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib.parse import urlparse
from pathlib import PurePosixPath
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count
import sys


default_num_workers = min(32, cpu_count() + 5)


def connected_to_internet(known_active_url = 'https://google.com'):
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
    """Returns true if url is a file and false otherwise."""
    if url.endswith(".html"):
        return False
    extensions = PurePosixPath(url).suffixes
    return len(extensions) > 0


def url_is_wiki_page(url):
    """Returns true if url is a url to an existing wikipedia page and false otherwise."""
    if not isinstance(url, str):
        return False
    parsed_url = urlparse(url)
    uses_http = parsed_url.scheme in ("http", "https")
    in_wikipedia_org = "wikipedia.org/wiki/" in url
    is_file = url_is_file(url)
    is_query = "?" in url 
    return uses_http and in_wikipedia_org and (not is_file) and (not is_query)


def create_has_link_func(url_to):
    """Given a target url, returns a function that checks
    if a url has a link back to the target url.
    If that is the case, return the second url, otherwise return None."""

    def has_link_to_input_url(url_from):
        if url_from == url_to:
            return False
        try:
            from_page_html_str = urlopen(url_from).read().decode("utf-8")
        except HTTPError:
            return False
        internal_link = url_to[url_to.find("/wiki/"):]
        return internal_link in from_page_html_str

    has_link_to_input_url.__name__ = f"has_link_to_{url_to}"
    return has_link_to_input_url


def link_iter_to_url_gen(urls, sub_domain):
    """Modifies the internal links to valid urls and removes non valid urls
    examples: https://en.wikipedia.org/wiki/Israel -> https://en.wikipedia.org/wiki/Israel
    /wiki/Israel -> https://{sub_domain}.wikipedia.org/wiki/Israel"""
    already_generated = set([])
    for url in urls:
        if not url in already_generated:
            already_generated.add(url)
            if url.startswith("/wiki/"):
                url = f"https://{sub_domain}.wikipedia.org" + url
            if url_is_wiki_page(url):
                yield url


def wiki_link_back_gen(input_url, num_workers = default_num_workers):
    """A generator function that gets a url to a wikipedia page
     and returns all urls to other wikipedia pages that have a link back to the original page.
    num_workers is the number of processes to use in the thread pool.
    """
    html_page = urlopen(input_url).read().decode("utf-8")
    links = findall("href=[\"\'](.*?)[\"\']", html_page)
    index_start_sub_domain = input_url.index("//") + 2
    index_stop_sub_domain = input_url.index(".")
    sub_domain = input_url[index_start_sub_domain : index_stop_sub_domain]
    url_gen = link_iter_to_url_gen(links, sub_domain)
    has_link_to_input = create_has_link_func(input_url)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_url = {executor.submit(has_link_to_input, url): url for url in url_gen}
        for future in as_completed(future_to_url):
            curr_url = future_to_url[future]
            is_linked = future.result()
            if is_linked:
                yield curr_url


def get_input_url(command_line_arguments, first_call = True):
    """Returns the input url from the command line from the user."""
    if first_call and len(command_line_arguments) > 1:
        entered_url = command_line_arguments[1]
    else:
        entered_url = input("Enter your URL: \n")

    error_message = ""

    if not url_is_wiki_page(entered_url):
        error_message += """
        The url must also be a working url to an active wikipedia page.
        The url must start with either http:// or https://,
        include with .wikipedia.org/wiki/
        and not be have a file extension (except html).
        """

    if not url_is_active(entered_url):
        error_message += f"The page in {entered_url} is not active or does not exist.\n"

    if error_message == "":
        return entered_url

    print(error_message)
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
        print("Please connect to the internet and try again.")
        return
    print("You are connected to the internet.")

    command_line_arguments = sys.argv
    input_url = get_input_url(command_line_arguments, True)
    max_num_workers = get_max_num_workers(command_line_arguments)

    wikipedia_urls = wiki_link_back_gen(input_url, max_num_workers)
    print(f"Those are the pages that satisfy the rules at README.md for the input {input_url}: \n")
    for output_url in wikipedia_urls:
        print(output_url)


if __name__ == "__main__":
    main()
