# Doc Grabber

A simple python application to help 'download' pdf documents from websites that allow users to view them as individual images/pages.

Currently implementation is kept minimal becasue I just wanted to get this working for a handful of particular cases rather than creating a clean, well developed, multipurpose, fully re-usable piece of software.

## Problem Description

Often when viewing e-books online, a "download as pdf" is not available to the reader. Upon inspection, often these books are stored with a sequintial naming format as individual pages. For example:
```
https://test_website.com/a_useful_book/page1.jpg
https://test_website.com/a_useful_book/page2.jpg
...
```
Where the only difference between each URL is a numeric value somewhere within the path. 

If you want to access the book for offline reading you could manually save each image and view later however this is clunkly and annoying. 

## Installation

Clone from git or download zip from git and unzip in a local directory.

## Usage

First, the user needs to get the link manually from the web page. This can normally be done pretty easily using Chrome developer tools and inspecting the page.

Once the link has been aquired, open a command prompt or terminal and navigate the working directory to the project folder.

### Prompted
To run the script normally, run the following command in the terminal/command prompt:
```
python main.py
```
This will run the script and prompt the user for necassary inputs. The script expects the following inputs:
```
Left hand side of the URL - everything to the left of the variable number.
Right hand side of the URL - everything to the right of the variable number (normally just the file extension).
Number of pages.
Output file name.
```
Example inputs:
```
First half of URL:  https://test_website.com/a_useful_book/page
Second half of URL: .jpg
Page count: 2
Output file name: a_useful_book.pdf
```
### Config File
Alternatively the inputs can be passed in using a config file. To pass in parameters using a config file use the following command:
```
python main.py config_file
```
Where config_file is the name of the config file relative to the scripts working directory and has the following eample structure:
```
https://test_website.com/a_useful_book/page
.jpg
2
a_useful_book.pdf
```
## A Note From The Author
This script has been designed for personal use as a research tool to help develop my skills and familiarity with GitHub and Python. 

Please use considerately. Make sure you understand the potential implications of using a web scraping tool before using it. 

Feedback, issues, queries and concerns all welcome.
