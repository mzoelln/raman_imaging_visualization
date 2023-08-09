import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

# import fitted data
path_result_cal = '04_StPeterFragment1_532_1800_50x_100p_4x1s_image_LMFit_PsdVgt1070to1100_up200cal.csv'
data_results_cal = pd.read_csv(path_result_cal, sep=';', engine='python', header=0, index_col=(0))

ext_image = (281, 201)

# reshape FWHM values from csv
# FWHM values calcite
fwhm_cal = pd.DataFrame(np.nan, index = range(0, 56481), columns=['fwhm'])
xc_cal = pd.DataFrame(np.nan, index = range(0, 56481), columns=['xc'])
df_extract = data_results_cal.set_index('spectrum no.')
df_extract.index = df_extract.index.astype(int)

fwhm_cal['fwhm'] = df_extract['psdv1_fwhm']
image_fwhm_cal = pd.DataFrame(fwhm_cal.values.reshape(ext_image))

xc_cal['xc'] = df_extract['psdv1_center']
image_xc_cal = pd.DataFrame(xc_cal.values.reshape(ext_image))

# load data
data = image_fwhm_cal

# Define a function to calculate the mean and standard deviation of the selected area
@st.cache # Use cache decorator to avoid redundant computations
def onselect_function(x1, y1, x2, y2):
    # Get the coordinates of the selected area
    min_x = math.floor(min(x1, x2))
    min_y = math.floor(min(y1, y2))
    max_x = math.ceil(max(x1, x2))
    max_y = math.ceil(max(y1, y2))
    
    # Filter the data points that are inside the selected area
    mask = data.iloc[min_y:max_y+1, min_x:max_x+1]
    
    # Calculate the mean and standard deviation of the selected data
    mean = np.nanmean(mask.values)
    std = np.nanstd(mask.values)

    return mean, std

# Create a title for the app
st.title("Interactive Plot with Streamlit")

# Create a sidebar for the widgets
sidebar = st.sidebar

# Create a slider widget for selecting a value
x = sidebar.slider("Select a value", 0, 100)

# Display your image data on the app using image function
st.image(data, caption="Image data", use_column_width=True)

# Create a custom chart that allows you to draw rectangles on the image with your mouse
chart_data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["a", "b", "c"])

chart = st.draw_chart(chart_data)

# Get the data of the drawn rectangles from the chart object
rectangles = chart.selected_data

# Check if there are any rectangles drawn
if rectangles:
    # Loop through the rectangles
    for i, rectangle in enumerate(rectangles):
        # Get the coordinates of the rectangle
        x1, y1 = rectangle["geometry"]["coordinates"][0][0]
        x2, y2 = rectangle["geometry"]["coordinates"][0][2]

        # Call the onselect_function with the coordinates and get the mean and std dev of the selected area
        mean, std = onselect_function(x1, y1, x2, y2)

        # Display the mean and std dev on the app with the color of the rectangle
        st.write(f"Rectangle {i+1} ({COLORS[i]}): Mean: {mean:.2f}, Standard deviation: {std:.2f}")
