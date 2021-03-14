import streamlit as st
import pandas as pd
import altair as alt
#import canlii

@st.cache
def get_data(address=None, biz_name=None):
    
    df = pd.read_csv('./data/processed/business-licences-hackathon.csv', sep = ';', low_memory=False)
    
    # for testing
    df = df.iloc[0:1]
    return df
    
    if (address) and (biz_name):
        #NEED TO CHANGE STREET TO ADDRESS
        #ONlY DISPLAY LATEST FOLDER YEAR
        df = df.query('BusinessName == @biz_name & Street == @address')
        return df.set_index("BusinessName")
    elif address:
        print(address)
        df = df.query('Street == @address')
        return df.set_index("Street")
    elif biz_name:
        #df.query()
        #print(biz_name)
        df = df.query('BusinessName == @biz_name')
        return df.set_index("BusinessName")
    else:
        print('Please enter in an address or business name.')

def main():
    #try:
    st.sidebar.text("Enter an address, business name, \n or both!")
    address = st.sidebar.text_input("Enter an address")
    biz_name = st.sidebar.text_input("Enter a business name")
    
    if st.sidebar.button('Search'):
        df = get_data(address, biz_name)
        
        company = df.iloc[0]
        business_name = company["BusinessName"]
        address = company["Street"]
        phone = "Unknown"
        num_employees = company["NumberofEmployees"]
        num_years_active = "Unknown"
        director_names = "Unknown"
        
        st.header("Results for "+business_name)
        col1, col2 = st.beta_columns(2)
        
        col1.subheader("Company Information")
        col1.markdown(f"Name: **{business_name}**")
        col1.markdown(f"Address: **{address}**")
        col1.markdown(f"Phone: **{phone}**")
        col1.markdown("Number of employees: **{:.0f}**".format(num_employees))
        col1.markdown(f"Estimated years active: **{num_years_active}**")
        col1.markdown(f"Director names: **{director_names}**")

        col1.subheader('Links')
        for searchTerm in [address, biz_name]:
            if(searchTerm):
                from requests.utils import quote
                searchTerm = quote(searchTerm)
                col1.markdown("<a href='https://google.com/search?q=\""+searchTerm+"\"' target='_blank'>Google exact match search</a>",  unsafe_allow_html=True)
                col1.markdown("<a href='https://google.com/search?q=\""+searchTerm+"\"' target='_blank'>Google partial search</a>",  unsafe_allow_html=True)
                col1.markdown("<a href='https://facebook.com/search/people/?q="+searchTerm+"' target='_blank'>Facebook search</a>",  unsafe_allow_html=True)
        
        col2.subheader("Streetview")
        col2.markdown("[ ]")

        col2.subheader('Other Results')
        col2.write(df.iloc[1:])
        
        col2.subheader("Offshore Leaks Database Check")
        # offshore_message, offshore_df, canlii_message, canlii_df
        if(address):
            pass
            #col2.write(offshore_leaks_search_address(address))
        if(biz_name):
            pass
            #col2.write(offshore_leaks_search_entity(biz_name))
            col2.subheader("CanLii Legal Check")
            #col2.write(canlii_search_entity(biz_name))
        
        col2.subheader("Fraud Check")
        col2.markdown("No fraud detected")
        
        with st.beta_expander('View Source Data'):
            st.write((df))

if __name__ == "__main__":
    main()