import streamlit as st
import pandas as pd
import altair as alt

#def one_row(df):
   #df.filter('year')
   #return df.loc[0,:]

#Save all names in separate dataframe
#Filter and save all other variables (i.e. address) as list
#Also need federal vs. provincial button

@st.cache
def get_data(address=None, biz_name=None):
    #AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    #df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    #global df
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
        
        st.header("Company")
        col1, col2 = st.beta_columns(2)
        
        company = df.iloc[0]
        business_name = company["BusinessName"]
        address = company["Street"]
        phone = "Unknown"
        num_employees = company["NumberofEmployees"]
        num_years_active = "Unknown"
        director_names = "Unknown"
        
        col1.subheader("Company Information")
        col1.markdown(f"Name: **{business_name}**")
        col1.markdown(f"Address: **{address}**")
        col1.markdown(f"Phone: **{phone}**")
        col1.markdown("Number of employees: **{:.0f}**".format(num_employees))
        col1.markdown(f"Estimated years active: **{num_years_active}**")
        col1.markdown(f"Director names: **{director_names}**")

        col1.subheader('Other Results')
        col1.write(df)
        
        col1.subheader('Links')
        col1.write(df)
        
        col2.subheader("Streetview")
        col2.markdown("[ ]")
        
        col2.subheader("Related Results")
        col2.write(df)
        
        col2.subheader("Legal Check")
        col2.markdown("No fraud detected")
        
        col2.subheader("Fraud Check")
        col2.markdown("No fraud detected")
        
        with st.beta_expander('View Source Data'):
            st.write((df))


if __name__ == "__main__":
    main()