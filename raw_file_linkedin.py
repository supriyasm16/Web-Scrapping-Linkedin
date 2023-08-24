from ast import keyword
from bs4 import BeautifulSoup
import re
import glob as g
from openpyxl import Workbook
import os
from posts_grabber_linkedin import post_grabber
from utilities.buying_signal_utilities import buying_signal_utilities
from utilities.raw_file_utilities import *
from tqdm import tqdm
import python_utils

# Add your Boolean search term here
country = "Ireland"
##search = "Natural Language Processing and Tourism and {country} or Natural Language Processing and Hospitality and {country} or Natural Language Processing and Travel and {country} or Natural Language Processing and Crypto and {country} or Natural Language Processing and Blockchain and {country} or Natural Language Processing and Fintech and {country} or Natural Language Processing and Medtech and {country} or Natural Language Processing and Healthtech and {country} or Natural Language Processing and EdTech and {country} or Natural Language Processing and Biotech and {country} or Natural Language Processing and AI and {country} or Natural Language Processing and Robotics and {country} or Natural Language Processing and Autonomous and {country} or Demand generation and Tourism and {country} or Demand generation and Hospitality and {country} or Demand generation and Travel and {country} or Demand generation and Crypto and {country} or Demand generation and Blockchain and {country} or Demand generation and Fintech and {country} or Demand generation and Medtech and {country} or Demand generation and Healthtech and {country} or Demand generation and EdTech and {country} or Demand generation and Biotech and {country} or Demand generation and AI and {country} or Demand generation and Robotics and {country} or Demand generation and Autonomous and {country}".format(country=country)
search = "pvc doors and windows and {country}".format(country=country)
search = re.sub(' and ', ' AND ', search)
search = search.split(' or ')
# Pass username and passwords as args to the post_grabber function
#grabber = post_grabber("********@gmail.com", "***")
a = input('Enter')
bs_utils = buying_signal_utilities()
util = raw_file_utilities()
full_path = (r"C:\Users\HP\Desktop\social_media_data-linkedln\posts") 
filenames = os.listdir(full_path)

for search_term in tqdm(search, desc='Running Search'):
    # Create a new Excel Workbook using openpyxl
    wb = Workbook()
    ws1 = wb.active
    #grabber.run(search=search_term)
    wb_filename= (r"C:\Users\HP\Desktop\social_media_data-linkedln\raw_files\raw_file_linkedin.xlsx")
    #wb_filename = "raw_files/{search}.xlsx".format(search=re.sub(' AND ', '_', search_term))
    # Look in the 'xlsx_files' directory for the files generated from raw_file_linkedin.py
    filenames = os.listdir(full_path)
    # some regex to remove HTML tags
    regex_remove_tag_newline = r'<(.*?)>|\n|\[|\]'
    # Adds header row of CSV
    ws1.append(['Keyword', 'Url', 'Post Content', 'Comment', 'Authors_name'])

    for txt_file in tqdm(filenames, leave=False, desc='Create Raw File'):
        txt_file = os.path.join(full_path, txt_file)
        with open(txt_file, 'r', encoding="utf-8") as file:
            html_text = file.read()
            webpage = BeautifulSoup(html_text, 'html.parser')
            entry = ['Null', 'Null', 'Null', 'Null', 'Null']  # initialize the array to be null
            # get the various parts from the HTML
            authors = webpage.find_all("span", class_="update-components-actor__name t-14 t-bold hoverable-link-text t-black")
            post = webpage.find_all("div", class_="update-components-text relative feed-shared-update-v2__commentary")
            post = re.sub(regex_remove_tag_newline, '', str(post)).lstrip().rstrip()
            comments = webpage.find_all("div", class_="update-components-text relative")
            # post = re.sub(regex_remove_tag_newline, '', str(comments)).lstrip().rstrip()
            comments_authors = webpage.select('span[class^="comments-post-meta__name-text hoverable-link-text"]')
            urn = re.search(r'data-urn="(.*?)"', str(webpage)).group(1)
            # Process the raw HTML and append to the workbook
            if (len(comments_authors) > 0):
                for i in range(len(comments_authors)):
                    span_with_name = re.search('<span aria-hidden="true">(.*?)</span>', str(comments_authors[i]))
                    if span_with_name:
                        comment_author_name = re.sub(regex_remove_tag_newline, '', span_with_name.group(1))
                    else:
                        comment_author_name = re.sub(regex_remove_tag_newline, '',
                                                     str(comments_authors[i])).lstrip().rstrip()

                    cleaned_comment = bs_utils.cleaning_text(comments[i])
                    entry[0] = search_term.lower()
                    entry[1] = 'https://www.linkedin.com/feed/update/{}'.format(urn)
                    entry[2] = "'" + post + "'"
                    entry[3] = "'" + cleaned_comment + "'"
                    entry[4] = comment_author_name.lower()
                    ws1.append(entry)
            else:
                entry[0] = search_term.lower()
                entry[1] = 'https://www.linkedin.com/feed/update/{}'.format(urn)
                entry[2] = entry[2] = "'" + post + "'"
                ws1.append(entry)

    wb.save(wb_filename)


# grabber.exit()
files = util.read_files('raw_files', 'xlsx', 'linkedin')
util.merge_files(files, "xlsx", "linkedin")
