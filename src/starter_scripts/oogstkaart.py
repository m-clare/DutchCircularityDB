import requests
from bs4 import BeautifulSoup
import re

# base
url = "https://www.oogstkaart.nl"

# material type 47 = Metaal
# search keyword can be any string value (in this case, isolating steel cross sections)
payload={'search_keyword': 'profiel',
         'oogstkaart_material_type[]': '47',
         'viewmode': 'thumb',
         'order': 'DESC',
         'post_per_page': 96}
headers={}
files=[]

response = requests.request("POST", url, headers=headers, data=payload, files=files)

soup = BeautifulSoup(response.text, 'html.parser')

# Get all valid links on the page
links = soup.find_all('a')

# Isolate links that are to product pages
material_links = []

for link in soup.find_all('a'):
    href = link.get('href')
    if re.match('https://www.oogstkaart.nl/materiaal/[a-z]+', href):
        material_links.append(href)

# remove duplicates
material_links = list(set(material_links))

# retrieve material page info
material_info = []

for link in material_links:
    material_response = requests.request('GET', link)
    material_soup = BeautifulSoup(material_response.text, 'html.parser')
    availability = material_soup.find_all("div", class_="availability-item")
    test = availability.find("span")
    print(test)
    specification = material_soup.find_all("div", class_="specification-item")
    material_info.append({'name': link.split('/')[-2],
                          'availability': availability,
                          'specification': specification})

# for material in material_info:
#     items = material['availability']
#     spans = []
#     for item in material['availability']:
#         for element in item:
#             try:
#                 thing = element.find('span')
#                 print(thing)
#                 # if thing:
#                     # print(thing.contents)
#             except TypeError:
#                 pass
#             # thing = re.search('<span.*>(.+)<.*', str(element.string))
            # filtered_items = list(filter(lambda x: re.search('.*span.*', x), item.contents))
        # print(filtered_items )
