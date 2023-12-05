# source : https://wikis.ec.europa.eu/display/EUROSTATHELP/API+-+Getting+started+with+statistics+API
# eurostat API builder: https://ec.europa.eu/eurostat/web/query-builder/tool
# description : algorithm pulls quarterly Greek GDP data from eurostat and coverts it to monthly

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# get status code of the API below and raise exception in case of HTTP errors
URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&geo=EL&unit=CP_MEUR&na_item=B1GQ&s_adj=NSA&lang=en"

try:
    response_API = requests.get(URL)
    response_API.raise_for_status()
    print("status_code: ", response_API.status_code, "\n")
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

# generate json object obj
data = response_API.text
obj = json.loads(data)

# print object to inspect json structure
index_gdp_dict = obj["value"]
print("GDP values:\n", index_gdp_dict, "\n")

quarter_index_dict = obj["dimension"]["time"]["category"]["index"]
print("Quarter values:\n", quarter_index_dict, "\n")

# convert dictionaries to dataframes
gdp = pd.DataFrame(list(index_gdp_dict.items()), columns=['Key', 'GDP'])
gdp['Key'] = gdp['Key'].astype(int)
quarter = pd.DataFrame(list(quarter_index_dict.items()), columns=['Quarter', 'Key'])
print("GDP dataframe:\n", gdp, "\n Quarter dataframe:\n", quarter)

# generate the GDP dataset
df = pd.merge(gdp, quarter, on='Key')
df = df.drop(columns=['Key'])
df = df[['Quarter', 'GDP']]
print("Quarter - GDP dataframe:\n", df)

'''
# plot Greek GDP
fig, ax = plt.subplots()
ax.plot(df["Quarter"], df["GDP"], linestyle="--", marker="o")
first_year = min(df["Quarter"])
last_year = max(df["Quarter"])
ax.set_title(f"Greek GDP in million € from {first_year} until {last_year}", fontweight="bold")
ax.set_xlabel("Year-Quarter", fontweight='bold')
ax.set_ylabel("GDP (million €)", fontweight='bold')
ax.xaxis.set_major_locator(MultipleLocator(7))

# plt.show()'''

# convert quarter column to datetime
df['Quarter'] = pd.to_datetime(df['Quarter'])
print("\nQuarterly GDP data as dates :\n", df)
# create Datetime index for df
df['datetime_index'] = pd.DatetimeIndex(df['Quarter'])
print("\nUpdated df :\n", df)
df = df.set_index('datetime_index')
print("\nIndexed df :\n", df)

# resample quarterly GDP data to monthly level
df_resampled = df.resample('M').ffill()
df_resampled["Month"] = df_resampled.index
df_resampled = df_resampled[["Quarter", "Month", "GDP"]]
print("\nResampled df :\n", df_resampled)

'''
# plot Greek GDP
fig2, ax2 = plt.subplots()
ax2.plot(df_resampled["Month"], df_resampled["GDP"], linestyle="--", marker="o")
first_point = min(df_resampled["Month"]).strftime('%m/%Y')
last_point = max(df_resampled["Month"]).strftime('%m/%Y')
ax2.set_title(f"Greek GDP in € million from {first_point} until {last_point}", fontweight="bold")
ax2.set_xlabel("Month", fontweight='bold')
ax2.set_ylabel("GDP (€ million)", fontweight='bold')
# ax.xaxis.set_major_locator(MultipleLocator(7))

plt.show()'''


fig, ax = plt.subplots(2)
ax[0].plot(df["Quarter"], df["GDP"], linestyle="--", marker="o")
ax[1].plot(df_resampled["Month"], df_resampled["GDP"], linestyle="--", marker="o")
first_point = min(df_resampled["Month"]).strftime('%m/%Y')
last_point = max(df_resampled["Month"]).strftime('%m/%Y')
# ax[0].set_title(f"Greek GDP in € million from {first_point} until {last_point}", fontweight="bold")
fig.suptitle(f"Greek GDP in € million from {first_point} until {last_point}", fontweight="bold")
ax[0].set_xlabel("Quarter", fontweight='bold')
ax[0].set_ylabel("GDP (€ million)", fontweight='bold')
ax[1].set_xlabel("Month", fontweight='bold')
ax[1].set_ylabel("GDP (€ million)", fontweight='bold')
# ax[0].xaxis.set_major_locator(MultipleLocator(7))

plt.show()

# print('\nmax : ', max(df_resampled["Month"]))
