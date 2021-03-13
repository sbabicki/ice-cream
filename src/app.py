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
    df = pd.read_csv('business-licences-hackathon.csv', sep = ';', low_memory=False)


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
    print(st.sidebar)
    if st.sidebar.button('Search'):
        df = get_data(address, biz_name)
        st.write(df)
        #option = st.sidebar.selectbox(
        #'These are multiple return values',
        #('ALL VALUE1', 'ALL VALUE2', 'ALL VALUE3')
        #st.sidebar.write('You selected:', option)
    #print(df)



        # countries = st.multiselect(
        #     "Choose countries", list(df.index), ["China", "United States of America"]
        #
        # if not countries:
        #     st.error("Please select at least one country.")
        # else:
        #     data = df.loc[countries]
        #     data /= 1000000.0
        #     st.write("### Gross Agricultural Production ($B)", data.sort_index())

        #     data = data.T.reset_index()
        #     data = pd.melt(data, id_vars=["index"]).rename(
        #         columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        #     )
        #     chart = (
        #         alt.Chart(data)
        #         .mark_area(opacity=0.3)
        #         .encode(
        #             x="year:T",
        #             y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
        #             color="Region:N",
        #         )
        #     )
        #     st.altair_chart(chart, use_container_width=True)
    # except urllib.error.URLError as e:
    #     st.error(
    #         """
    #         **This demo requires internet access.**

    #         Connection error: %s
    #     """
    #         % e.reason
    #     )

if __name__ == "__main__":
    main()