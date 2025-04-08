import json

# Load the modified JSON that contains fields like "input", "input2", etc.
with open('modified_file.json', 'r') as f:
    data = json.load(f)

# Filter out entries with less than 5 rounds.
filtered_data = []
for entry in data:
    # Count keys that are "input" or "inputN" (where N is a number)
    round_count = sum(1 for key in entry if key == "input" or (key.startswith("input") and key[5:].isdigit()))
    if round_count >= 5:  # Only include entries with at least 5 rounds.
        filtered_data.append(entry)

# Determine the maximum number of rounds among the filtered entries.
max_round = 0
for entry in filtered_data:
    round_count = sum(1 for key in entry if key == "input" or (key.startswith("input") and key[5:].isdigit()))
    if round_count > max_round:
        max_round = round_count

# Build a new list to store round-robin results.
new_data = []

# Perform a round-robin over the rounds, ignoring rounds 1 and 2:
for round_num in range(3, max_round + 1):
    for entry in filtered_data:
        input_field = f"input{round_num}"
        output_field = f"output_length{round_num}"
        if input_field in entry:
            new_entry = {"input": entry[input_field]}
            # Include output_length if present; if not, default to 20.
            new_entry["output_length"] = entry.get(output_field, 20)
            new_data.append(new_entry)

# Write the new JSON list to a file.
with open('round_robin.json', 'w') as f:
    json.dump(new_data, f, indent=2)
