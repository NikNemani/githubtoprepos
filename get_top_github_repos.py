import requests
import time
import pandas as pd
import sqlalchemy as sq
##

urls = [ 
"https://api.github.com/search/repositories?q=stars:%3E=1000+language:javascript&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:python&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:java&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:golang&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:rust&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:dart&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:c#&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:c&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:cpp&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:typescript&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:swift&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:php&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:perl&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:shell&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:kotlin&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:ruby&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:tsql&sort=stars&order=desc"
, "https://api.github.com/search/repositories?q=stars:%3E=1000+language:scala&sort=stars&order=desc"
]
data = []

def gather_data(response):
    targetkeys = ["id","name", "description", "language", "html_url", "stargazers_count", "forks", "created_at", "updated_at"]
    for item in response : # each item is a dict
        tempdict = {key: item[key] for key in targetkeys}
#        tempdict['license'] = item['license'].get('name') # item['license'] is a dict
        data.append(tempdict)

for url in urls:
    print(url)
    response = requests.get(url)
    print("response.status_code =  ", response.status_code)
    if response.status_code == 200 :
        response = response.json()['items'] ## response will be a list of dictionaries
        gather_data(response)
    else :
        response.text

    time.sleep(5) ## to make sure we don't get into github rate limits

df = pd.DataFrame(data).drop_duplicates().rename(columns = {'stargazers_count':'stars'})

db = sq.create_engine('sqlite:///github.db')

df.to_sql(name="toprepos", con=db, if_exists='replace', index=False)

