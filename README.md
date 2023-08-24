# LinkedIn Scraper


This is a script that allows you to scrape posts and comments from any LinkedIn using a search keyword.

### Table of Contents

- Code Structure and Overview
- Runing Code

### Code Structure and Overview
The code is split into two scripts for ease of use. You will see two files, one named **raw_file_linkedin.py** and **buying_signal_linkedin.py**. Don't worry about the post_grabber_linkedin.py. This is only a helper file with useful functions. You DO NOT need you run this file. You only need to run the raw_file_linkedin.py and then the buying_signal_linkedin.py. Raw_file_linkedin will use the Selenium WebDriver to automate connecting and scrolling through LinkedIn. All the posts it scrapes will be placed in the folder called **posts**. There is a seprerate text file for each post containing the raw HTML for the post div. 

The comments are then scraped from the post and is in the format:
<center>Post_url, Comment, Comment_author, Date_posted, LinkedIn_Post</center>
<p></p>
For elements that could not be scraped from the post the value of **Null** was used. The comment and LinkedIn_post were also encapsulated in ' ' so that it would work well with CSV parsers. 

### Running Code
#### Step 1
First pass your username and password to the post_grabber function in raw_file_linkedin.py. Then change the ***search*** variable to be the boolean expression you want to search for. 
**NOTE: This search string can be as long as you want, provided that every boolean keyword has a space character around it. So the search term "NLP and Tech or NLP and Marketing" is acceptable but "NLPand Tech orNLP and Marketing" is not.**
The script will have unpredictable results if the above condition is not met

This will generate all the raw files for each search term and place it in the **raw_files** folder. It will also create a file in there called **"raw_file_linkedin.xlsx"**. This is important for the next step.
#### Step 2
Run the file called **buying_signal_linkedin.py**. This will automatically read the raw file created in the previous step and will output an xlsx file called buying_signal_linkedin.xlsx. This is the final output of the script and contains all the required information.
<p></p>
