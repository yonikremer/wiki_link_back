"""Unit testing for solution.py"""


from unittest import TestCase
import unittest

from link_back import url_is_web_page, link_back_gen, url_is_file

class TestSolution(TestCase):
    """A unittest for solution.py"""
    valid_urls = (
        "https://github.com/urllib3/urllib3",
        "http://github.com/urllib3/urllib3",
        "https://en.wikipedia.org/wiki/Israel",
        "https://en.wikipedia.org/wiki/Red_Sea",
        "https://en.wikipedia.org/wiki/Egypt",
        "https://he.wikipedia.org/wiki/%D7%99%D7%A9%D7%A8%D7%90%D7%9C"
        )

    invalid_urls = (
        "https://ami.wikipedia.org/wiki/Faylo:Jerusalem-Mauerrundgang-64-Sportplatz-2010-gje.jpg",
        "/wiki/Israel",
        "Random text", "", {"key": "value"}, [1, 2, 3], None, 42
        )

    known_url_pairs = (
        ("https://en.wikipedia.org/wiki/Israel",
            "https://en.wikipedia.org/wiki/Red_Sea"),
        ("https://en.wikipedia.org/wiki/Israel",
            "https://en.wikipedia.org/wiki/Egypt"),
        ("https://en.wikipedia.org/wiki/Israel",
            "https://he.wikipedia.org/wiki/%D7%99%D7%A9%D7%A8%D7%90%D7%9C"),
        ("https://en.wikipedia.org/wiki/Israel",
            "https://en.wikipedia.org/wiki/Theodor_Herzl"),
        ("https://requests.readthedocs.io/en/latest/",
            "https://github.com/requests/requests")
        )

    one_sided_pairs = (
        ("https://en.wikipedia.org/wiki/Israel", "https://en.wikipedia.org/wiki/Iron_Age"),
        ("https://en.wikipedia.org/wiki/Israel", "https://en.wikipedia.org/wiki/Middle_school")
        )

    file_urls = (
        "https://en.wikipedia.org/wiki/File:Hatikvah_instrumental.ogg",
        "https://en.wikipedia.org/wiki/File:Hatikvah_instrumental.ogg",
        )


    def test_is_not_solution(self, url_input, url_output):
        """Asserts that url2 is NOT generated from by calling link_back_gen(url1)"""
        for answer in link_back_gen(url_input):
            message = f"{url_output} is generated from {url_input} when is should not."
            self.assertNotEqual(answer, url_output, message)


    def test_is_solution(self, url_input, url_output):
        """Asserts that url2 is generated from by calling link_back_gen(url1)"""
        for answer in link_back_gen(url_input):
            if answer == url_output:
                return
        message = f"{url_output} is not generated from {url_input} but should be."
        self.fail(message)


    def test_known_url_pairs(self):
        """Asserts that the known urls are generated from by calling link_back_gen(url1)"""
        print("Started testing known_url_pairs")
        for url1, url2 in self.known_url_pairs:
            with self.subTest(url1=url1, url2=url2):
                self.test_is_solution(url1, url2)
                self.test_is_solution(url2, url1)
        print("Finished testing known_url_pairs")


    def test_one_sided(self):
        """Asserts that the wiki_link_back_gen does not generate
           a url that does not have a link back to the original page"""
        print("Started testing one_sided")
        for url2, url1 in self.one_sided_pairs:
            with self.subTest(url1=url1, url2=url2):
                self.test_is_not_solution(url1, url2)
                self.test_is_not_solution(url2, url1)
        print("Finished testing one_sided")


    def test_generating_strings(self):
        """Asserts that the link_back_gen is generating strings."""
        print("Started testing generating strings")
        exm_valid_url = "https://requests.readthedocs.io/en/latest/"
        answer_generator = link_back_gen(exm_valid_url, num_workers=1)
        first_ans = next(answer_generator)
        self.assertIsInstance(first_ans, str)
        print("Finished testing generating strings")


    def test_is_web_page(self):
        """Asserts that is_page returns true for valid urls"""
        print("Started testing is_web_page")
        for valid_url in self.valid_urls:
            with self.subTest(valid_url=valid_url):
                self.assertTrue(url_is_web_page(valid_url))

        for invalid_url in self.invalid_urls:
            with self.subTest(invalid_url=invalid_url):
                self.assertFalse(url_is_web_page(invalid_url))

        for file_url in self.file_urls:
            with self.subTest(file_url=file_url):
                self.assertFalse(url_is_web_page(file_url))
        print("Finished testing is_web_page")


    def test_url_is_file(self):
        """Tests the function url_is_file"""
        print("Started testing url_is_file")
        for file_url in self.file_urls:
            with self.subTest(file_url=file_url):
                self.assertTrue(url_is_file(file_url))
        for page_url in self.valid_urls:
            with self.subTest(page_url=page_url):
                self.assertFalse(url_is_file(page_url))
        print("Finished testing url_is_file")


if __name__ == '__main__':
    unittest.main()
