import pandas as pd

#need to get each line, strip shit, based on line number offset assign column to it

df = pd.read_excel("state_of_cali_certs.xls") 

print(df.columns)