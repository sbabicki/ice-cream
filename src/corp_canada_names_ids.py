import pandas as pd
import requests
import pandas_read_xml as pdx
import zipfile
import glob

# import data from federal
url ="http://www.ic.gc.ca/app/scr/cc/CorporationsCanada/download/OPEN_DATA_SPLIT.zip"
save_folder = "data/raw"
save_path = save_folder+"/federal_data.zip"

r = requests.get(url, stream=True)
with open(save_path, "wb") as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

# unzip folder
zip = zipfile.ZipFile(save_path)
zip.extractall(save_folder)

# import list of xml files
xml_files = []
for name in glob.glob(save_folder+"/OPEN_DATA_*.xml"):
    xml_files.append(name)

df_names_ids = pd.DataFrame(columns = ["corp_id", "corp_name"])
for file in xml_files:
    corp_canada_df = pdx.read_xml(file,  ["cc:corpcan", "corporations"], encoding='utf8')
    corp_id = []
    corp_name = []
    for i in range(corp_canada_df.size):
        if "names" in corp_canada_df["corporation"][i].keys():
            names_list = corp_canada_df["corporation"][i]['names']['name']
            if isinstance(names_list, list):
                for j in range(len(names_list)):
                    if "#text" in names_list[j].keys():
                        corp_name.append(names_list[j]['#text'])
                        corp_id.append(corp_canada_df["corporation"][i]['@corporationId'])
            else:
                corp_name.append(names_list['#text'])
                corp_id.append(corp_canada_df["corporation"][i]['@corporationId'])
        else: 
            corp_name.append(None)
            corp_id.append(corp_canada_df["corporation"][i]['@corporationId'])
        
    df_file = pd.DataFrame({"corp_id": corp_id, "corp_name": corp_name})
    df_names_ids = df_names_ids.append(df_file, ignore_index=True)