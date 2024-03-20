LinkedIn Scraper

Code Structure and Overview:

This script facilitates scraping posts and comments from any LinkedIn profile using a search keyword. It consists of two main scripts: raw_file_linkedin.py and buying_signal_linkedin.py, offering ease of use.

Raw_file_linkedin.py:

Utilizes Selenium WebDriver to automate LinkedIn connection and scrolling.
Scrapes posts, placing them in the posts folder with individual text files containing raw HTML.
Scrapes comments in the format: Post_url, Comment, Comment_author, Date_posted, LinkedIn_Post.
For unscraped elements, Null is used, and comments are encapsulated in single quotes for compatibility with CSV parsers.
Running Code:

Step 1:

Pass your username and password to the post_grabber function in raw_file_linkedin.py.
Modify the search variable with the desired boolean expression, ensuring proper spacing around boolean keywords.
Execute the script to generate raw files for each search term in the raw_files folder, including raw_file_linkedin.xlsx for the next step.
Step 2:

Run buying_signal_linkedin.py, which automatically reads the raw file generated in the previous step.
Output an xlsx file named buying_signal_linkedin.xlsx, containing all required information, serving as the final script output.
