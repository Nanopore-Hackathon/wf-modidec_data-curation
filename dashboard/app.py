import time
import os
import sys
import datetime
import argparse
from pathlib import Path
#from datetime import datetime, timedelta
import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import subprocess
from PIL import Image
from plotly.colors import qualitative
import numpy as np
from plotly.subplots import make_subplots
import glob
import json

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
    parser.add_argument('-o', '--output_directory', help='path to the output directory of the nextflow pipeline', required=True)
    parser.add_argument('-d', '--docs_directory', help='path to the docs directory of the github', required=True)
    #parser.add_argument('-i', '--input_directory', help='path to the input directory where new fastq are being deposited', required=True)
    return parser.parse_args(args)

## read the kraken data
def get_kraken_data(path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", names = ["perc_cov", "n_reads_root", "n_reads", "rank", "tax_ID", "sc_name"])


############################################ 
# Imports

## get arguments to run app
args = vars(parse_args(sys.argv[1:]))
out_path_base = args["output_directory"]
docs_path_base = args["docs_directory"]

## define the paths to input files
multiqc_path = os.path.join(out_path_base, "QC/multiqc_report.html")
pavian_path = os.path.join(out_path_base, "data/kraken2/sankeyNetwork.html")
krona_path = os.path.join(out_path_base, "img/krona_kraken2_16s_BC03_16S_test_sub4000_bracken_genuses.html")

## create time dataframe
time_path = os.path.join(out_path_base, "n_reads_time.tsv")


############################################
# Sidebar

## Logo
logo=os.path.join(docs_path_base, 'img/RT-metagenomics-logo_light.png')
st.sidebar.image(logo)

## Menu
with st.sidebar:
    selected = option_menu("ModiDec", ["Dashboard"], 
        icons=['house'], menu_icon="cast", default_index=0, #'activity',
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "nav-link": {"text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "lightblue"},
        }
    )
        

############################################
# Initialise page content

placeholder = st.empty() # init placeholder

## wait until output structure has been generated
with st.spinner('Wait for output structure to be created ..'):
    while os.path.isdir(os.path.join(out_path_base, "data/")) == False:
        # do nothing
        time.sleep(1)
    #st.info('Output structure available')

# Initialize the time dataframe
if not os.path.exists(time_path):
    df_time = pd.DataFrame(columns = ["n_reads_total", "n_families", "sys_time", "barcode","file_name","file_time"])
    df_time.to_csv(time_path, index=False)


############################################
# Sidebar controls and footer

st.sidebar.markdown("**Pipeline execution**")

## About section
st.sidebar.divider()
url1 = "https://github.com/Nanopore-Hackathon/ModiDec"
st.sidebar.markdown("[:blue[Version: 2024-05-12]](%s)"%url1)
st.sidebar.caption("**Research use only**")
#st.sidebar.markdown("<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>", unsafe_allow_html=True)
url2 = "https://www.andre-holzer.com"
st.sidebar.caption("[:grey[©2024 Holzer Scientific Consulting]](%s)"%url2)   


############################################
# Page content once data is available

# Start infinite loop
while True:

    ## Check if the files exist
    multiqc_exists = os.path.exists(multiqc_path)
    pavian_exists = os.path.exists(pavian_path)
    krona_exists = os.path.exists(krona_path)

    # get current list of bracken files
    file_list = [os.path.join(out_path_base, "data/bracken", x) for x in os.listdir(os.path.join(out_path_base, "data/bracken")) if x.endswith("_merged.bracken.kreport")]
    

    ############################################
    # Dashboard

    if selected == "Dashboard":
        with placeholder.container():

            # page title
            st.header("Dashboard")

            # summary boxes
            col1, col2 = st.columns(2, gap="small")

            with col1:
                container = st.container(border=True)
                container.markdown('<p style="font-family:sans-serif; color:grey90; gap: 0rem; margin-bottom: 10px; font-size: 12px; text-align: left;">Samples:</p>', unsafe_allow_html=True)
                container.markdown(f'<p style="font-family:sans-serif; color:{PRIMARY_COLOR}; gap: 0rem; margin-bottom: 5px; font-size: 22px; text-align: center;"># {n_samples}</p>', unsafe_allow_html=True)
                container.markdown('<p style="font-family:sans-serif; color:grey; gap: 0rem; margin-bottom: 15px; font-size: 12px; text-align: center;">of max. 12</p>', unsafe_allow_html=True)

            with col2:
                container = st.container(border=True)
                container.markdown('<p style="font-family:sans-serif; color:grey90; gap: 0rem; margin-bottom: 10px; font-size: 12px; text-align: left;">Reads:</p>', unsafe_allow_html=True)
                container.markdown(f'<p style="font-family:sans-serif; color:{PRIMARY_COLOR}; gap: 0rem; margin-bottom: 5px; font-size: 22px; text-align: center;">{formatted_totalreads}</p>', unsafe_allow_html=True)
                container.markdown(f'<p style="font-family:sans-serif; color:grey; gap: 0rem; margin-bottom: 15px; font-size: 12px; text-align: center;">~ {formatted_averagereads} per sample</p>', unsafe_allow_html=True)

            #st.divider()


    
    time.sleep(2) # sleep for a few sec before the next iteration