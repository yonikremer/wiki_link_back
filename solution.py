"""The solution to the challenge. Read more at the readme file"""


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
    in_wikipedia_org = ".wikipedia.org/wiki/" in url
    if not (is_secure and in_wikipedia_org):
        return False
    return True


def get_has_link_func(url_to: str) -> Callable[[str], Optional[str]]:
    """Given a target url, returns a function that checks if a url has a link back to the target url.
    If that is the case, return the second url, otherwise return None."""
    def has_link(url_from: str) -> Optional[str]:
        if url_from == url_to:
            return url_from
        if "File:" in url_from: 
            return None
        from_page_html_str: str = urlopen(url_from).read().decode("utf-8")
        link_to_page: str = url_to[url_to.find("/wiki/"):]
        if link_to_page in from_page_html_str:
            return url_from
        return None
    return has_link


def link_list_to_url_list(links_list: List[str], language: str) -> Generator[str, None, None]: 
    """Modifies the internal links to valid urls and removes non valid urls"""
    url_list= []
    for link in links_list:
        if link.startswith("/wiki/"):
            url_list.append(f"https://{language}.wikipedia.org" + link)
        else:
            url_list.append(link)
    for url in url_list:
        if is_wiki_page(url):
            yield url


def wiki_link_back_gen(input_url: str, num_workers: int = 9) -> Generator[str, None, None]:
    """A generator function that gets a url to a wikipedia page
     and returns all urls to other wikipedia pages that have a link back to the original page.
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
    """The function called when running the file solution.py
       read more in the readme file"""
    print("The url must also be a working url to an active wikipedia page")
    input_url: str = input("Enter a url to a wikipedia page")
    if not is_wiki_page(input_url):
        main()

    print("The number of workers must be a literal positive int")
    recommended_num_workers = min(32, cpu_count() + 5)
    input_message = f"""Enter the number of workers,
    the recommended value for your computer is: {recommended_num_workers} """
    num_workers_str = input(input_message)
    if not num_workers_str.isnumeric():
        main()
    num_workers = int(num_workers_str)
    if num_workers == 0:
        main()

    wikipedia_urls: Generator[str, None, None] = wiki_link_back_gen(input_url, num_workers)
    print(f"Those are the pages that the page {input_url} has a url to and they have a url to {input_url}")
    print()
    for output_url in wikipedia_urls:
        print(output_url)


if __name__ == "__main__":
    main()
