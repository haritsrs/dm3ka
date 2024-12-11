import streamlit as st
import pandas as pd

# Title of the app
st.title("Class Similarity Checker")

# Load the dataset directly from the existing 'baak.csv'
df = pd.read_csv('baak.csv')  # Make sure baak.csv is in the same directory as this script

# Preprocessing steps:
# 1. Ensure there are no missing values in 'KELAS', 'DOSEN', and 'MATA KULIAH'
df = df.dropna(subset=['KELAS', 'DOSEN', 'MATA KULIAH'])

# 2. Ensure 'KELAS', 'DOSEN', and 'MATA KULIAH' are in string format
df['KELAS'] = df['KELAS'].astype(str)
df['DOSEN'] = df['DOSEN'].astype(str)
df['MATA KULIAH'] = df['MATA KULIAH'].astype(str)

# 3. Remove duplicates
df = df.drop_duplicates(subset=['KELAS', 'DOSEN', 'MATA KULIAH'])

# Get the list of available classes (in '3KA01', '3KA02', etc. format)
classes = df['KELAS'].unique()

# Old feature: Class comparison to all other classes

# Let the user input class numbers (1 to 20) as integers
input_class_numbers = st.text_area("Enter class numbers to compare, separated by commas (e.g., 1, 2, 3):", "1, 2, 3")

# Split the input into a list of class numbers (as strings) and convert them to the full class code
class_prefix = "3KA"
input_class_numbers = [str(num).strip() for num in input_class_numbers.split(",")]

# Create the full class names (e.g., '3KA01', '3KA02', etc.)
input_classes = [class_prefix + num.zfill(2) for num in input_class_numbers]

# Ensure that the inputted classes are valid
valid_classes = [cls for cls in input_classes if cls in classes]

# Submit Button for Old Feature: Class Comparison to All Other Classes
if st.button("Compare to Other Classes"):
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
        st.warning("Please enter valid class numbers from the available options.")

# New feature: Check specific DOSEN and MATA KULIAH overlap between two classes

# Let the user input class numbers (1 to 20) for two classes to compare
input_class_1_number = st.text_input("Enter the first class number (1 to 20, e.g., 1):", "1")
input_class_2_number = st.text_input("Enter the second class number (1 to 20, e.g., 2):", "2")

# Convert numbers to full class names (e.g., '3KA01', '3KA02')
input_class_1 = class_prefix + str(input_class_1_number).zfill(2)
input_class_2 = class_prefix + str(input_class_2_number).zfill(2)

# Ensure that the inputted classes are valid
valid_classes_in_data = [cls for cls in [input_class_1, input_class_2] if cls in classes]

# Submit Button for New Feature: DOSEN and MATA KULIAH Overlap Between Two Classes
if st.button("Check DOSEN and MATA KULIAH Overlap"):
    if len(valid_classes_in_data) == 2:
        # Step 1: Display the DOSEN and MATA KULIAH for the two selected classes
        st.subheader(f"DOSEN and MATA KULIAH for {input_class_1}")
        df_class_1 = df[df['KELAS'] == input_class_1][['DOSEN', 'MATA KULIAH']].drop_duplicates()
        st.dataframe(df_class_1)

        st.subheader(f"DOSEN and MATA KULIAH for {input_class_2}")
        df_class_2 = df[df['KELAS'] == input_class_2][['DOSEN', 'MATA KULIAH']].drop_duplicates()
        st.dataframe(df_class_2)

        # Step 2: Find the overlap of DOSEN and MATA KULIAH between the two classes
        overlap_dosen = set(df_class_1['DOSEN']) & set(df_class_2['DOSEN'])
        overlap_matakuliah = set(df_class_1['MATA KULIAH']) & set(df_class_2['MATA KULIAH'])

        # Step 3: Create a DataFrame to display the overlap data in a table
        overlap_data = []

        # Add overlap for DOSEN
        for dosen in overlap_dosen:
            overlap_data.append({
                'DOSEN': dosen,
                'MATA KULIAH (Class 1)': df_class_1[df_class_1['DOSEN'] == dosen]['MATA KULIAH'].values[0],
                'MATA KULIAH (Class 2)': df_class_2[df_class_2['DOSEN'] == dosen]['MATA KULIAH'].values[0]
            })
        
        # Add overlap for MATA KULIAH
        for matakuliah in overlap_matakuliah:
            # Only show MATA KULIAH that is not already in the DOSEN overlap data
            if not any(item['MATA KULIAH (Class 1)'] == matakuliah for item in overlap_data):
                overlap_data.append({
                    'DOSEN': 'N/A',  # No specific DOSEN for this MATA KULIAH
                    'MATA KULIAH (Class 1)': matakuliah,
                    'MATA KULIAH (Class 2)': matakuliah
                })

        # Create a DataFrame for the overlap results
        overlap_df = pd.DataFrame(overlap_data)

        # Step 4: Filter out rows where both DOSEN and MATA KULIAH are 'N/A'
        overlap_df = overlap_df[(overlap_df['DOSEN'] != 'N/A') | (overlap_df['MATA KULIAH (Class 1)'] != overlap_df['MATA KULIAH (Class 2)'])]

        # Step 5: Display the overlap data in a table
        st.subheader(f"Overlap between {input_class_1} and {input_class_2}")
        if overlap_df.empty:
            st.write("No overlap found.")
        else:
            st.dataframe(overlap_df)

    else:
        st.warning("Please enter valid class numbers (1-20) that exist in the available classes.")
