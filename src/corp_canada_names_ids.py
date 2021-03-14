import pandas as pd
import requests
import pandas_read_xml as pdx
import zipfile
import glob

# import data from federal
url = "http://www.ic.gc.ca/app/scr/cc/CorporationsCanada/download/OPEN_DATA_SPLIT.zip"
save_folder = "data/raw"
save_path = save_folder + "/federal_data.zip"

r = requests.get(url, stream=True)
with open(save_path, "wb") as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

# unzip folder
zip = zipfile.ZipFile(save_path)
zip.extractall(save_folder)

# import list of xml files
xml_files = []
for name in glob.glob(save_folder + "/OPEN_DATA_*.xml"):
    xml_files.append(name)

# create df of corporate names and ids and write to .csv
df_names_ids = pd.DataFrame(columns=["corp_id", "corp_name"])
for file in xml_files:
    corp_canada_df = pdx.read_xml(file, ["cc:corpcan", "corporations"], encoding="utf8")
    corp_id = []
    corp_name = []
    for i in range(corp_canada_df.size):
        if "names" in corp_canada_df["corporation"][i].keys():
            names_list = corp_canada_df["corporation"][i]["names"]["name"]
            if isinstance(names_list, list):
                for j in range(len(names_list)):
                    if "#text" in names_list[j].keys():
                        corp_name.append(names_list[j]["#text"])
                        corp_id.append(
                            corp_canada_df["corporation"][i]["@corporationId"]
                        )
            else:
                corp_name.append(names_list["#text"])
                corp_id.append(corp_canada_df["corporation"][i]["@corporationId"])
        else:
            corp_name.append(None)
            corp_id.append(corp_canada_df["corporation"][i]["@corporationId"])

    df_file = pd.DataFrame({"corp_id": corp_id, "corp_name": corp_name})
    df_names_ids = df_names_ids.append(df_file, ignore_index=True)
df_names_ids.write_to("data/processed/corp_canada_names_ids.csv")

# create df of corporate addresses and ids and write to .csv
df_address_ids = pd.DataFrame(columns=["corp_id", "address"])
for file in file_list:
    corp_canada_df = pdx.read_xml(
        f"data/{file}", ["cc:corpcan", "corporations"], encoding="utf8"
    )
    corp_id = []
    address = []
    for i in range(corp_canada_df.size):
        if "addresses" in corp_canada_df["corporation"][i].keys():
            address_list = corp_canada_df["corporation"][i]["addresses"]["address"]
            if isinstance(address_list, list):
                for j in range(len(address_list)):
                    if "addressLine" in address_list[j].keys():
                        if address_list[j]["addressLine"] is None:
                            addressLine = "No address"
                        else:
                            if isinstance(address_list[j]["addressLine"], list):
                                addressLine = ", ".join(
                                    filter(None, address_list[j]["addressLine"])
                                )
                            else:
                                addressLine = address_list[j]["addressLine"]
                    else:
                        addressLine = "No address"
                    if "city" in address_list[j].keys():
                        if address_list[j]["city"] is None:
                            city = "No city"
                        else:
                            city = address_list[j]["city"]
                    else:
                        city = "No city"
                    if "postalCode" in address_list[j].keys():
                        postalcode = address_list[j]["postalCode"]
                    else:
                        postalcode = "No postal code"
                    if "province" in address_list[j].keys():
                        province = address_list[j]["province"]["@code"]
                    else:
                        province = "No province"
                    indv_address = [
                        addressLine,
                        city,
                        province,
                        postalcode,
                        address_list[j]["country"]["@code"],
                    ]
                    indv_address = ", ".join(indv_address)
                    address.append(indv_address)
                    corp_id.append(corp_canada_df["corporation"][i]["@corporationId"])
            else:
                if "addressLine" in address_list.keys():
                    if address_list["addressLine"] is None:
                        addressLine = "No address"
                    else:
                        if isinstance(address_list["addressLine"], list):
                            addressLine = ", ".join(
                                filter(None, address_list["addressLine"])
                            )
                        else:
                            addressLine = address_list["addressLine"]
                else:
                    addressLine = "Blank"
                if "city" in address_list.keys():
                    if address_list["city"] is None:
                        city = "No city"
                    else:
                        city = address_list["city"]
                else:
                    city = "No city"
                if "postalCode" in address_list.keys():
                    postalcode = address_list["postalCode"]
                else:
                    postalcode = "No postal code"
                if "province" in address_list.keys():
                    province = address_list["province"]["@code"]
                else:
                    province = "No province"
                indv_address = [
                    addressLine,
                    city,
                    province,
                    postalcode,
                    address_list["country"]["@code"],
                ]
                indv_address = ", ".join(indv_address)
                address.append(indv_address)
                corp_id.append(corp_canada_df["corporation"][i]["@corporationId"])
        else:
            address.append(None)
            corp_id.append(corp_canada_df["corporation"][i]["@corporationId"])

    df_file = pd.DataFrame({"corp_id": corp_id, "address": address})
    df_address_ids = df_address_ids.append(df_file, ignore_index=True)
