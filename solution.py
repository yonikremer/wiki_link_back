from typing import Generator, List
import re
from urllib.request import urlopen


def is_wiki_page(url: str) -> bool:
    """Returns true if url is a link to a wikipedia page"""
    if not isinstance(url, str): 
        return False
    return ".wikipedia.org/wiki/" in url and url.startswith("https://")


def has_link(url_from: str, url_to: str) -> bool:
    """Returns true if url is a link from url_from to url_to and false otherwise"""
    if not is_wiki_page(url_from) or not is_wiki_page(url_to):
        return False
    from_page_html_str: str = urlopen(url_from).read().decode("utf-8")
    internal_link_to_page = url_to[url_to.find("/wiki/"):]
    return internal_link_to_page in from_page_html_str


def wiki_link_back_gen(input_url: str) -> Generator[str, None, None]:
    """
    A generator function that gets a link to a wikipedia page and returns all links to other wikipedia pages 
    that have a link back to the original page
    """
    string_page = urlopen(input_url).read().decode("utf-8")
    url_list = re.findall("href=[\"\'](.*?)[\"\']", string_page)
    for linked_page_url in url_list:
        if has_link(linked_page_url, input_url):
            yield linked_page_url
    


def main():
    input_link = input("Enter a link to a wikipedia page")
    if not is_wiki_page(input_link):
        print("The link must be to a wikipedia page.")
        print("please run the program again with a valid link")
        print("A valid link is a string that starts with 'https://' and contains '.wikipedia.org/wiki/'")
        return
    # input_link = "https://en.wikipedia.org/wiki/Israel"
    wikipedia_links = wiki_link_back_gen(input_link)
    for linked_page_url in wikipedia_links:
        print(linked_page_url)


if __name__ == "__main__":
    main()
