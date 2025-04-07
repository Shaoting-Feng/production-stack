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

# Count the distribution of num_round values
counter = Counter(num_round_list)
total = sum(counter.values())

# Sort the keys and calculate the cumulative frequency distribution
sorted_keys = sorted(counter.keys())
cumulative = 0
cum_freq = []
for key in sorted_keys:
    cumulative += counter[key]
    cum_freq.append(cumulative / total)

# Plot the cumulative distribution using a step plot
plt.figure()
plt.step(sorted_keys, cum_freq, where="post")
plt.xlabel("num_round")
plt.ylabel("Cumulative Frequency")
plt.title("Cumulative Distribution of num_round for All Items")
plt.ylim(0, 1)
plt.savefig("ShareGPT_num_round_cumulative_distribution.pdf")
plt.close()

# Calculate and print the percentages for thresholds 5, 10, and 20
thresholds = [5, 10, 20]
for t in thresholds:
    count_below = sum(count for key, count in counter.items() if key < t)
    percentage = (count_below / total) * 100
    print(f"Percentage of conversations with num_round less than {t}: {percentage:.2f}%")
