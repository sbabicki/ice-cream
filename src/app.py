import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
from requests.utils import quote
import fuzzy_blacklist

@st.cache
def get_data(address=None, biz_name=None):
    
    df = pd.read_csv('./data/processed/business-licences-hackathon.csv', low_memory=False)
    #df = orig_df
    # for testing
    #df = df.iloc[0:1]
    #return df
    
    if address and biz_name:
        address = address.lower()
        biz_name = biz_name.lower()
        df = df.query('BusinessName.str.lower() == @biz_name & Address.str.lower() == @address')
    elif address:
        address = address.lower()
        df = df.query('Address.str.lower() == @address')
    elif biz_name:
        biz_name = biz_name.lower()
        df = df.query('BusinessName.str.lower() == @biz_name')
    else:
        print('Please enter in an address or business name.')
    
    if df.empty:
        df = df.append(pd.Series(), ignore_index = True)
        if biz_name:
            df["BusinessName"] = biz_name
        if address:
            df["Address"] = address
    df.fillna("Unknown", inplace=True)   
    return df.reset_index(drop=True)

def load_company_page(df):
    company = df.iloc[0, :]
    business_name = company["BusinessName"] 
    business_address = company["Address"]
    phone = "Unknown"
    num_employees = str(company["NumberofEmployees"]).replace(".0", "")
    num_years_active = "Unknown"
    director_names = "Unknown"
    
    st.header("Results for "+business_name)
    col1, col2 = st.beta_columns(2)
    
    col1.subheader("Company Information")
    col1.markdown(f"Name: **{business_name}**")
    col1.markdown(f"Address: **{business_address}**")
    col1.markdown(f"Phone: **{phone}**")
    col1.markdown(f"Number of employees: **{num_employees}**")
    col1.markdown(f"Estimated years active: **{num_years_active}**")
    col1.markdown(f"Director names: **{director_names}**")

    col1.subheader('Search Links')
    for kind, searchTerm in {"name" : business_name, "address" : business_address}.items():
        if searchTerm != "Unknown":
            query = quote(searchTerm)
            html = "<a href='{url}{query}' target='_blank'><img src='{logo}' width='30' style='padding:5px'>{text} for <b>{searchTerm}</b></a>"
            google_logo = "https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA"
            facebook_logo = "https://facebookbrand.com/wp-content/uploads/2019/04/f_logo_RGB-Hex-Blue_512.png?w=30&h=30"
            linkedin_logo = "https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg"
            google_exact = html.format(query = f'"{query}"', logo = google_logo, searchTerm = searchTerm, text="Exact match", url ="https://google.com/search?q=")
            google_partial = html.format(query = query, logo = google_logo, searchTerm = searchTerm, text="Partial match", url = "https://google.com/search?q=")
            facebook = html.format(query = query, logo = facebook_logo, searchTerm = searchTerm, text="Search", url = "https://facebook.com/search/places/?q=")
            linkedin = html.format(query = query, logo = linkedin_logo, searchTerm = searchTerm, text="Search", url = "https://linkedin.com/search/results/all/?keywords=")
            col1.markdown(google_exact,  unsafe_allow_html=True)
            col1.markdown(google_partial,  unsafe_allow_html=True)
            col1.markdown(facebook,  unsafe_allow_html=True)
            if kind == "name":
                col1.markdown(linkedin,  unsafe_allow_html=True)

    col1.subheader('Other Matching Results')
    col1.write(df.iloc[1:])
    
    def message(blacklist_db, search):
        found_text = "<span style='color:red;'>RED FLAG - probable match found for {search}</span>".format(search=search)
        not_found_text = "<span style='color:green;'>No red flag found for {search}</span>".format(search=search)
        return found_text if any(blacklist_db['scores'] > 80) else not_found_text
        
    col2.subheader("Offshore Leaks Database Check")
    if business_address != "Unknown":
        blacklist_db = fuzzy_blacklist.offshore_leaks_search_address(business_address)
        col2.markdown(message(blacklist_db, business_address), unsafe_allow_html=True)
        col2.write(blacklist_db)
        
    if business_name != "Unknown":
        blacklist_db = fuzzy_blacklist.offshore_leaks_search_entity(business_name)
        col2.markdown(message(blacklist_db, business_name), unsafe_allow_html=True)
        col2.write(blacklist_db)
        
        blacklist_db = fuzzy_blacklist.canlii_search_entity(business_name)
        col2.subheader("CanLii Legal Check")
        col2.markdown(message(blacklist_db, business_name), unsafe_allow_html=True)
        col2.write(blacklist_db)
    
    col2.subheader("Fraud Check")
    col2.markdown("No fraud detected")
    
    if business_address != "Unknown":
        st.subheader(f"Google maps search by address ({business_address})")
        address_map = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBYB6IAnJXwc6X8Yr1WR0hMcarcUNgEVQM&q="+quote(business_address)
        components.iframe(address_map)
    if business_name != "Unknown":
        st.subheader(f"Google maps search by business name ({business_name})")
        business_map = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBYB6IAnJXwc6X8Yr1WR0hMcarcUNgEVQM&q="+quote(business_name)
        components.iframe(business_map)
    
    with st.beta_expander('View Source Data'):
        st.write((df))
    
def main():
    
    #try:
    st.sidebar.text("Enter an address, business name, \n or both!")
    search_address = st.sidebar.text_input("Enter an address")
    search_biz_name = st.sidebar.text_input("Enter a business name")
    
    if st.sidebar.button('Search'):
        df = get_data(search_address, search_biz_name)
        load_company_page(df)

if __name__ == "__main__":
    main()