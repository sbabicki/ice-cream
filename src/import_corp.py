import pandas as pd
import requests
import pandas_read_xml as pdx
import zipfile
import glob

save_folder = "../data/raw/federal"
save_path = save_folder+"/federal_data.zip"

def download_data():

    # import data from federal
    url ="http://www.ic.gc.ca/app/scr/cc/CorporationsCanada/download/OPEN_DATA_SPLIT.zip"

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
    #xml_files.append(pdx.read_xml(name,  ["cc:corpcan", "corporations"], encoding="utf8"))# import data from federal
    xml_files.append(name)
    
# create df of corporate names and ids and write to .csv
df_names_ids = pd.DataFrame(columns=["corp_id", "businessNumber"])
for file in xml_files:
    print(file)
    corp_canada_df = pdx.read_xml(file, ["cc:corpcan", "corporations"], encoding="utf8")
    corp_id = []
    businessNumber = []
    for i in range(corp_canada_df.size):
        #if "businessNumbers" in corp_canada_df["corporation"][i].keys():
        try:
            bn = corp_canada_df["corporation"][i]["businessNumbers"]["businessNumber"]
            businessNumber.append(bn)
            corp_id.append(corp_canada_df["corporation"][i]["@corporationId"])
        except:
            businessNumber.append(None)
            corp_id.append(corp_canada_df["corporation"][i]["@corporationId"])

    df_file = pd.DataFrame({"corp_id": corp_id, "businessNumber": businessNumber})
    df_names_ids = df_names_ids.append(df_file, ignore_index=True)
df_names_ids.to_csv("corp_canada_names_bn.csv")
