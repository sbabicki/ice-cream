import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
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
    search_address = st.sidebar.text_input("Enter an address")
    search_biz_name = st.sidebar.text_input("Enter a business name")
    
    if st.sidebar.button('Search'):
        df = get_data(search_address, search_biz_name)
        
        company = df.iloc[0]
        business_name = company["BusinessName"]
        business_address = company["Street"]
        phone = "Unknown"
        num_employees = company["NumberofEmployees"]
        num_years_active = "Unknown"
        director_names = "Unknown"
        
        st.header("Results for "+business_name)
        col1, col2 = st.beta_columns(2)
        
        col1.subheader("Company Information")
        col1.markdown(f"Name: **{business_name}**")
        col1.markdown(f"Address: **{business_address}**")
        col1.markdown(f"Phone: **{phone}**")
        col1.markdown("Number of employees: **{:.0f}**".format(num_employees))
        col1.markdown(f"Estimated years active: **{num_years_active}**")
        col1.markdown(f"Director names: **{director_names}**")

        col1.subheader('Links')
        for searchTerm in [business_address, business_address]:
            if(searchTerm):
                from requests.utils import quote
                searchTerm = quote(searchTerm)
                col1.markdown("<a href='https://google.com/search?q=\""+searchTerm+"\"' target='_blank'>Google exact match search</a>",  unsafe_allow_html=True)
                col1.markdown("<a href='https://google.com/search?q=\""+searchTerm+"\"' target='_blank'>Google partial search</a>",  unsafe_allow_html=True)
                col1.markdown("<a href='https://facebook.com/search/people/?q="+searchTerm+"' target='_blank'>Facebook search</a>",  unsafe_allow_html=True)

        col2.subheader('Other Results')
        col2.write(df.iloc[1:])
        
        col2.subheader("Offshore Leaks Database Check")
        # offshore_message, offshore_df, canlii_message, canlii_df
        if(business_address):
            pass
            #col2.write(offshore_leaks_search_address(address))
        if(business_name):
            pass
            #col2.write(offshore_leaks_search_entity(biz_name))
            col2.subheader("CanLii Legal Check")
            #col2.write(canlii_search_entity(biz_name))
        
        col2.subheader("Fraud Check")
        col2.markdown("No fraud detected")
        
        if business_address:
            st.subheader(f"Google maps search by address ({business_address})")
            address_map = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBYB6IAnJXwc6X8Yr1WR0hMcarcUNgEVQM&q="+quote(business_address)
            components.iframe(address_map)
        if business_name:
            st.subheader(f"Google maps search by business name ({business_name})")
            business_map = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBYB6IAnJXwc6X8Yr1WR0hMcarcUNgEVQM&q="+quote(business_name)
            components.iframe(business_map)
        
        with st.beta_expander('View Source Data'):
            st.write((df))

if __name__ == "__main__":
    main()