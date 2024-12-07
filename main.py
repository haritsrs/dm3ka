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

# Step 3: Find the class with the highest overlap
most_similar_class = max(similarity_counts, key=similarity_counts.get)
most_similar_count = similarity_counts[most_similar_class]

# Display the results
print(f"The class most similar to 3KA19 is {most_similar_class} with {most_similar_count} similar DOSEN(s).")
