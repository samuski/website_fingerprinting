import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from export_stats import analyze

TEST_DIRECTORY = "./test"
REFERENCE_CSV = "stats.csv"

df = pd.read_csv(REFERENCE_CSV)

feature_cols = [
    "packets_in", "bytes_in", "packets_out", "bytes_out",
    "in_times_mean", "in_times_median", "in_times_std",
    "out_times_mean", "out_times_median", "out_times_std"
]

X_ref = df[feature_cols]
y_ref = df["site_name"]

# Scale reference data
scaler = StandardScaler()
X_ref_scaled = scaler.fit_transform(X_ref)

# Train KNN classifier
clf = KNeighborsClassifier(n_neighbors=3, weights='distance')
clf.fit(X_ref_scaled, y_ref)

correct, total = 0, 0

for fname in os.listdir(TEST_DIRECTORY):
    if fname.endswith(".pcapng"):
        path = os.path.join(TEST_DIRECTORY, fname)
        print(f"Processing {fname}...")

        try:
            test_stats = analyze(path)
            X_test = pd.DataFrame([test_stats], columns=feature_cols)
            X_test_scaled = scaler.transform(X_test)

            # Debug distances
            distances, indices = clf.kneighbors(X_test_scaled)
            print("Nearest neighbors:")
            for i, dist in zip(indices[0], distances[0]):
                neighbor = df.iloc[i]
                print(f"  {neighbor['site_name']} (distance: {dist:.4f})")

            pred = clf.predict(X_test_scaled)[0]
            actual = fname.split('_')[0]
            print(f"Predicted: {pred} \nActual: {actual}")

            if pred == actual:
                correct += 1
            total += 1
            print("\n--------------------------------------------------------\n")

        except Exception as e:
            print(f"Error classifying {fname}: {e}")

score = (correct / total) * 100
print(f"Score: {score:.2f}% ({correct}/{total})")

