from splinter import Browser
from bs4 import BeautifulSoup
import selenium 
from selenium import webdriver
from splinter.exceptions import ElementDoesNotExist
import csv
import re
import time
import datetime
from datetime import tzinfo
import pytz
from pytz import timezone
import logging
import os
import shutil
from pathlib import Path
from logging.handlers import WatchedFileHandler

time.time()

caught = []
caught2 = []
caught3 = []
account_list =[]
accounts_that_pass = []
accounts_that_failed = []

logger = logging.getLogger()
log_level = logging.DEBUG

logFormatter = logging.Formatter("%(message)s")

handler = WatchedFileHandler("/PATH/Captured.txt")
handler.setFormatter(logFormatter)
handler.setLevel(log_level)
logger.addHandler(handler)
logger.setLevel(log_level)

## Rotate logs after each parse of the downloaded page
def rotate_log():
    try:
        #print("Try block...")
        if os.stat("/PATH/Captured.txt").st_size > 0:
            time = str(datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d_%H-%M-%S"))
            shutil.move("/PATH/Captured.txt", "/PATH/Captured.txt"+time)

    except Exception as e:
        print(e)

## Open account file and create a list of accounts to check.
with open("PATH/accounts.csv",'r') as acct_file:
	acct_searches = csv.reader(acct_file)
	for lines in acct_searches:
		account_list.extend(lines)
		for acct in account_list:
			output = open((acct.strip() + '.txt'),'w')

p = open(r"/PATH/accounts_pass.txt", "w")
f = open(r"/PATH/accounts_fail.txt", "w")

## Open browser and login to Salesforce
browser = Browser() #"firefox"
browser.visit('https://salesforce.com/')
browser.fill('username', 'USERNAME')
browser.fill('pw', 'PASSWORD')
button = browser.find_by_name('Login')
button.click()

print("Waiting on timer: ")
## Timer to allow access to email for two factor authentication
time.sleep(60)
print("TImer expired... Performing searches")

val = 0
test = 0

## Search account number and navigate to Cases page to copy html and begin regex search. If Cases has < 6 cases skip expanding the page and just view the html.##
for i in account_list:		
	account = account_list[val]
	browser.fill('str', int(account))
	browser.find_by_id('phSearchButton').first.click()
	print("Searching...")
	time.sleep(2)
	
	try:
		browser.find_by_id('showMore-500').first.click()
		browser.find_by_id('Case_body')
		time.sleep(2)
		content = browser.html
		time.sleep(2)
	except ElementDoesNotExist:
		time.sleep(2)
		content = browser.html
		time.sleep(2)

	## If file exists, use it. If it does not excist open one
	my_file = Path("/PATH/Captured.txt")

	if my_file.is_file():
		reader = open("/PATH/Captured.txt")
	else:
		reader = open("/PATH/Captured.txt")

	## Write html to file
	logger.debug(content)

	for line in reader:
		line = line.rstrip()
		a = re.findall('(\sFraud\s)', line)
		a2 = re.findall('(\sfraud\s)', line)
		b = re.findall('(\sCollections\s)', line)
		b2 = re.findall('(\scollections\s)', line)
		c = re.findall('(\sZzzzzzzz\s)', line)
		c2 = re.findall('(\szzzzzzzz\s)', line)

		caught.extend(a)
		caught.extend(a2)
		caught2.extend(b)
		caught2.extend(b2)
		caught3.extend(c)
		caught3.extend(c2)

		test = 0

		if len(caught) > 0:
			test = 1
		elif len(caught2) > 0:
			test = 1
		elif len(caught3) > 0:
			test= 1
		else:
			test = 0
	

		# If list contains > 0 keyword matches the account number will be added to "Accounts_fail.txt", if list = 0 the account number will be added to the "Accounts_pass.txt" file
	if test == 0:
		accounts_that_pass.extend(account)
		p.write("Account Passed: " + str(account) +"\n")
		val = val + 1

	else:
		accounts_that_failed.extend(account)
		f.write("Account Failed: " + str(account)+"\n")
		val = val + 1

	time.sleep(2)
	rotate_log()
	caught.clear()
	caught2.clear()
	caught3.clear()
	print("Rotating log")