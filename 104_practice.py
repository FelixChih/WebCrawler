import requests, random
import json
from bs4 import BeautifulSoup
import pandas as pd
import os

path = r"./104"
if not os.path.exists(path):
    os.mkdir(path)

page = 1
columns = ['Job Title', 'Company Name', 'Content', 'Python', 'R', 'MySQL', 'Excel', 'Google Analytics']

Job_Title = []
Company_name = []
Content = []
Python = []
R = []
MySQL = []
Excel = []
Google_Analytics = []
Tableau = []

for x in range(30):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E6%95%B8%E6%93%9A%E5%88%86%E6%9E%90&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page={}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'.format(page)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Referer": "https://www.104.com.tw/job/3g1gd?jobsource=jolist_a_relevance",
               "Cookie": "__auc=c93ccca1181dcc82eb2a88478b6; job_same_ab=1; _gcl_au=1.1.439328136.1657266516; luauid=921238015; _hjSessionUser_601941=eyJpZCI6IjUwZjBkMmIzLTAzNzctNTJkZS04MmIzLTllYTFhZWI3N2EwZiIsImNyZWF0ZWQiOjE2NTcyNjY1MTYxNzgsImV4aXN0aW5nIjp0cnVlfQ==; TS01e1e367=01180e452de7d1c1a47e21d6b66ad3964bf7476f2c72c38f89f48bfe8f63c77b68c5f80227cbf84d9beec2f516f8d9b9dcdaaf7dc9f5e4d37ccc3d6676a42244b7446d489f8eca1e97abbf2a6cf269b513df9b0cd83dc46f3a95b25c1a9fc8baef5064dede; _ga_R9FVPY79LQ=GS1.1.1657437842.1.0.1657437846.56; bprofile_history=%5B%7B%22key%22%3A%2259glysw%22%2C%22custName%22%3A%22(%E7%B8%BD%E5%85%AC%E5%8F%B8)%E5%8D%97%E5%B1%B1%E4%BA%BA%E5%A3%BD%E4%BF%9D%E9%9A%AA%22%7D%5D; cust_same_ab=2; c_job_view_job_info_nabi=3g1gd%2C2004001010%2C2003002008; _gaexp=GAX1.3.Kf9mni78Qdi0oS-SgI41PA.19257.2; __asc=179da0e6181f17727fa637d1e9d; _gid=GA1.3.1922208037.1657613529; ALGO_EXP_6019=A; ALGO_EXP_12509=G; _ga=GA1.3.313269257.1657266516; lup=921238015.4623532291991.5035849152215.1.4640712161167; lunp=5035849152215; _hjSession_601941=eyJpZCI6IjQ5YmQyZTc4LThhN2ItNDE3Zi1hYmMwLTVmOTg5NTI0Njg0NiIsImNyZWF0ZWQiOjE2NTc2MTM1NDYwNzIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; TS016ab800=01180e452dd236bf9b692362166b065f15db670f948d1c32621aa7fd9a93841df1d36025c4834d0dba01f42f0b1d667008a6154d4ee93d323d935f39d17d301f5f874dbaf973906ff503e953d5ec63d49068f35799b0462c8f9ea59a2fba805e4721e01e6cf182c170bfffd99679c2f45efc5f2686; _ga_W9X1GB1SVR=GS1.1.1657613517.12.1.1657615072.60; _ga_FJWMQR9J2K=GS1.1.1657613517.12.1.1657615072.60; _ga_WYQPBGBV8Z=GS1.1.1657613517.12.1.1657615072.60",
               "Connection": "keep-alive"}

    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, "html.parser")

    titles = soup.select("div.b-block__left h2 a")
    company = soup.select("div.b-block__left ul li a")

    for x, y in zip(titles, company):
        InLink = x["href"].split("/")[4][0:5]
        content_url = "https://www.104.com.tw/job/ajax/content/" + InLink
        content_res = requests.get(content_url, headers = headers)
        content = content_res.json()
        Job_Title.append(x.text)
        Company_name.append(y.text)
        Content.append(content["data"]["jobDetail"]["jobDescription"])

        skill = content["data"]["condition"]["specialty"]
        if "Python" in str(skill):
            Python.append("O")
        else:
            Python.append("")

        if "R" in str(skill):
            R.append("O")
        else:
            R.append("")

        if "MySQL" in str(skill):
            MySQL.append("O")
        else:
            MySQL.append("")

        if "Excel" in str(skill):
            Excel.append("O")
        else:
            Excel.append("")

        if "Google Analytics" in str(skill):
            Google_Analytics.append("O")
        else:
            Google_Analytics.append("")

        if "Tableau" in str(skill):
            Tableau.append("O")
        else:
            Tableau.append("")

    page += 1

# Use Pandas
col_1 = "Job Title"
col_2 = "Company Name"
col_3 = "Content"
col_4 = "Python"
col_5 = "R"
col_6 = "MySQL"
col_7 = "Excel"
col_8 = "Google Analytics"
col_9 = "Tableau"

data = pd.DataFrame({col_1:Job_Title[11:], col_2:Company_name[11:], col_3:Content[11:], col_4:Python[11:], col_5:R[11:],
                     col_6:MySQL[11:], col_7:Excel[11:], col_8:Google_Analytics[11:], col_9:Tableau[11:]})

data.to_csv("TGI102_02_遲名恩.csv")
