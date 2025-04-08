import json
import matplotlib.pyplot as plt
from transformers import AutoTokenizer

MODEL_NAME = "meta-llama/Llama-3.1-70B-Instruct"

def main():
    # Load your JSON file
    with open("round_robin_5000.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data = data[5000:]
    
    # Initialize tokenizer with the specified model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    # Function to calculate token length using the tokenizer
    def calculate_token_length(text: str) -> int:
        tokens = tokenizer.encode(text, add_special_tokens=False)
        return len(tokens)
    
    # Calculate token lengths for each entry in the JSON
    token_lengths = [calculate_token_length(entry["input"]) for entry in data]
    
    # Calculate and print average token lengths for various thresholds
    thresholds = [1000, 1500, 2000, 2500, 5000, 10000, 50000]
    for t in thresholds:
        if len(data) >= t:
            avg = sum(token_lengths[:t]) / t
            print(f"Average token length for first {t} entries: {avg:.2f}")
        else:
            print(f"Not enough entries to calculate average for first {t} entries (only {len(data)} entries available).")
    
    # Create x-axis values (1, 2, 3, ...)
    x_values = list(range(1, len(data) + 1))
    
    # Scatter plot of token lengths vs. sequence index
    plt.scatter(x_values, token_lengths)
    plt.title("Input Token Length vs Sequence")
    plt.xlabel("Sequence of Input")
    plt.ylabel("Token Length (approx.)")
    plt.grid(True)
    
    # Save the plot to a file named "xxx.png"
    plt.savefig("xxx.png")
    plt.show()

if __name__ == "__main__":
    main()
