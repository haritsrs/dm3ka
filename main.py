import streamlit as st
import pandas as pd

st.title("Pemeriksa Kesamaan Dosen 3KA Depok")
st.subheader("Aplikasi untuk membandingkan dosen dan mata kuliah antara kelas")
st.write("Dibuat oleh: Harits Raharjo Setiono")

df = pd.read_csv('baak.csv')
df = df.dropna(subset=['KELAS', 'DOSEN', 'MATA KULIAH'])
df['KELAS'] = df['KELAS'].astype(str)
df['DOSEN'] = df['DOSEN'].astype(str)
df['MATA KULIAH'] = df['MATA KULIAH'].astype(str)
df = df.drop_duplicates(subset=['KELAS', 'DOSEN', 'MATA KULIAH'])

classes = df['KELAS'].unique()

with st.expander("Pembandingan dengan semua Kelas", expanded=False):
    input_class_numbers = st.multiselect(
        "Pilih angka kelasnya untuk dibandingkan:", 
        options=classes,
        default=[classes[0]]
    )
    valid_classes = [cls for cls in input_class_numbers if cls in classes]
    if st.button("Bandingkan", key="compare_all_classes"):
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
                st.subheader(f"Jumlah kesamaan untuk {input_class}")
                similarity_df = pd.DataFrame.from_dict(similarity_counts[input_class], orient='index', columns=['Jumlah Overlap'])
                similarity_df = similarity_df.sort_values(by='Jumlah Overlap', ascending=False)
                st.dataframe(similarity_df)
        else:
            st.warning("Tolong pilih kelas yang valid (1-20).")

with st.expander("Pembandingan Dosen dan Mata Kuliah antara dua Kelas", expanded=False):
    input_class_1 = st.selectbox("Pilih kelas pertama:", options=classes, index=0)
    input_class_2 = st.selectbox("Pilih kelas kedua:", options=classes, index=1)
    valid_classes_in_data = [cls for cls in [input_class_1, input_class_2] if cls in classes]
    if st.button("Bandingkan", key="compare_two_classes"):
        if len(valid_classes_in_data) == 2:
            st.subheader(f"DOSEN dan MATA KULIAH untuk {input_class_1}")
            df_class_1 = df[df['KELAS'] == input_class_1][['DOSEN', 'MATA KULIAH']].drop_duplicates()
            st.dataframe(df_class_1)
            st.subheader(f"DOSEN dan MATA KULIAH untuk {input_class_2}")
            df_class_2 = df[df['KELAS'] == input_class_2][['DOSEN', 'MATA KULIAH']].drop_duplicates()
            st.dataframe(df_class_2)
            overlap_dosen = set(df_class_1['DOSEN']) & set(df_class_2['DOSEN'])
            overlap_matakuliah = set(df_class_1['MATA KULIAH']) & set(df_class_2['MATA KULIAH'])
            overlap_data = []
            for dosen in overlap_dosen:
                overlap_data.append({
                    'DOSEN': dosen,
                    'MATA KULIAH (Kelas 1)': df_class_1[df_class_1['DOSEN'] == dosen]['MATA KULIAH'].values[0],
                    'MATA KULIAH (Kelas 2)': df_class_2[df_class_2['DOSEN'] == dosen]['MATA KULIAH'].values[0]
                })
            for matakuliah in overlap_matakuliah:
                if not any(item['MATA KULIAH (Kelas 1)'] == matakuliah for item in overlap_data):
                    overlap_data.append({
                        'DOSEN': 'N/A',
                        'MATA KULIAH (Kelas 1)': matakuliah,
                        'MATA KULIAH (Kelas 2)': matakuliah
                    })
            overlap_df = pd.DataFrame(overlap_data)
            overlap_df = overlap_df[(overlap_df['DOSEN'] != 'N/A') | (overlap_df['MATA KULIAH (Kelas 1)'] != overlap_df['MATA KULIAH (Kelas 2)'])]
            st.subheader(f"Overlap antara {input_class_1} dan {input_class_2}")
            if overlap_df.empty:
                st.write("Tidak ditemukan overlap.")
            else:
                st.dataframe(overlap_df)
        else:
            st.warning("Tolong masukkan angka kelas yang valid (1-20) yang ada dalam daftar kelas.")

with st.expander("Perbandingan Kelas berdasarkan Dosen dan Mata Kuliah", expanded=False):
    selected_class = st.selectbox("Pilih kelas:", classes)
    dosen_in_class = df[df['KELAS'] == selected_class]['DOSEN'].unique()
    selected_dosen = st.selectbox("Pilih DOSEN:", dosen_in_class)
    if st.button("Bandingkan Kelas Lain", key="compare_by_dosen"):
        dosen_classes = df[df['DOSEN'] == selected_dosen]
        selected_class_subjects = set(
            dosen_classes[dosen_classes['KELAS'] == selected_class]['MATA KULIAH']
        )
        comparison_data = []
        for _, row in dosen_classes.iterrows():
            class_name = row['KELAS']
            subject_name = row['MATA KULIAH']
            if class_name != selected_class:
                comparison_data.append({
                    'KELAS': class_name,
                    'MATA KULIAH': subject_name,
                })
        comparison_df = pd.DataFrame(comparison_data)
        st.subheader(f"Kelas lain yang diajar oleh {selected_dosen}")
        if comparison_df.empty:
            st.write(f"Tidak ada kelas lain yang diajar oleh {selected_dosen}.")
        else:
            st.dataframe(comparison_df)

st.write("Versi 1.4")