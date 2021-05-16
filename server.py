import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from bs4 import BeautifulSoup
from flask import Flask
app = Flask(__name__)


res = requests.get("https://www.mohfw.gov.in/")
soup = BeautifulSoup(res.text, 'html.parser')


a = soup.find_all(class_='mob-hide')
active = a[1].getText().split()
discharged = a[3].getText().split()
deaths = a[5].getText().split()
total = [int(active[0]), int(discharged[0]), int(deaths[0])]
new_case = [active[1], discharged[1], deaths[1]]


for i, j in enumerate(new_case):
    j = j[1:len(j)-1]
    new_case[i] = j
print("                                                 In new cases in India:\nActive :\n      ",
      new_case[0], " Discharged :", new_case[1], "Deaths :", new_case[2])
print('\n')
print("                                                 In total cases India:\nActive :\n       ",
      total[0], " Discharged :", total[1], "Deaths :", total[2])
print('\n')


stateCode = {
    'Andaman and Nicobar Islands': "AN",
    'Andhra Pradesh': "AP",
    'Arunachal Pradesh': "AR",
    'Assam': "AS",
    'Bihar': "BR",
    'Chandigarh': "CT",
    'Chhattisgarh': "CH",
    'Delhi': "DL",
    'Dadara & Nagar Havelli': "DN",
    'Goa': "GA",
    'Gujarat': "GJ",
    'Haryana': "HR",
    'Himachal Pradesh': "HP",
    'Jammu and Kashmir': "JK",
    'Jharkhand': "JH",
    'Karnataka': "KA",
    'Kerala': "KL",
    'Ladakh': "LA",
    'Madhya Pradesh': "MP",
    'Maharashtra': "MH",
    'Manipur': "MN",
    'Meghalaya': "ML",
    
    'Mizoram': "MZ",
    'Nagaland': "NL",
    'Odisha': "OR",
    'Puducherry': "PY",
    'Punjab': "PB",
    'Rajasthan': "RJ",
    'Sikkim': "SK",
    'Tamil Nadu': "TN",
    'Telengana': "TG",
    'Tripura': "TR",
    'Uttarakhand': "UT",
    'Uttar Pradesh': "UP",
    'West Bengal': "WB"
}

stateRes = requests.get('https://api.covid19india.org/v4/data.json')
jsonData = stateRes.json()
name = input("                                                 Enter state name\n").title()
print('\n')

for i, j in stateCode.items():
    if name in i:
        print(name, " ", jsonData[j]['total'])
        keys = jsonData[j]['total'].keys()
        values = jsonData[j]['total'].values()
        plt.bar(keys, values)
        plt.ylim([5000, 1000000])
        plt.show()
        break

curr_state = input("                                                 Which state are you in:        \n").title()
final_state = []
print('\n')
print("                                                 Enter the 3 states you wish to travel: \n       ")
for i in range(0, 3):
    a = input().title()
    final_state.append(a)
print(final_state)
ls = []
state_ls = []
for a in final_state:
    for i, j in stateCode.items():
        if a in i:
            state_ls.append(a)
            dt = jsonData[j]['total']
            ls.append(dt)

print(ls)
df = pd.DataFrame().from_dict(ls)
df["state"] = state_ls
print(df)
f, axes = plt.subplots(2, 2)
sns.barplot(data=df, x='state', y='confirmed', hue='state',
            ax=axes[0][0]).set_title('Confirmed')
sns.barplot(data=df, x='state', y='recovered', hue='state',
            ax=axes[0][1]).set_title('Recovered')
sns.barplot(data=df, x='state', y='tested', hue='state',
            ax=axes[1][0]).set_title('Tested')
sns.barplot(data=df, x='state', y='deceased', hue='state',
            ax=axes[1][1]).set_title('Deceased')
plt.tight_layout()
plt.show()
