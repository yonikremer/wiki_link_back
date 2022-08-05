"""The solution to the challenge.
run this file to use the program.
Read more at the readme file"""


from typing import Generator, Callable, Optional, List, Iterable
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count
import sys


StringGenerator: type = Generator[str, None, None]


def connected_to_internet(known_active_url: str = 'https://google.com'):
    """Returns true if you are connected to internet and false otherwise."""
    try:
        urlopen(known_active_url)
    except URLError:
        return False
    return True


def url_is_active(url: str) -> bool:
    """Returns true if you can get the content of the url and false otherwise."""
    try:
        return urlopen(url).get_code() == 200
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
        if url_from == url_to:
            return url_from
        if "File:" in url_from:
            return False
        from_page_html_str: str = urlopen(url_from).read().decode("utf-8")
        internal_link: str = url_to[url_to.find("/wiki/"):]
        return internal_link in from_page_html_str

    has_link_to_input_url.__name__ = f"has_link_to_{url_to}"
    return has_link_to_input_url


def link_iter_to_url_gen(links_list: Iterable[str], sub_domain: str) -> StringGenerator:
    """Modifies the internal links to valid urls and removes non valid urls
    examples: https://en.wikipedia.org/wiki/Israel -> https://en.wikipedia.org/wiki/Israel
    /wiki/Israel -> https://{sub_domain}.wikipedia.org/wiki/Israel"""
    for link in links_list:
        if link.startswith("/wiki/"):
            link = f"https://{sub_domain}.wikipedia.org" + link
        if url_is_wiki_page(link):
            yield link


def wiki_link_back_gen(input_url: str, num_workers: int = 9) -> StringGenerator:
    """A generator function that gets a url to a wikipedia page
     and returns all urls to other wikipedia pages that have a link back to the original page.
    num_workers is the number of processes to use in the thread pool.
    """
    html_string_page: str = urlopen(input_url).read().decode("utf-8")
    link_list: List[str] = re.findall("href=[\"\'](.*?)[\"\']", html_string_page)
    index_start_sub_domain = input_url.index("//") + 2
    index_stop_sub_domain = input_url.index(".")
    sub_domain: str = input_url[index_start_sub_domain:index_stop_sub_domain]
    url_gen: StringGenerator = link_iter_to_url_gen(link_list, sub_domain)
    has_link_to_input: Callable[[str], Optional[str]] = create_has_link_func(input_url)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_url = {executor.submit(has_link_to_input, url): url for url in url_gen}
        for future in as_completed(future_to_url):
            curr_url = future_to_url[future]
            is_linked = future.result()
            if is_linked:
                yield curr_url


def main():
    """The function called when running the file solution.py
       read more in the readme file"""
    if not connected_to_internet():
        print("You are not connected to the internet, Internet is required to run this program.")
        print("Please connect to the internet and try again.")
        return
    print("You are connected to the internet.")

    arguments = sys.argv
    if len(arguments) > 1 and url_is_wiki_page(arguments[1]) and url_is_active(arguments[1]):
        input_url = arguments[1]
    else:
        input_url: str = input("Enter your URL: \n")
        if not url_is_wiki_page(input_url):
            print("The url must also be a working url to an active wikipedia page")
            print("The Requirements are:")
            print("A string")
            print("Full path leading to active page")
            print("Starting with https:// or http://")
            print("Containing .wikipedia.org")
            main()
        if not (url_is_wiki_page(input_url) and url_is_active(input_url)):
            print(f"The page in {input_url} is not active or does not exist.")
            main()

    print("The number of workers must be a literal positive int")
    default_num_workers = min(32, cpu_count() + 5)
    input_message = f"""Enter the number of workers,
    the default value for your computer is: {default_num_workers} """
    num_workers_str = input(input_message)
    if not num_workers_str.isnumeric():
        main()
    num_workers = int(num_workers_str)
    if num_workers == 0:
        main()

    wikipedia_urls: StringGenerator = wiki_link_back_gen(input_url, num_workers)
    print(f"Those are the pages that the page {input_url} has a url to and they have a url to {input_url}")
    print()
    for output_url in wikipedia_urls:
        print(output_url)


if __name__ == "__main__":
    main()
