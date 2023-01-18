import requests
from  bs4 import BeautifulSoup
import csv

jobs = []
# Request 21 pages.
for page in range(1,22):
    url = f"https://careers.google.com/api/v3/search/?distance=50&page={page}&q=security"
    response = requests.get(url)  # Request the API.
    data = response.json()
    # print(data['jobs'])
    # print(len(data['jobs']))
    
    # Each page contain an "jobs" key is a jobs list. 
    for i in range(len(data['jobs'])):
        '''Each job has some keys(title, categories(list type), apply_url, responsibilities, qualifications, locations,company_name,description,education_levels,application_instruction,additional_instructions,created,modified,publish_date,has_remote)'''

        # Filtering:
        categories = ', '.join(data['jobs'][i]['categories'])
        education_levels = ', '.join(data['jobs'][i]['education_levels'])
        responsibilities =  BeautifulSoup(data['jobs'][i]['responsibilities'], "lxml").text.strip()
        qualifications =  BeautifulSoup(data['jobs'][i]['qualifications'], "lxml").text.strip()
        description = BeautifulSoup(data['jobs'][i]['description'], "lxml").text.strip()       
            
        job = {
            "title": data['jobs'][i]['title'],
            "categories": categories,
            "url" : data['jobs'][i]['apply_url'],
            "responsibilities" : responsibilities,
            "qualifications" : qualifications,
            "company name" : data['jobs'][i]['company_name'],
            "description": description, 
            "education levels": education_levels, 
            "has remote": data['jobs'][i]['has_remote'], 
        }

        jobs.append(job)
# Storing the results.
with open(r"/PATH/results.csv","w") as file: # Add the file PATH. 
    writer = csv.DictWriter(file, job.keys())
    writer.writeheader()
    writer.writerows(jobs)
    print("File is created successfully.")
