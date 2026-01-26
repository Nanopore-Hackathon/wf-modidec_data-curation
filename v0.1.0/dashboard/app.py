

############################################
# description
# last edited: 2023-09-28
# by Johannes Rolshausen
# johannes.rolshausen@gmail.com

# call this script with the following arguments:
# -i <input_directory> -o <output_directory> -s <start_index> -e <end_index>

# example call:
# streamlit run app.py -- -i exampledirInput -o examplediroutput -s 0 -e 4   





import time
import os
import sys
import argparse
#from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import pathlib


############################################
# Initialisation

## page configuration
st.set_page_config(
    page_title="dashboard",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:andre.holzer.biotech@gmail.com',
        'Report a bug': "https://github.com/NanoporeHackathon/modidec/issues",
        'About': "###### ModiDec dashboard is developed by [Holzer Scientific Consulting](https://www.andre-holzer.com).\nCopyright 2023-2024. All rights reserved.\n"
    }
)


############################################ 
# Global settings

## number of top families to plot
n_top_families = 10

## define markdown styles
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
.small-font {
    font-size:12px !important;
}            
</style>
""", unsafe_allow_html=True)

# Custom CSS to increase line spacing
css = """
<style>
    .markdown-text-container {
        margin-bottom: 2px; /* Reduce the bottom margin */
    }
</style>
"""

#color schemes: 

# Fetch the primary color from an environment variable
PRIMARY_COLOR = os.getenv('PRIMARY_COLOR', '#FF4B4B')  # Default to a fallback color if not set

# Main scheme:
#px.colors.diverging.RdYlBu

# Grey scale:
grey_palette = [
    '#CCCCCC', # Light grey
    '#999999',  # Medium-light grey
    '#666666',  # Medium-dark grey
    '#333333',  # Dark grey
    ]  

# Medum size color palette:
colors_Set2 = px.colors.qualitative.Set2
colors_Pastel2 = px.colors.qualitative.Pastel2
combined_colors = colors_Set2 + colors_Pastel2

px.defaults.template = "ggplot2"
px.defaults.color_continuous_scale = px.colors.diverging.RdYlBu


############################################
# Functions

## argument parser
def parse_args(args):
    parser = argparse.ArgumentParser('Streamlit data dir')
    parser.add_argument('-i', '--input_directory', help='path to the input directory where new fastq are being deposited', required=True)
    parser.add_argument('-o', '--output_directory', help='path to the output directory of the nextflow pipeline', required=True)
    parser.add_argument('-s', '--start_index', help='start index', required=True)
    parser.add_argument('-e', '--end_index', help='end index', required=True)
    return parser.parse_args(args)


## data mapping progress bar

args = vars(parse_args(sys.argv[1:]))
start_index = args["start_index"]
end_index = args["end_index"]
input_directory = args["input_directory"]
output_directory = args["output_directory"]
 
progress_text = "Data mapping in process..."
percent_complete = 0
number_of_iterations = int(end_index) - int(start_index)
progress_value = 0
my_bar = st.progress(percent_complete, text=progress_text)
number_of_input_files = len(list(pathlib.Path(input_directory).glob('*.bam')))
number_of_output_files =  len(list(pathlib.Path(output_directory).glob('*')))



while percent_complete < 100:
    new_number_of_output_files = len(list(pathlib.Path(output_directory).glob('*')))

    if new_number_of_output_files > number_of_output_files:

        progress_value = new_number_of_output_files / (number_of_input_files* number_of_iterations)
        if progress_value > 1:
            progress_value = 1
        my_bar.progress(progress_value, text=progress_text)
    
    number_of_output_files = new_number_of_output_files
    time.sleep(2)

