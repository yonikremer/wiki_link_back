from typing import Generator, Callable, Optional, List
import re
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count


def is_wiki_page(url: str) -> bool:
    """Returns true if url is a url to an existing wikipedia page and false otherwise."""
    if not isinstance(url, str): 
        return False
    is_secure = url.startswith("https://")
    is_wiki_articale = ".wikipedia.org/wiki/" in url
    if not (is_secure and is_wiki_articale): return False
    if "File:" in url: return False
    return True


def get_has_link_func(url_to: str) -> Callable[[str], Optional[str]]:
    """Given a target url, returns a function that checks if a url has a link to the target url"""
    def has_link(url_from: str) -> Optional[str]:
        """Returns true if url is a link from url_from to url_to and false otherwise"""
        from_page_html_str: str = urlopen(url_from).read().decode("utf-8")
        link_to_page: str = url_to[url_to.find("/wiki/"):]
        if link_to_page in from_page_html_str: return url_from
        return None
    return has_link


def link_list_to_url_list(links_list: List[str], language: str) -> Generator[str, None, None]: 
    """Modifies the internal links to valid urls and removes non valid urls"""
    for i in range(len(links_list)):
        if links_list[i].startswith("/wiki/"):
            links_list[i] = f"https://{language}.wikipedia.org" + links_list[i]
    for url in links_list:
        if is_wiki_page(url): 
            yield url


def wiki_link_back_gen(input_url: str, num_workers: int = 9) -> Generator[str, None, None]:
    """
    A generator function that gets a url to a wikipedia page and returns all urls to other wikipedia pages 
    that have a link back to the original page.
    num_workers is the number of processes to use in the thread pool.
    """
    html_string_page: str = urlopen(input_url).read().decode("utf-8")
    link_list: List[str] = re.findall("href=[\"\'](.*?)[\"\']", html_string_page)
    index_start_language = input_url.index("//") + 2
    index_stop_language = input_url.index(".")
    language: str = input_url[index_start_language:index_stop_language]
    url_gen: Generator[str, None, None] = link_list_to_url_list(link_list, language)
    has_link_to_input: Callable[[str], Optional[str]] = get_has_link_func(input_url)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_url = {executor.submit(has_link_to_input, url): url for url in url_gen}
        for future in as_completed(future_to_url):
            curr_url = future_to_url[future]
            is_linked = future.result() is not None
            if is_linked:
                yield curr_url


def main():
    # print("A valid url is a string that starts with 'https://' and contains '.wikipedia.org/wiki/'")
    # input_url = input("Enter a url to a wikipedia page")
    # if not is_wiki_page(input_url): main()
    # input_url = "https://en.wikipedia.org/wiki/Israel"
    input_url = "https://en.wikipedia.org/wiki/Red_Sea"

    print("The number of workers must be a literal positive int")
    recomended_num_workers = min(32, cpu_count() + 5)
    input_message = f"""Enter the number of workers, the recommended 
                        value for your computer is: {recomended_num_workers} """
    num_workers_str = input(input_message)
    if not num_workers_str.isnumeric(): main()
    num_workers = int(num_workers_str)
    if num_workers == 0: main()

    wikipedia_urls = wiki_link_back_gen(input_url, num_workers)
    print(f"Those are the pages that the page {input_url} has a url to and they have a url to {input_url}")
    print()
    for linked_page_url in wikipedia_urls:
        print(linked_page_url)


if __name__ == "__main__":
    main()
