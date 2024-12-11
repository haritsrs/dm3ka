import streamlit as st
import pandas as pd

# Title of the app
st.title("Class Similarity Checker")

# Load the dataset directly from the existing 'baak.csv'
df = pd.read_csv('baak.csv')  # Make sure baak.csv is in the same directory as this script

# Preprocessing steps:
# 1. Ensure there are no missing values in 'KELAS' and 'DOSEN'
df = df.dropna(subset=['KELAS', 'DOSEN'])

# 2. Ensure 'KELAS' and 'DOSEN' are in string format
df['KELAS'] = df['KELAS'].astype(str)
df['DOSEN'] = df['DOSEN'].astype(str)

# 3. Remove duplicates
df = df.drop_duplicates(subset=['KELAS', 'DOSEN'])

# Get the list of available classes (in '3KA01', '3KA02', etc. format)
classes = df['KELAS'].unique()

# Let the user input class numbers (1 to 20) as integers
input_class_numbers = st.text_area("Enter class numbers to compare (1 to 20), separated by commas (e.g., 1, 2, 3):", "1")

# Split the input into a list of class numbers (as strings) and convert them to the full class code
class_prefix = "3KA"
input_class_numbers = [str(num).strip() for num in input_class_numbers.split(",")]

# Create the full class names (e.g., '3KA01', '3KA02', etc.)
input_classes = [class_prefix + num.zfill(2) for num in input_class_numbers]

# Ensure that the inputted classes are valid
valid_classes = [cls for cls in input_classes if cls in classes]

if valid_classes:
    # Step 1: Initialize a dictionary to store similarity counts for each class
    similarity_counts = {}

    for input_class in valid_classes:
        # Get the list of DOSEN for the current class
        dosen_input_class = df[df['KELAS'] == input_class]['DOSEN'].unique()

        # Step 2: Calculate the overlap of DOSEN with all other classes
        for kelas in classes:
            if kelas == input_class:  # Skip comparing the class to itself
                continue
            
            dosen_other_class = df[df['KELAS'] == kelas]['DOSEN'].unique()
            overlap_count = len(set(dosen_input_class) & set(dosen_other_class))

            # Store the result in the dictionary
            if input_class not in similarity_counts:
                similarity_counts[input_class] = {}
            similarity_counts[input_class][kelas] = overlap_count

    # Step 3: Display the similarity results for each selected class
    for input_class in valid_classes:
        st.subheader(f"Similarity counts for {input_class}")
        similarity_df = pd.DataFrame.from_dict(similarity_counts[input_class], orient='index', columns=['Overlap Count'])
        similarity_df = similarity_df.sort_values(by='Overlap Count', ascending=False)
        st.dataframe(similarity_df)
else:
    st.warning("Please enter valid class numbers (1-20) from the available options.")
