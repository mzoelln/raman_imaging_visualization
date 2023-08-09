import streamlit as st
import numpy as np
import pandas as pd
import math
import plotly.express as px
import plotly.graph_objects as go

pip install --upgrade

# import fitted data
path_result_cal = '04_StPeterFragment1_532_1800_50x_100p_4x1s_image_LMFit_PsdVgt1070to1100_up200cal.csv'
data_results_cal = pd.read_csv(path_result_cal, sep=';', engine='python', header=0, index_col=(0))

ext_image = (281, 201)

# reshape FWHM values from csv
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

# Create an imshow plot with Plotly
fig = px.imshow(data, color_continuous_scale="viridis_r", zmin=3.0, zmax=7.0)

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

# Define a callback function for the button click
def button_click(trace, points, state):
    # Get the coordinates of the corners of the rectangle
    x1 = points.xs[0]
    y1 = points.ys[0]
    x2 = points.xs[1]
    y2 = points.ys[1]
    
    # Call the onselect_function to calculate the mean and std of the selected area
    mean, std = onselect_function(x1, y1, x2, y2)
    
    # Display the results on the app using st.write
    st.write(f"The mean of the selected area is {mean:.2f}")
    st.write(f"The standard deviation of the selected area is {std:.2f}")

# Create a custom modebar button that allows you to draw a rectangle on the plot
button = dict(
            method="drawopenpath",
            args=[{"shape": {"type": "rect"}}],
            name="Draw Rectangle",
            icon={"width": 512,
                  "height": 512,
                  "path": "M512 256c0 141.385-114.615 256-256 256S0 397.385 0 256 114.615 0 256 0s256 114.615 256 256z m-77.154-128h-307.692c-14.769 0-26.769 12-26.769 26.769v230.462c0 14.769 12 26.769 26.769 26.769h307.692c14.769 0 26.769-12 26.769-26.769V154.769c0-14.769-12-26.769-26.769-26.769z"}
        )

# Add the custom modebar button to the figure config
config = dict(
        modeBarButtonsToAdd=[button]
)

# Add a callback function for the button click event
fig.data[0].on_click(button_click)

# Display the plot on the app using st.plotly_chart
st.plotly_chart(fig, use_container_width=True)

