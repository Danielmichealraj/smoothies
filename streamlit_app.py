

# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title("Customise your:heart: smoothie :apple:")
st.write("""Choose the fruits you want in your customised smoothie""")



name_on_order = st.text_input('Name to be printed no Smoothie:')
st.write('Name printed will be:', name_on_order)
cnx = st.connection ("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data= my_dataframe, use_container_width=True)


ingrediants_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)

if ingrediants_list:
    ingrediants_string =' '
    for fruit_name in ingrediants_list:
        ingrediants_string += fruit_name + ' '
        st.subheader(fruit_name + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_name)
        fv_df= st.dataframe(data= fruityvice_response.json(), use_container_width = True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingrediants_string + """ ',' """ + name_on_order + """ ')"""
    order_confirm = st.button('Confirm Order')
   

    
    if order_confirm:
        session.sql(my_insert_stmt).collect()
        
        st.success('Order Placed Thank you')


