from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome("./chromedriver")

def corp_canada_directors(corp_name, corp_id):
    driver.get("https://www.ic.gc.ca/app/scr/cc/CorporationsCanada/fdrlCrpSrch.html")
    search = driver.find_element_by_id("corpNumber")
    search.clear()
    search.send_keys(corp_id)
    search.send_keys(Keys.RETURN)
    driver.find_element_by_partial_link_text(corp_name).click()
    address_elems = driver.find_elements_by_class_name("list-inline-block")

    names = []
    address = []
    for i in range(len(address_elems)):
        full_text = address_elems[i].text
        split_text = full_text.split("\n", 1)
        split_text = [w.replace('\n', ', ') for w in split_text]
        names.append(split_text[0])
        address.append(split_text[1])
    df_company = pd.DataFrame({"corp_name": [corp_name]*num_directors, "corp_id": [corp_id]*num_directors, "director_name": names, "address": address})
    return df_company
