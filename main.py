import streamlit as st
import pandas as pd

# Title of the app
st.title("Class Similarity Checker")

# File upload
uploaded_file = st.file_uploader("Upload CSV File", type="csv")

if uploaded_file:
    # Load the dataset
    df = pd.read_csv(uploaded_file)

    # Step 1: Get the list of DOSEN for 3KA19
    dosen_3ka19 = df[df['KELAS'] == '3KA19']['DOSEN'].unique()

    # Step 2: Count overlap of DOSEN for each class
    similarity_counts = {}
    for kelas in df['KELAS'].unique():
        if kelas == '3KA19':
            continue
        # Get unique DOSEN for the current class
        dosen_other = df[df['KELAS'] == kelas]['DOSEN'].unique()
        overlap_count = len(set(dosen_3ka19) & set(dosen_other))
        similarity_counts[kelas] = overlap_count

    # Step 3: Display all classes sorted by similarity
    similarity_df = pd.DataFrame.from_dict(similarity_counts, orient='index', columns=['Overlap Count'])
    similarity_df = similarity_df.sort_values(by='Overlap Count', ascending=False)

    st.subheader("Similarity counts for all classes compared to 3KA19")
    st.dataframe(similarity_df)
