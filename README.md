# Requirements: 
python 3
internet connection

# Clone:
You can clone the repository using the command:
$ git clone https://github.com/yonikremer/wiki_link_back
Or using the green "code" button in the github page

# Running instructions:
run the commands:
$ cd PATH_TO_REPOSETORY
$ python3 solutions.py

Than you will the following messages: 
A valid url is a string that starts with 'https://' and contains '.wikipedia.org/wiki/'
Enter a url to a wikipedia page

Than you need to enter a url according to the requirements in the message
If the input is NOT valid, tou will get the messages:

The url must be to a wikipedia page according to the requirements above.
Enter a url to a wikipedia page

Untill you will enter a valid url

If the url is valid the program will print:
Those are the pages that the page input_url has a url to and they have a link to input_url
And than prints every the output_url the satisfy:
for your_input, output_url:
    both are valid urls to a wikipedia articale
    the articale in your_input has a url to the articale in output_url
    the articale in output_url has a url to the articale in your_input
Every url will be printed in a separate line
