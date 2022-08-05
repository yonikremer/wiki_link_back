"""The solution to the challenge.
run this file to use the program.
Read more at the readme file"""


from typing import Generator, Callable, Optional, List, Iterable, Set
from re import findall
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count
import sys


default_num_workers = min(32, cpu_count() + 5)
StringGenerator: type = Generator[str, None, None]


def connected_to_internet(known_active_url = 'https://google.com'):
    """Returns true if you are connected to internet and false otherwise."""
    try:
        urlopen(known_active_url)
    except URLError:
        return False
    return True


def url_is_active(url: str) -> bool:
    """Returns true if you can get the content of the url and false otherwise."""
    try:
        return urlopen(url).getcode() == 200
    except (HTTPError, URLError):
        return False


def url_is_wiki_page(url: str) -> bool:
    """Returns true if url is a url to an existing wikipedia page and false otherwise."""
    if not isinstance(url, str):
        return False
    uses_http = url.startswith("https://") or url.startswith("http://")
    in_wikipedia_org = ".wikipedia.org/wiki/" in url
    return uses_http and in_wikipedia_org


def create_has_link_func(url_to: str) -> Callable[[str], bool]:
    """Given a target url, returns a function that checks
    if a url has a link back to the target url.
    If that is the case, return the second url, otherwise return None."""

    def has_link_to_input_url(url_from: str) -> bool:
        if "File:" in url_from or url_from == url_to:
            return False
        from_page_html_str: str = urlopen(url_from).read().decode("utf-8")
        internal_link: str = url_to[url_to.find("/wiki/"):]
        return internal_link in from_page_html_str

    has_link_to_input_url.__name__ = f"has_link_to_{url_to}"
    return has_link_to_input_url


def link_iter_to_url_gen(urls: Iterable[str], sub_domain: str) -> StringGenerator:
    """Modifies the internal links to valid urls and removes non valid urls
    examples: https://en.wikipedia.org/wiki/Israel -> https://en.wikipedia.org/wiki/Israel
    /wiki/Israel -> https://{sub_domain}.wikipedia.org/wiki/Israel"""
    already_generated: Set[str] = set([])
    for url in urls:
        if not url in already_generated:
            already_generated.add(url)
            if url.startswith("/wiki/"):
                url = f"https://{sub_domain}.wikipedia.org" + url
            if url_is_wiki_page(url):
                yield url


def wiki_link_back_gen(input_url: str, num_workers: int = default_num_workers) -> StringGenerator:
    """A generator function that gets a url to a wikipedia page
     and returns all urls to other wikipedia pages that have a link back to the original page.
    num_workers is the number of processes to use in the thread pool.
    """
    html_page: str = urlopen(input_url).read().decode("utf-8")
    link_list: List[str] = findall("href=[\"\'](.*?)[\"\']", html_page)
    index_start_sub_domain = input_url.index("//") + 2
    index_stop_sub_domain = input_url.index(".")
    sub_domain: str = input_url[index_start_sub_domain:index_stop_sub_domain]
    url_gen: StringGenerator = link_iter_to_url_gen(link_list, sub_domain)
    has_link_to_input: Callable[[str], bool] = create_has_link_func(input_url)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_url = {executor.submit(has_link_to_input, url): url for url in url_gen}
        for future in as_completed(future_to_url):
            curr_url = future_to_url[future]
            is_linked = future.result()
            if is_linked:
                yield curr_url


def get_input_url() -> str:
    """Returns the input url from the command line from the user."""
    command_line_arguments = sys.argv
    if len(command_line_arguments) > 1:
        entered_url = command_line_arguments[1]
    else:
        entered_url: str = input("Enter your URL: \n")

    if not url_is_wiki_page(entered_url):
        error_message = """
        The url must also be a working url to an active wikipedia page.
        The Requirements are:
        1. The url must start with either http:// or https://
        2. The url must include with .wikipedia.org/wiki/
        3. The url must be a valid url to an active wikipedia page.
        """
        return get_input_url()

    if not url_is_active(entered_url):
        error_message = f"The page in {entered_url} is not active or does not exist."

    if url_is_wiki_page(entered_url) and url_is_active(entered_url):
        return entered_url

    print(error_message)
    return get_input_url()


def get_max_num_workers() -> int:
    """Returns the max number of workers to use in the thread pool from the user."""
    command_line_arguments: List[str] = sys.argv
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
       read more in the readme file"""
    if not connected_to_internet():
        print("You are not connected to the internet, Internet is required to run this program.")
        print("Please connect to the internet and try again.")
        return
    print("You are connected to the internet.")

    input_url = get_input_url()
    max_num_workers = get_max_num_workers()

    wikipedia_urls: StringGenerator = wiki_link_back_gen(input_url, max_num_workers)
    print(f"Those are the pages that satisfy the rules at README.md for the input {input_url}: \n")
    for output_url in wikipedia_urls:
        print(output_url)


if __name__ == "__main__":
    main()
