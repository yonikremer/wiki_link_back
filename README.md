# The challenge:

## My description:
In this challenge, the program gets a url to a wikipedia page (let's call is input_page) 
and prints every output_page that satisfies the following conditions:
1. output_page is a valid url to an active wikipedia page.
2. output_page has a link to input_page.
3. input_page has a link to output_page.

## As sent to me:
In this exercise you will write a computer program that receives a URL to a Wikipedia article on the command line. The program will print a list of URLs to other Wikipedia articles:

that are linked to from the original article
and that also link back to it.
the program will print one URL (that is linked and links back) per line to stdout
For example, if we use the article about Israel

```$ python my-program.py https://en.wikipedia.org/wiki/Israel```

Then the article about Theodor Herzl will be among the results, since he is a very important figure in Israeli history - and thus the two articles link to each other.

However (at least at the time of writing this document), the Israel article links to the Iron Age article, but the Iron Age article does not link back to Israel.

To summarize this example, a correct program will print the link to the Theodor Herzl article, but not the link to the Iron Age article.

### Some rules:

You may only use modules in the Python standard library.
You should submit your work as a github repository, with a short README.md file that has instructions on how to run your program.
You should not use comments in your code - try to make the code readable without comments
bonus: parallelize your program so that it completes faster.

# Requirements: 
python 3.10+ and Internet connection.

The program should run in older versions of Python, but it wasn't tested.

# Clone:
You can clone the repository using the command:
'$ git clone https://github.com/yonikremer/wiki_link_back'
Or using the green "code" button in the github page to download the repository as a zip file and then unzip it.

# Running instructions
Run the commands:
```$ cd PATH_TO_REPOSITORY```
```$ python solution <{your url} {maximum number of workers}>```

The requirements for the url:
The url must also be a working url to an active wikipedia page
The Requirements are:
A string
Full path leading to active page
Starting with https:// or http://
Containing .wikipedia.org

If that doesn't work, try replacing 'python' with 'py', 'py3' and 'python3'.
Or simply run solution.py using the code editor

If the url you provided is not valid, you will the following messages: 
The url must also be a working url to an active wikipedia page
The Requirements are:
A string
Full path leading to active page
Starting with https:// or http://
Containing .wikipedia.org

Than you will get the following message:
Enter the number of workers,
the recommended value for your computer is:

If the url and number of workers are valid the program will print:
Those are the pages that the page input_url has a url to and they have a link to input_url
And than prints every the output_url according to the rules in the first section.

# Testing:
You can my unit tests using the command:
'$ python3 test_solution.py'
Notice that testing could be slow because it's running the program many times.

# Other notes:
I used the following standard libraries:
unittest, random, typing, re (regular expressions), urllib, concurrent.futures, os
I didn't use pytest because it is not a standard library.