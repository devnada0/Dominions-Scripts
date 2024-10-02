import numpy as np
import matplotlib.pyplot as plt

# Function to prompt for scout reports
def get_scout_reports():
    while True:
        try:
            reports_input = input("Enter scout reports separated by commas (e.g., 60,80,70): ")
            scout_reports = [int(x.strip()) for x in reports_input.split(',')]
            if len(scout_reports) == 0:
                raise ValueError
            return scout_reports
        except ValueError:
            print("Invalid input. Please enter integers separated by commas.")

# Function to prompt for error percentage
def get_error_percentage():
    while True:
        try:
            error_input = input("Enter error percentage (default is 50): ")
            if error_input.strip() == '':
                return 50.0
            error_percent = float(error_input)
            if error_percent <= 0 or error_percent >= 100:
                raise ValueError
            return error_percent
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100.")

# Get user inputs
scout_reports = get_scout_reports()
error_percent = get_error_percentage()

# Possible actual unit counts
P = error_percent / 100  # Convert percentage to proportion
min_report = min(scout_reports)
max_report = max(scout_reports)

# Calculate N_min and N_max based on the error percentage and rounding
N_min = int(np.floor((min_report / (1 + P)) / 10) * 10)
N_max = int(np.ceil((max_report / (1 - P)) / 10) * 10)

# Ensure N_min and N_max are within valid ranges
N_min = max(N_min, 10)  # Minimum units cannot be less than 10
N_max = max(N_max, N_min + 10)  # Ensure at least one value in the range

print(f"Possible actual unit counts range from {N_min} to {N_max}")

N_values = range(N_min, N_max + 10, 10)  # Consider multiples of 10

# Initialize probability dictionary
probabilities = {}

# Function to calculate the probability of a reported unit given N
def probability_of_report(N, reported_unit):
    # The error percentage ranges uniformly from -P to +P
    error_percentages = np.linspace(-P, P, 101)  # 101 values from -P to +P
    # Calculate possible reported units
    possible_reports = N * (1 + error_percentages)
    # Round to nearest multiple of 10
    possible_reports = 10 * np.round(possible_reports / 10)
    # Calculate the probability of each possible reported unit
    unique, counts = np.unique(possible_reports, return_counts=True)
    probabilities = counts / counts.sum()
    # Create a mapping from reported units to their probabilities
    report_prob_dict = dict(zip(unique, probabilities))
    # Return the probability of the reported unit
    return report_prob_dict.get(reported_unit, 0)

# Calculate the probability for each N
for N in N_values:
    # Initialize total probability for N
    total_prob_N = 1
    for report in scout_reports:
        prob = probability_of_report(N, report)
        # If probability is zero, this N is not possible
        if prob == 0:
            total_prob_N = 0
            break
        # Multiply probabilities (assuming independence)
        total_prob_N *= prob
    probabilities[N] = total_prob_N

# Remove N with zero probability
probabilities = {N: prob for N, prob in probabilities.items() if prob > 0}

# Normalize probabilities
total_prob = sum(probabilities.values())
if total_prob > 0:
    for N in probabilities:
        probabilities[N] /= total_prob

    # Sort the probabilities for plotting
    sorted_N = sorted(probabilities.keys())
    sorted_probs = [probabilities[N] for N in sorted_N]

    # Plotting the probability distribution
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_N, sorted_probs, color='skyblue')
    plt.title('Probability Distribution of Actual Unit Counts')
    plt.xlabel('Actual Number of Units (N)')
    plt.ylabel('Probability')
    plt.grid(True)
    plt.show()

    # Print probabilities
    print("\nProbability distribution:")
    for N in sorted_N:
        print(f"Actual Units: {N}, Probability: {probabilities[N]:.6f}")
else:
    print("No possible actual unit counts could produce the given scout reports with the specified error percentage.")
