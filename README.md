# The challenge:
In this challenge, the program gets a url to a wikipedia page (let's call is input_page) 
and return every output_page that satisfies the following conditions:
1. The output_page is a valid url to an active wikipedia page.
2. The output_page has a link to input_page.
3. The input_page has a link to output_page.

# Requirements: 
python 3.7+
Internet connection 

# Clone:
You can clone the repository using the command:
'$ git clone https://github.com/yonikremer/wiki_link_back'
Or using the green "code" button in the github page

# Running instructions:
Run the commands:
'$ cd PATH_TO_REPOSITORY'
'$ python3 solutions.py'
If that doesn't work, replace 'python3' with 'python', 'py3' and 'py'

Than you will the following messages: 
A valid url is a string that starts with 'https://' and contains '.wikipedia.org/wiki/'
Enter a url to a wikipedia page

Than you need to enter a url according to the requirements in the message

Than you will get the following message:
The number of workers must be a literal positive int
Enter the number of workers, the recommended value for your computer is: ____

Than you need to enter the maximum number of workers

If the url and number of workers are valid the program will print:
Those are the pages that the page input_url has a url to and they have a link to input_url
And than prints every the output_url the satisfy:
for your_input, output_url:
	>both are valid urls to a wikipedia pages
    >the page in your_input has a url to the page in output_url
    >the page in output_url has a url to the page in your_input
Every url will be printed in a separate line
