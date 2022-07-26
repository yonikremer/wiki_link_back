from unittest import TestCase
import unittest
from solution import wiki_link_back_gen, is_wiki_page
import random
from typing import Tuple


class TestSolution(TestCase):
    valid_urls: Tuple[str] = (
        "https://en.wikipedia.org/wiki/Israel", 
        "https://en.wikipedia.org/wiki/Red_Sea", 
        "https://en.wikipedia.org/wiki/Egypt",
        "https://he.wikipedia.org/wiki/%D7%99%D7%A9%D7%A8%D7%90%D7%9C"
        )

    invalid_urls: Tuple[str] = (
        "https://docs.python.org/3/library/unittest.html#subtests", 
        "http://en.wikipedia.org/wiki/Red_Sea/",
        "https://mail.google.com/mail",
        "Random text", "", {"key": "value"}, [1, 2, 3], None, 42
        )

    known_url_pairs: Tuple[Tuple[str]] = (
        ("https://en.wikipedia.org/wiki/Israel", "https://en.wikipedia.org/wiki/Red_Sea"),
        ("https://en.wikipedia.org/wiki/Israel", "https://en.wikipedia.org/wiki/Egypt"), 
        ("https://en.wikipedia.org/wiki/Israel", "https://he.wikipedia.org/wiki/%D7%99%D7%A9%D7%A8%D7%90%D7%9C"),
        ("https://en.wikipedia.org/wiki/Israel", "https://en.wikipedia.org/wiki/Theodor_Herzl")
        )

    one_sided_paires: Tuple[Tuple[str]] = (
        ("https://en.wikipedia.org/wiki/Israel", "https://en.wikipedia.org/wiki/Iron_Age"),
        ("https://en.wikipedia.org/wiki/Israel", "https://en.wikipedia.org/wiki/Middle_school")
        )


    def test_is_solution(self, url_1: str, url_2: str) -> None:
        """Asserts that url2 is generated from by calling wiki_link_back_gen(url1)"""
        url2_is_ans_to_url1 = False
        for url_answer_to1 in wiki_link_back_gen(url_1):
            if url_answer_to1 == url_2:
                url2_is_ans_to_url1 = True
                break
        self.assertTrue(url2_is_ans_to_url1)


    def test_is_not_solution(self, url1: str, url2: str) -> None:
        """Asserts that url2 is NOT generated from by calling wiki_link_back_gen(url1)"""
        for url_answer_to1 in wiki_link_back_gen(url1):
            self.assertNotEqual(url_answer_to1, url2, message = f"{url2} is generated from {url1} when is should not.")


    def test_is_wiki_page(self) -> None:
        """Asserts that is_wiki_page returns true for valid urls"""
        for valid_url in self.valid_urls:
            with self.subTest(valid_url=valid_url):
                self.assertTrue(is_wiki_page(valid_url))

        for invalid_url in self.invalid_urls:
            with self.subTest(invalid_url=invalid_url):
                self.assertFalse(is_wiki_page(invalid_url))


    def test_generating_strings(self) -> None:
        """Asserts that the wiki_link_back_gen is generating strings."""
        exm_valid_url: str = random.choice(self.valid_urls)
        answer_generator = wiki_link_back_gen(exm_valid_url, num_workers=1)
        first_ans = next(answer_generator)
        self.assertIsInstance(first_ans, str)


    def test_known_url_pairs(self) -> None:
        """Asserts that the known urls are generated from by calling wiki_link_back_gen(url1)"""
        for url1, url2 in self.known_url_pairs:
            with self.subTest(url1=url1, url2=url2):
                self.test_is_solution(url1, url2)
                self.test_is_solution(url2, url1)
    
    def test_one_sided(self) -> None: 
        """Asserts that the wiki_link_back_gen does not generate a url that does not have a link back to the original page"""
        for url2, url1 in self.one_sided_paires: 
            with self.subTest(url1=url1, url2=url2):
                self.test_is_not_solution(url1, url2)
                self.test_is_not_solution(url2, url1)
            


if __name__ == '__main__':
    unittest.main()
