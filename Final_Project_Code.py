"""
Name: Ashley Tavano
CS230: Section 4
Data: Fast Food Restaurants in the USA
URL:
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium as fo
import pydeck as pdk
import seaborn as sns
from click import option
from pandas import options
from enum import unique

### ANY AI CODE IS HIGHLIGHTED BY ###

#Data Frame used : Fast Food Restaurants in the USA
try:
    dataFrame = pd.read_csv("C:\\Users\\ashle\\OneDrive\\Desktop\\fast_food_usa.csv")
except FileNotFoundError:
    st.error("File not found, please check the file path")
#[PY3] try/error checking

#Drop unnecessary columns  [DA7]
columns_to_drop = ["id", 'sourceURLs']
missing_columns = [col for col in columns_to_drop if col not in dataFrame.columns] #[PY4] List Comprehension
if not missing_columns:   #[DA4] Filter by one condition
    dataFrame = dataFrame.drop(columns = columns_to_drop)
else:
    st.warning(f"The following columns were not found and could not be dropped: {missing_columns} ")


#Reorganize Restaurant categories for later use:
restaurant_categories = {
        "American": [
            "American / Hamburgers / Fast Food",
            "American Restaurant and Fast Food Restaurant",
            "American Restaurant and Fast Food Restaurant Broadmoor-Sherwood",
            "American Restaurant, Burger Joint, and Fast Food Restaurant",
            "American Restaurant, Fast Food Restaurant, and Breakfast Spot",
            "American Restaurant, Fast Food Restaurant, and Breakfast Spot Bevo Mill",
            "American Restaurant, Fast Food Restaurant, and Breakfast Spot Downtown Indianapolis",
            "American Diner and Fast Food",
            "American Grill and Fast Food Restaurant",
            "Southern American Comfort Food and Fast Food"
        ],
        "Asian": [
            "Asian Restaurant, Chinese Restaurant, and Fast Food Restaurant",
            "Asian Restaurant, Fast Food Restaurant, and Chinese Restaurant",
            "Asian Restaurant, Fast Food Restaurant, and Chinese Restaurant Anderson Arbor",
            "Southeast Asian and Fast Food",
            "Japanese Sushi Bar and Fast Food",
            "Korean BBQ and Fast Food"
        ],
        "Bakery": [
            "Bakeries / Desserts / Fast Food",
            "Bakery & Pastries / American / Fast Food",
            "Bakery, Restaurant, and Fast Food Restaurant",
            "Bakery and Café with Fast Food Options",
            "Gourmet Bakery and Fast Food Spot"
        ],
        "Burger Joint": [
            "Burger Joint and Fast Food Restaurant",
            "Burger Joint and Fast Food Restaurant Brooklyn - Centre",
            "Burger Joint and Fast Food Restaurant Central City South",
            "Gourmet Burgers and Fast Food",
            "Classic Diner Burgers and Fast Food"
        ],
        "Fast Food": [
            "Fast Food",
            "Fast Food / Sandwiches / Wraps",
            "Fast Food Restaurant",
            "Fast Food Restaurant Atascocita South",
            "Quick Bites and Fast Food",
            "Family-Friendly Fast Food Spot"
        ],
        "Mexican": [
            "Mexican / Fast Food",
            "Mexican Restaurant and Fast Food Restaurant",
            "Mexican Restaurant and Fast Food Restaurant Northwest Torrance",
            "Authentic Mexican Tacos and Fast Food",
            "Tex-Mex and Fast Food Combo"
        ],
        "Pizza": [
            "Pizza / Fast Food / American",
            "Pizza Place and Fast Food Restaurant",
            "Pizza Place, Fast Food Restaurant, and Italian Restaurant",
            "Pizza Place, Fast Food Restaurant, and Italian Restaurant Preston Park",
            "Brick Oven Pizza and Fast Food",
            "Custom Pizza and Fast Food Bar"
        ],
        "Sandwich": [
            "Sandwich Place and Fast Food Restaurant",
            "Sandwich Place and Fast Food Restaurant Allegheny West",
            "Sandwich Place and Fast Food Restaurant Belltown",
            "Gourmet Sandwich Shop and Fast Food",
            "Classic Sub Shop and Fast Food"
        ],
        "Seafood": [
            "Seafood / American / Fast Food",
            "Fish Chips Shop and Fast Food Restaurant",
            "Fast Food Restaurant and Seafood Restaurant",
            "Lobster Rolls and Fast Food",
            "Fresh Catch Seafood and Fast Food"
        ],
        "Taco": [
            "Taco Place and Fast Food Restaurant",
            "Taco Place, Fast Food Restaurant, and Mexican Restaurant",
            "Taco Place, Fast Food Restaurant, and Mexican Restaurant Valley Station",
            "Street Tacos and Fast Food",
            "Modern Taco Bar and Fast Food"
        ]
    }

#Section 1: Page Introduction and Design materials

st.set_page_config(page_title= "Exploring Fast Food in the U.S.", layout = "wide")  #[ST4] page configuration to set title and layout
###Code based on ChatGPT. See Section 1 of accompanying document

#Design   [ST4]
st.markdown(
    """
<style>
.reportview-container .markdown-text-container {
    font-family: monospace;
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}
.Widget>label {
    color: white;
    font-family: monospace;
}
[class^="st-b"]  {
    color: white;
    font-family: monospace;
}
.st-bb {
    background-color: transparent;
}
.st-at {
    background-color: #0c0080;
}
footer {
    font-family: monospace;
}
.reportview-container .main footer, .reportview-container .main footer a {
    color: #0c0080;
}
header .decoration {
    background-image: none;
}

</style>
""",
    unsafe_allow_html=True,
)
###See section 1 of accompanying document

st.title("🍔 Exploring Fast Food in the U.S.")
st.subheader("Explore data on 10,000 fast-food restaurants across the country.")

st.image("C:\\Users\\ashle\\OneDrive - Bentley University\\Attachments\\Fast_food_Image.jpg", width=500)  #[ST4] image
"\n"

#Section 2: Dataset Overview
st.header("\n📊 Dataset Overview")
'''
This dataset contains information about 10,000 fast-food restaurants across the U.S. 
Below, you can view the entire dataset or search for specific entries.
'''
st.dataframe(dataFrame, use_container_width=True)

st.header("📈 Summary Statistics")

total_restaurants = len(dataFrame)
unique_categories = dataFrame["categories"].nunique()
unique_cities = dataFrame['city'].nunique()

dataFrame["dateAdded"] = pd.to_datetime(dataFrame["dateAdded"])
date_range = (dataFrame["dateAdded"].min(), dataFrame["dateAdded"].max())
formatted_date_range = (
    date_range[0].strftime("%B %d, %Y"),
    date_range[1].strftime("%B %d, %Y")
)
###Code based on ChatGPT. See Section 2 of accompanying document


st.markdown(f"""
Total Restaurants: {total_restaurants}
\nUnique Categories: {unique_categories}
\nUnique Cities: {unique_cities}
\nDate Range: {formatted_date_range[0]} to {formatted_date_range[1]}
""")
"\n"


#Section 3: Data Insight and Analysis through Maps and Graphs
#Button
if "show_section" not in st.session_state:    #[DA4] Filter by one condition
    st.session_state.show_section = False


if st.button("Click Here for More Data Insights!"): #[ST2] st.button
    st.session_state.show_section = not st.session_state.show_section

###Some Code for button based on code from ChatGPT. See section 3 of document

if st.session_state.show_section:
    st.subheader("Interactive Data Insights")

    # Map Display - Geographic Visualization    [MAP] Two maps displayed here: basic and heat maps for users choice
    st.subheader("View this data across the U.S.")
    map_choice = st.radio("Choose Map Type", ("Basic Map", "Heatmap"))  #[ST3] st.radio
    if map_choice == "Basic Map":   #[DA4] Filter by one condition
        st.map(dataFrame[['latitude', 'longitude']])

    elif map_choice == "Heatmap":
        heatmap = pdk.Deck(
            layers=[
                pdk.Layer(
                    "HeatmapLayer",
                    dataFrame[['latitude', 'longitude']],
                    get_position='[longitude, latitude]',
                    get_weight=1,
                    radius=80,
                    opacity=0.7
                )
            ],
            initial_view_state=pdk.ViewState(
                latitude=dataFrame['latitude'].mean(),
                longitude=dataFrame['longitude'].mean(),
                zoom=4,
                pitch=0
            ),
            map_style='mapbox://styles/mapbox/light-v9',
        )
        st.pydeck_chart(heatmap)
    "\n"

    #Data Insights through Graphs and Questions
    st.subheader("Visualize Data")
    chart_type = st.slider(    #[ST3] Additional streamlit widget
        "Select Chart Type",
        min_value = 1,
        max_value = 3,
        value=1,
        step=1
    )

    #1: [VIZ1] Bar Chart (Top cities with Most Restaurants)
    if chart_type == 1:
        st.write("Top Cities with the Most Restaurants")
        top_cities = dataFrame['city'].value_counts().head(10)  # [DA3] Find top 10 cities
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_cities.index, y=top_cities.values,
                    ax=ax)
        ax.set_title("Top 10 Cities with the Most Restaurants")
        ax.set_xlabel("City")
        ax.set_ylabel("Number of Restaurants")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig)

    #2:[VIZ2] Pie Chart (Distribution of Restaurant Categories)
    if chart_type == 2:
        st.write("Pie Chart: Distribution of Restaurant Categories")
        filtered_categories = {key: val for key, val in restaurant_categories.items() if key != 'Fast Food'}
        category_counts = {key: 0 for key in filtered_categories.keys()}
        for category in dataFrame['categories']:
            for key, subcategories in filtered_categories.items():
                if category in subcategories:
                    category_counts[key] += 1
                    break
        category_labels = list(category_counts.keys())
        category_sizes = list(category_counts.values())
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(category_sizes, labels=category_labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title("Distribution of Restaurant Categories")
        st.pyplot(fig)
###Code for pie chart based on code from ChatGPT. See Section 3 of accompanying document


    #3: [VIZ3] Line Chart (Restaurants Added Over Time)
    elif chart_type == 3:
        st.write("Number of Restaurants Added Over Time")
        restaurant_per_month = dataFrame.groupby(dataFrame['dateAdded'].dt.to_period('M')).size()
        fig, ax = plt.subplots(figsize = (10,6))
        restaurant_per_month.plot(kind = 'line', ax=ax, color='blue')
        ax.set_title("Number of Restaurants Added Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Restaurants")
        st.pyplot(fig)



    #Interactive Question:
    st.subheader("Which State has the Most ______?")

    #Select a type of restaurant:
    selected_category = st.selectbox("Select a Category:", list(restaurant_categories.keys()))  #[PY1] (restaurant_categories.keys()) is the parameter)
    #Select a state:
    province = st.selectbox("Select a State:", dataFrame['province'].unique()) #[PY1] Called a second time with a new parameter ('province')
#[ST1] st.selectbox

    if selected_category and province:
        filtered_data = dataFrame[    # [PY2] filtered_data returns more than one value based on the conditions
            (dataFrame['categories'].isin(restaurant_categories[selected_category])) & (dataFrame['province'] == province)
            #[DA5] Filter data with "and", "&"
        ]

        st.subheader(f"There are {len(filtered_data)} {selected_category} restaurants in {province}.")
        if st.button("Click here for locations!"):
            st.write("Restaurants:")
            st.dataframe(filtered_data[["name", 'address', 'city']])
            map_center = [filtered_data['latitude'].mean(), filtered_data['longitude'].mean()]
            m = fo.Map(location = map_center , zoom_start=8)

            for _, row in filtered_data.iterrows(): #[DA8] iterrows
                fo.Marker(
                    location = [row['latitude'], row['longitude']],
                    popup= f"{row['name']}<br>{row['address']}<br>{row['city']}",
                    tooltip=row['name'],
                ).add_to(m)
            st.components.v1.html(m._repr_html_(), height = 250)




#Section 4: Interactive Display of Restaurant locations
st.header("Find Food Restaurants in the U.S.")

restaurant_options = sorted(dataFrame["name"].unique())   #[DA2]
selected_restaurant = st.selectbox("Select a restaurant", options = restaurant_options)
filtered_dataFrame = dataFrame[dataFrame['name'] == selected_restaurant]

state_options = sorted(filtered_dataFrame['province'].unique())   #[DA2]
selected_state = st.selectbox("Select a State", options = state_options)
filtered_dataFrame = filtered_dataFrame[filtered_dataFrame['province']== selected_state]

city_options = sorted(filtered_dataFrame['city'].unique())   #[DA2]
selected_city = st.selectbox("Select a City", options= city_options)
filtered_dataFrame = filtered_dataFrame[filtered_dataFrame['city']== selected_city]

st.write(f"Showing Details for {selected_restaurant} in {selected_city}, {selected_state}: ")
st.write(filtered_dataFrame[["address", "websites"]])

#Create a map using folium:
lat = filtered_dataFrame['latitude'].iloc[0]
lon = filtered_dataFrame['longitude'].iloc[0]

m = fo.Map(location =[lat,lon],zoom_start = 10)  #[MAP] using folium
for _, row in filtered_dataFrame.iterrows():   #[DA8] iterrows()
    fo.Marker(
        location = [row['latitude'], row['longitude']],
        popup=f"{row['name']}<br>{row['address']}",
        tooltip=row["name"],
    ).add_to(m)
st.components.v1.html(m._repr_html_(), height = 500)

### Code for Map based on code from ChatGPT. See Section 4 of accompanying document


