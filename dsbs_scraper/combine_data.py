
import os
from bs4 import BeautifulSoup
import csv
import io
import re
import pandas as pd
import sqlite3

directory = 'data'

def split_data(data):
    data_io = io.StringIO(data)
    reader = csv.reader(data_io)
    for row in reader:
        return row


def extract_data_from_htmls():

    headers = ["view","firm_name","person","title","address_line_1","address_line_2","city","state","zip","capabilities","email","website","area"]
    with open('all_states.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)


    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            with open(f, "r", encoding="utf-8") as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, "html.parser")
                pre_tag = soup.find("pre")
                rows = str(pre_tag).split("\n")

                cols = ["view","firm_name","person","title","address_line_1","address_line_2","city","state","zip","capabilities","email","website"]
                area = filename.split("_")[1]
                rows = rows[1:]
                for r in rows:
                    actual_data = {}

                    row_data = r.split('","')


                    for i in range(len(row_data)):
                        if cols[i] == "view":
                            pattern = r'href="([^"]+)"'
                            match = re.search(pattern, row_data[i])
                            if match:
                                href_value = match.group(1)
                                actual_data[cols[i]] = "https://dsbs.sba.gov" + href_value + " "
                            else:
                                actual_data[cols[i]] = ""
                        elif cols[i] == "email":
                            match = re.search(r'>([^<]+)<', row_data[i])
                            if match:
                                inner_text = match.group(1)
                                actual_data[cols[i]] = inner_text + " "
                            else:
                                actual_data[cols[i]] = ""
                        else:
                            actual_data[cols[i]] = row_data[i] + " "

                    actual_data["area"] = area
                    headers = list(actual_data.keys())
                    if len(headers) > 2:
                        row = [str(actual_data[header]).replace(',',' ').replace('"','') for header in headers]
                        with open('all_states.csv', 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow(row)



def combine_areas():
    df = pd.read_csv('all_states.csv', delimiter=",")
    df = df.groupby(["view","firm_name","person","title","address_line_1","address_line_2","city","state","zip","capabilities","email","website"])['area'].agg(' '.join).reset_index()
    zips = pd.read_csv("zip_code_database.csv", dtype=str, encoding='utf-8')
    df["plusfour"] = df["zip"].str.split("-").str[1]
    df["zip"] = df["zip"].str.split("-").str[0]
    df["full_zip"] = df["zip"] + "-" + df["plusfour"]
    zip_map = {}
    for _, row in zips.iterrows():
        zip_map[str(row.iloc[0]).replace(" ","")] = str(row.iloc[3]) 
    df['actual_city'] = df['zip'].apply(lambda z: zip_map.get(str(z), 'misc'))
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    conn = sqlite3.connect('sbdata.db')  
    table_name = 'sba'  
    df.to_sql(table_name, conn, if_exists='replace', index=False)

