import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

# Generate some random data
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

# Create a figure and an imshow plot
fig, ax = plt.subplots()
ax.set_facecolor("black")
im = ax.imshow(data, cmap="viridis_r", vmin=3.0, vmax=7.0)

# Display the figure on the app using pyplot function
st.pyplot(fig)

# Create four slider widgets for selecting an area on the plot
x1 = sidebar.slider("Select x1", 0, data.shape[1]-1)
y1 = sidebar.slider("Select y1", 0, data.shape[0]-1)
x2 = sidebar.slider("Select x2", 0, data.shape[1]-1)
y2 = sidebar.slider("Select y2", 0, data.shape[0]-1)

# Draw a red rectangle on the plot using the slider values
rect = plt.Rectangle((x1,y1), x2-x1, y2-y1,
                     facecolor='none',
                     edgecolor='black',
                     linewidth=2,
                     alpha=0.5)
ax.add_patch(rect)

# Display the updated figure on the app using pyplot function
st.pyplot(fig)

# Call the onselect_function with the slider values and get the mean and std dev of the selected area
mean, std = onselect_function(x1,y1,x2,y2)

# Display the mean and std dev on the app
st.write(f"Mean: {mean:.2f}")
st.write(f"Standard deviation: {std:.2f}")
