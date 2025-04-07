import json

# Load the modified JSON that contains fields like "input", "input2", etc.
with open('modified_file.json', 'r') as f:
    data = json.load(f)

# Build a new list to store round-robin results
new_data = []

# First, determine the maximum number of rounds among the entries.
max_round = 0
for entry in data:
    # Count keys that are "input" or "inputN" (where N is a number)
    round_count = 0
    for key in entry:
        if key == "input" or (key.startswith("input") and key[5:].isdigit()):
            round_count += 1
    if round_count > max_round:
        max_round = round_count

# Now perform a round-robin over the rounds:
# For round 1, then round 2, etc., add each entry's corresponding input and output_length (if present) to new_data.
for round_num in range(1, max_round + 1):
    for entry in data:
        input_field = "input" if round_num == 1 else f"input{round_num}"
        output_field = "output_length" if round_num == 1 else f"output_length{round_num}"
        if input_field in entry:
            new_entry = {"input": entry[input_field]}
            # Include output_length if present; if not, default to 20.
            new_entry["output_length"] = entry.get(output_field, 20)
            new_data.append(new_entry)

# Write the new JSON list to a file.
with open('round_robin.json', 'w') as f:
    json.dump(new_data, f, indent=2)
