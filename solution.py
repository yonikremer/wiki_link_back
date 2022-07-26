from typing import Generator, Callable, Optional, List
import re
from urllib.request import urlopen
from multiprocessing.pool import ThreadPool as Pool
from os import cpu_count


def is_wiki_page(url: str) -> bool:
    """Returns true if url is a url to a wikipedia page"""
    if not isinstance(url, str): 
        return False
    return ".wikipedia.org/wiki/" in url and url.startswith("https://")


def get_has_link_func(url_to: str) -> Callable[[str], Optional[str]]:
    """Given a target url, returns a function that checks if a url has a link to the target url"""
    def has_link(url_from: str) -> Optional[str]:
        """Returns true if url is a link from url_from to url_to and false otherwise"""
        if not is_wiki_page(url_from) or not is_wiki_page(url_to):
            return None
        from_page_html_str: str = urlopen(url_from).read().decode("utf-8")
        link_to_page: str = url_to[url_to.find("/wiki/"):]
        if link_to_page in from_page_html_str: 
            return url_from
        return None
    return has_link


def wiki_link_back_gen(input_url: str, num_proccess: int = cpu_count()) -> Generator[str, None, None]:
    """
    A generator function that gets a url to a wikipedia page and returns all urls to other wikipedia pages 
    that have a link back to the original page.
    num_proccess is the number of processes to use in the thread pool.
    """
    html_string_page: str = urlopen(input_url).read().decode("utf-8")
    url_list: List[str] = re.findall("href=[\"\'](.*?)[\"\']", html_string_page)
    pool = Pool(processes=num_proccess)
    has_link_to_input: Callable[[str], Optional[str]] = get_has_link_func(input_url)
    for linked_page_url in pool.imap_unordered(has_link_to_input, url_list):
        if linked_page_url is not None:
            yield linked_page_url
    


def main():
    # print("A valid url is a string that starts with 'https://' and contains '.wikipedia.org/wiki/'")
    # input_url = input("Enter a url to a wikipedia page")
    # while not is_wiki_page(input_url):
    #     print("The url must be to a wikipedia page according to the requirements above.")
    #     input_url = input("Enter a url to a wikipedia page")
    print("The number of procceses must be a literal positive int")
    input_message = f"Enter the number of procceses, it's recommended to use the number of cpu's which is {cpu_count()}"
    num_procceses_str = input(input_message)
    num_procceses = int(num_procceses_str)
    while not (num_procceses_str.isnumeric() and num_procceses > 0):
        num_procceses_str = input(f"{num_procceses_str} is not a valid literal int, please enter a valid literal int")
        num_procceses = int(num_procceses_str)
    input_url = "https://en.wikipedia.org/wiki/Israel"
    wikipedia_urls = wiki_link_back_gen(input_url, num_procceses)
    print(f"Those are the pages that the page {input_url} has a url to and they have a url to {input_url}")
    print()
    for linked_page_url in wikipedia_urls:
        print(linked_page_url)


if __name__ == "__main__":
    main()
