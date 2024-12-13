import streamlit as st
import pandas as pd

# Title of the app
st.title("Pemeriksa Kesamaan Dosen 3KA Depok")

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

# Collapsible section
with st.expander("Pembandingan dengan semua kelas", expanded=False):
    # Input field for class numbers
    input_class_numbers = st.text_area(
        "Ketik angka kelasnya untuk dibandingkan, bila lebih dari 1 gunakan koma (Contoh: 1, 2, 3):", "19"
    )

    # Split the input into a list of class numbers and convert them to the full class code
    class_prefix = "3KA"
    input_class_numbers = [str(num).strip() for num in input_class_numbers.split(",")]

    # Create the full class names (e.g., '3KA01', '3KA02', etc.)
    input_classes = [class_prefix + num.zfill(2) for num in input_class_numbers]

    # Ensure that the inputted classes are valid
    valid_classes = [cls for cls in input_classes if cls in classes]

    # Submit Button for Class Comparison
    if st.button("Bandingkan", key="compare_all_classes"):
        if valid_classes:
            # Initialize a dictionary to store similarity counts for each class
            similarity_counts = {}

            for input_class in valid_classes:
                # Get the list of DOSEN for the current class
                dosen_input_class = df[df['KELAS'] == input_class]['DOSEN'].unique()

                # Calculate the overlap of DOSEN with all other classes
                for kelas in classes:
                    if kelas == input_class:  # Skip comparing the class to itself
                        continue

                    dosen_other_class = df[df['KELAS'] == kelas]['DOSEN'].unique()
                    overlap_count = len(set(dosen_input_class) & set(dosen_other_class))

                    # Store the result in the dictionary
                    if input_class not in similarity_counts:
                        similarity_counts[input_class] = {}
                    similarity_counts[input_class][kelas] = overlap_count

            # Display the similarity results for each selected class
            for input_class in valid_classes:
                st.subheader(f"Jumlah kesamaan untuk {input_class}")
                similarity_df = pd.DataFrame.from_dict(similarity_counts[input_class], orient='index', columns=['Jumlah Overlap'])
                similarity_df = similarity_df.sort_values(by='Jumlah Overlap', ascending=False)
                st.dataframe(similarity_df)

        else:
            st.warning("Tolong ketik kelas yang valid (1-20).")

# New feature: Check specific DOSEN and MATA KULIAH overlap between two classes

# Let the user input class numbers (1 to 20) for two classes to compare
with st.expander("Pembandingan DOSEN dan MATA KULIAH antara dua kelas", expanded=False):
    input_class_1_number = st.text_input("Ketik kelas pertama (1 sampai 20, Contoh: 1):", "1")
    input_class_2_number = st.text_input("Ketik kelas kedua (1 sampai 20, Contoh: 2):", "2")

    # Convert numbers to full class names (e.g., '3KA01', '3KA02')
    input_class_1 = class_prefix + str(input_class_1_number).zfill(2)
    input_class_2 = class_prefix + str(input_class_2_number).zfill(2)

    # Ensure that the inputted classes are valid
    valid_classes_in_data = [cls for cls in [input_class_1, input_class_2] if cls in classes]

    # Submit Button for New Feature: DOSEN and MATA KULIAH Overlap Between Two Classes
    if st.button("Bandingkan", key="compare_two_classes"):
        if len(valid_classes_in_data) == 2:
            # Step 1: Display the DOSEN and MATA KULIAH for the two selected classes
            st.subheader(f"DOSEN dan MATA KULIAH untuk {input_class_1}")
            df_class_1 = df[df['KELAS'] == input_class_1][['DOSEN', 'MATA KULIAH']].drop_duplicates()
            st.dataframe(df_class_1)

            st.subheader(f"DOSEN dan MATA KULIAH untuk {input_class_2}")
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
                    'MATA KULIAH (Kelas 1)': df_class_1[df_class_1['DOSEN'] == dosen]['MATA KULIAH'].values[0],
                    'MATA KULIAH (Kelas 2)': df_class_2[df_class_2['DOSEN'] == dosen]['MATA KULIAH'].values[0]
                })
            
            # Add overlap for MATA KULIAH
            for matakuliah in overlap_matakuliah:
                # Only show MATA KULIAH that is not already in the DOSEN overlap data
                if not any(item['MATA KULIAH (Kelas 1)'] == matakuliah for item in overlap_data):
                    overlap_data.append({
                        'DOSEN': 'N/A',  # No specific DOSEN for this MATA KULIAH
                        'MATA KULIAH (Kelas 1)': matakuliah,
                        'MATA KULIAH (Kelas 2)': matakuliah
                    })

            # Create a DataFrame for the overlap results
            overlap_df = pd.DataFrame(overlap_data)

            # Step 4: Filter out rows where both DOSEN and MATA KULIAH are 'N/A'
            overlap_df = overlap_df[(overlap_df['DOSEN'] != 'N/A') | (overlap_df['MATA KULIAH (Kelas 1)'] != overlap_df['MATA KULIAH (Kelas 2)'])]

            # Step 5: Display the overlap data in a table
            st.subheader(f"Overlap antara {input_class_1} dan {input_class_2}")
            if overlap_df.empty:
                st.write("Tidak ditemukan overlap.")
            else:
                st.dataframe(overlap_df)

        else:
            st.warning("Tolong masukkan angka kelas yang valid (1-20) yang ada dalam daftar kelas.")
