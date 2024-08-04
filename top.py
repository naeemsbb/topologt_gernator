import streamlit as st
import os
import subprocess
from topology_genrator import preprocess_ligand, generate_topology
import numpy as np

# Streamlit interface setup
st.title('Topology Generator')
st.write('Upload your .mol2 or .pdb file to generate topology files.')

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=['mol2', 'pdb'])
if uploaded_file is not None:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success('File uploaded successfully!')

    # Preprocess the ligand
    if st.button('Preprocess Ligand'):
        preprocess_cmd = f'preprocess_ligand {uploaded_file.name}'
        subprocess.run(preprocess_cmd, shell=True)
        preprocessed_file_name = f"{uploaded_file.name.split('.')[0]}_preprocessed.mol2"
        st.success(f'Preprocessed file created: {preprocessed_file_name}')

        # Generate topology files
        if st.button('Generate Topology'):
            generate_cmd = f'generate_topology {preprocessed_file_name}'
            subprocess.run(generate_cmd, shell=True)

            gro_file = uploaded_file.name.split('.')[0] + '.gro'
            itp_file = uploaded_file.name.split('.')[0] + '.itp'
            prm_file = uploaded_file.name.split('.')[0] + '.prm'

            # Download links
            st.success('Topology files generated successfully!')
            with open(gro_file, "rb") as f:
                st.download_button('Download .gro file', f, file_name=gro_file)
            with open(itp_file, "rb") as f:
                st.download_button('Download .itp file', f, file_name=itp_file)
            with open(prm_file, "rb") as f:
                st.download_button('Download .prm file', f, file_name=prm_file)

# Dependencies
# Make sure to include 'topology_generator' in your requirements.txt along with 'parmed'
# For example:
# topology_generator==<version>
# parmed

# To run the Streamlit application, save this script and run `streamlit run your_script_name.py`
