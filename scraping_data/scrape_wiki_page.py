# import required modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
import numpy as np
 
# get URL
page = requests.get("https://en.wikipedia.org/wiki/Love_It_or_List_It_Vancouver")
 
# scrape webpage
soup = BeautifulSoup(page.content, 'html.parser')
tables=soup.find_all('table',{'class':"wikitable"})
 
df_summary=pd.read_html(str(tables[0]))
# convert list to dataframe
df_summary=pd.DataFrame(df_summary[0])
print(df_summary.head())

episodes = pd.DataFrame(columns = ["season", "ep_num","ep_name","og_air_date", "jillian", "todd"])

for i in range(1, len(tables)-1):
    temp = pd.read_html(str(tables[i]))
    temp=pd.DataFrame(temp[0])

    #format data
    temp.columns = temp.columns.droplevel(0)
    temp["Season no."] = i
    temp = temp.iloc[:-1]
    temp.rename(columns={"Season no.":"season", 
                         "Series no.": "ep_num", 
                         "Episode name":"ep_name", 
                         "Original air date":"og_air_date", 
                         "Jillian":"jillian", 
                         "Todd":"todd"}, inplace = True)
    episodes = episodes.append(temp)

episodes["win"] = np.where((episodes.jillian == "X"), "jillian", "todd")
print(episodes)

df_summary.to_csv("../data/summary_data.csv")
episodes.to_csv(("../data/episodes.csv"))