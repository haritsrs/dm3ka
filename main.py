import streamlit as st
import pandas as pd

st.title("Class Similarity Checker")

df = pd.read_csv('baak.csv')

df = df.dropna(subset=['KELAS', 'DOSEN', 'MATA KULIAH'])

df['KELAS'] = df['KELAS'].astype(str)
df['DOSEN'] = df['DOSEN'].astype(str)
df['MATA KULIAH'] = df['MATA KULIAH'].astype(str)

df = df.drop_duplicates(subset=['KELAS', 'DOSEN', 'MATA KULIAH'])

classes = df['KELAS'].unique()

input_class_numbers = st.text_area("Enter class numbers to compare, separated by commas (e.g., 1, 2, 3):", "1, 2, 3")

class_prefix = "3KA"
input_class_numbers = [str(num).strip() for num in input_class_numbers.split(",")]

input_classes = [class_prefix + num.zfill(2) for num in input_class_numbers]

valid_classes = [cls for cls in input_classes if cls in classes]

if st.button("Compare to Other Classes"):
    if valid_classes:
        similarity_counts = {}

        for input_class in valid_classes:
            dosen_input_class = df[df['KELAS'] == input_class]['DOSEN'].unique()

            for kelas in classes:
                if kelas == input_class:
                    continue
                
                dosen_other_class = df[df['KELAS'] == kelas]['DOSEN'].unique()
                overlap_count = len(set(dosen_input_class) & set(dosen_other_class))

                if input_class not in similarity_counts:
                    similarity_counts[input_class] = {}
                similarity_counts[input_class][kelas] = overlap_count

        for input_class in valid_classes:
            st.subheader(f"Similarity counts for {input_class}")
            similarity_df = pd.DataFrame.from_dict(similarity_counts[input_class], orient='index', columns=['Overlap Count'])
            similarity_df = similarity_df.sort_values(by='Overlap Count', ascending=False)
            st.dataframe(similarity_df)

    else:
        st.warning("Please enter valid class numbers from the available options.")

input_class_1_number = st.text_input("Enter the first class number (1 to 20, e.g., 1):", "1")
input_class_2_number = st.text_input("Enter the second class number (1 to 20, e.g., 2):", "2")

input_class_1 = class_prefix + str(input_class_1_number).zfill(2)
input_class_2 = class_prefix + str(input_class_2_number).zfill(2)

valid_classes_in_data = [cls for cls in [input_class_1, input_class_2] if cls in classes]

if st.button("Check DOSEN and MATA KULIAH Overlap"):
    if len(valid_classes_in_data) == 2:
        st.subheader(f"DOSEN and MATA KULIAH for {input_class_1}")
        df_class_1 = df[df['KELAS'] == input_class_1][['DOSEN', 'MATA KULIAH']].drop_duplicates()
        st.dataframe(df_class_1)

        st.subheader(f"DOSEN and MATA KULIAH for {input_class_2}")
        df_class_2 = df[df['KELAS'] == input_class_2][['DOSEN', 'MATA KULIAH']].drop_duplicates()
        st.dataframe(df_class_2)

        overlap_dosen = set(df_class_1['DOSEN']) & set(df_class_2['DOSEN'])
        overlap_matakuliah = set(df_class_1['MATA KULIAH']) & set(df_class_2['MATA KULIAH'])

        overlap_data = []

        for dosen in overlap_dosen:
            overlap_data.append({
                'DOSEN': dosen,
                'MATA KULIAH (Class 1)': df_class_1[df_class_1['DOSEN'] == dosen]['MATA KULIAH'].values[0],
                'MATA KULIAH (Class 2)': df_class_2[df_class_2['DOSEN'] == dosen]['MATA KULIAH'].values[0]
            })
        
        for matakuliah in overlap_matakuliah:
            if not any(item['MATA KULIAH (Class 1)'] == matakuliah for item in overlap_data):
                overlap_data.append({
                    'DOSEN': 'N/A',
                    'MATA KULIAH (Class 1)': matakuliah,
                    'MATA KULIAH (Class 2)': matakuliah
                })

        overlap_df = pd.DataFrame(overlap_data)

        overlap_df = overlap_df[(overlap_df['DOSEN'] != 'N/A') | (overlap_df['MATA KULIAH (Class 1)'] != overlap_df['MATA KULIAH (Class 2)'])]

        st.subheader(f"Overlap between {input_class_1} and {input_class_2}")
        if overlap_df.empty:
            st.write("No overlap found.")
        else:
            st.dataframe(overlap_df)

    else:
        st.warning("Please enter valid class numbers (1-20) that exist in the available classes.")
