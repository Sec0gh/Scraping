import requests
import csv
from itertools import zip_longest
from bs4 import BeautifulSoup
from termcolor import colored

links = []  # List To store all grabbed links from the main page.
self_reported_tags = [] # To store the self reported tags data.
market_names = []       # To store all market names.

def Grab_all_links():
    url = "https://coinmarketcap.com/all/views/all/"
    response = requests.get(url)
    main_page = BeautifulSoup(response.content, "lxml")
    tags = main_page.find_all("tr", {"class":"cmc-table-row"})
    for i in range(0,len(tags)):
        links.append(tags[i].find("a",{"class": "cmc-link"}).attrs["href"])  
    print(colored("[+] All links has been collected.", "green")) 


def scraper():
    heading_tags = []
    # Request each link.
    for i in range(len(links)): 
        url = f"https://coinmarketcap.com{links[i]}"
        response = requests.get(url)
        page = BeautifulSoup(response.content, "lxml")
        
        headings = page.find_all("div", {"class":"heading"})
        for i in range(len(headings)):
            heading_tags.append(headings[i].text)
        
        heading_tags = list(set(heading_tags))  
        for i in range(len(heading_tags)):
            if "Self-Reported Tags" in heading_tags[i]:
                try:
                    name = page.find("span", {"class":"sc-1d5226ca-1 fLa-dNu"}).text
                    tags = page.find_all("div",{"class":"sc-b83c9ecb-4 gVqBsE"})

                    desired_div = tags[0]
                    desired_data_divs = desired_div.find_all("div")
                    data = [div.text for div in desired_data_divs] 
                    
                    market_names.append(name)
                    self_reported_tags.append(data)
                except:
                    break

# print(len(market_names)) 
# print("_________________________________________")
# print(len(self_reported_tags))   

def main():
    Grab_all_links()
    print(colored("please, wait for the Scraper tool to be working now,","green"))
    print(colored("Loading...","green"))
    scraper()
    columns = [market_names, self_reported_tags]
    rows = zip_longest(*columns)    # unpacking the columns list.
    with open("Self Reported Tags.csv","w") as file: 
        writer = csv.writer(file)
        writer.writerow(["Market Name", "Self Reported Tags"]) # Write headers.
        writer.writerows(rows)
        print(colored("[+] File is created successfully.","green",attrs=['bold']))

if __name__ == '__main__':
    main()