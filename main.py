import pandas as pd

# Load the dataset
file_path = 'baak.csv'
df = pd.read_csv(file_path)

# Step 1: Get the list of DOSEN for 3KA19
dosen_3ka19 = df[df['KELAS'] == '3KA19']['DOSEN'].unique()

# Step 2: Count overlap of DOSEN for each class
similarity_counts = {}
for kelas in df['KELAS'].unique():
    if kelas == '3KA19':
        continue
    # Get unique DOSEN for the current class
    dosen_other = df[df['KELAS'] == kelas]['DOSEN'].unique()
    # Calculate overlap
    overlap_count = len(set(dosen_3ka19) & set(dosen_other))
    similarity_counts[kelas] = overlap_count

# Step 3: Display all classes sorted by similarity
similarity_df = pd.DataFrame.from_dict(similarity_counts, orient='index', columns=['Overlap Count'])
similarity_df = similarity_df.sort_values(by='Overlap Count', ascending=False)

# Print the sorted DataFrame
print("Similarity counts for all classes compared to 3KA19:")
print(similarity_df)
