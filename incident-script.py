import csv
import requests
import http.client

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.headless = True

incident_summary="sample incident summary.csv"
app_owner="sample_app_owner.csv"
form_url="https://docs.google.com/forms/d/1p6L4MeSR8EydHV2lGBa88JsqvhwNs9H09j3oL5FKHlw/"

form_url_view = form_url+"viewform"
form_url_response = form_url+"formResponse"

incident_rows = []
owner_rows = []

def tempFunc():
	with open(incident_summary, 'r') as incident_file:
		incident_reader =csv.DictReader(incident_file)

		for row in incident_reader:

			if not ('staging' in row['environment'] and 'qa' in row['environment'] and 'dev' in row['environment']):
				print(row)
				app_repo = row['app-repo']
				app_name = row['app-name']
				triggered_by = row['triggered-by']
				commited_by = row['commited-by']

				#check for app owner in app owner file

				with open(app_owner, 'r') as owner_file:
					owner_reader =csv.DictReader(owner_file)

					#Getting owner details")

					for row in owner_reader:

						if row['app-repo']==app_repo:
							repo_owner = row['owner']
							print(row['owner'])

							#fill and submit the google form
							driver = webdriver.Chrome(options=options)
							driver.get(form_url)
							driver.implicitly_wait(20)
							app_repo_txt = driver.find_element(By.XPATH, "//span[contains(text(),'App Repo')]/../../../..//input")
							app_repo_txt.click()
							app_repo_txt.send_keys(app_repo)
							repo_owner_txt = driver.find_element(By.XPATH, "//span[contains(text(),'App Owner')]/../../../..//input")
							repo_owner_txt.send_keys(repo_owner)
							repo_owner_txt.click()
							submitbutton = driver.find_element(By.XPATH, "//span[contains(text(),'Submit')]")
							submitbutton.click()
							driver.close()



					owner_rows.append(row)

		incident_rows.append(row)


def main():
	tempFunc()
	



if __name__ == '__main__':
	main()