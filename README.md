# The challenge:
In this challenge, the program gets a url to a wikipedia page (let's call is input_page) 
and prints every output_page that satisfies the following conditions:
1. The output_page is a valid url to an active wikipedia page.
2. The output_page has a link to input_page.
3. The input_page has a link to output_page.

# Requirements: 
python 3.7+
Internet connection 

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
I used type hints but I know some people don't use them, I could adjust my style according the team.
I used the following standard libraries:
unittest, random, typing, re (regular expressions), urllib, concurrent.futures, os
I didn't use pytest because it is not a standard library.