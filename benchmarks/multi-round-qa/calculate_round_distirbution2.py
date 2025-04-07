import json
import matplotlib.pyplot as plt
from collections import Counter

# Load the ShareGPT.json file
with open("ShareGPT.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Use all conversation items
data_subset = data

# Extract the num_round values (default to 0 if missing)
num_round_list = [item.get("num_round", 0) for item in data_subset]

# Count the frequency distribution of num_round values
counter = Counter(num_round_list)

# Sort the keys and extract frequencies
sorted_keys = sorted(counter.keys())
frequency = [counter[k] for k in sorted_keys]

# Plot the frequency distribution as a bar chart
plt.figure()
plt.bar(sorted_keys, frequency)
plt.xlabel("num_round")
plt.ylabel("Frequency")
plt.title("Distribution of num_round for All Items")

# Save the plot as a PDF file
plt.savefig("ShareGPT_num_round_distribution.pdf")
plt.close()
