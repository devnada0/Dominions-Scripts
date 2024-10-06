import numpy as np
import matplotlib.pyplot as plt

# Function to prompt for scout reports with flexible delimiter (comma or space)
def get_scout_reports(prompt_message):
    while True:
        try:
            reports_input = input(prompt_message)
            if not reports_input.strip():  # If left blank, return an empty list
                return []
            # Split by both commas and spaces, and filter out any empty strings
            scout_reports = [int(x.strip()) for x in reports_input.replace(",", " ").split() if x.strip()]
            return scout_reports
        except ValueError:
            print("Invalid input. Please enter integers separated by commas or spaces.")

# Get user inputs for both types of reports
scout_reports_50 = get_scout_reports("Enter scout reports with 50% error separated by spaces or commas (leave blank for none): ")
scout_reports_30 = get_scout_reports("Enter scout reports with 30% error separated by spaces or commas (leave blank for none): ")

# Combine all reports for analysis, and record which type each report is
all_scout_reports = [(report, 50) for report in scout_reports_50] + [(report, 30) for report in scout_reports_30]

# If there are no reports entered, exit the script
if len(all_scout_reports) == 0:
    print("No scout reports entered. Exiting script.")
    exit()

# Possible actual unit counts (based on the mix of reports)
P_50 = 50 / 100  # Error rate for 50% reports
P_30 = 30 / 100  # Error rate for 30% reports

# Determine the overall min and max possible values based on both types of reports
min_report = min([report for report, _ in all_scout_reports])
max_report = max([report for report, _ in all_scout_reports])

# Calculate N_min and N_max based on the maximum error rate (50%)
N_min = int(np.floor((min_report / (1 + P_50)) / 10) * 10)
N_max = int(np.ceil((max_report / (1 - P_50)) / 10) * 10)

# Ensure N_min and N_max are within valid ranges
N_min = max(N_min, 10)  # Minimum units cannot be less than 10
N_max = max(N_max, N_min + 10)  # Ensure at least one value in the range

print(f"Possible actual unit counts range from {N_min} to {N_max}")

N_values = range(N_min, N_max + 10, 10)  # Consider multiples of 10

# Initialize probability dictionary
probabilities = {}

# Function to calculate the probability of a reported unit given N and an error percentage
def probability_of_report(N, reported_unit, error_percent):
    # The error percentage ranges uniformly from -error_percent to +error_percent
    error_range = np.linspace(-error_percent, error_percent, 101)  # 101 values from -error_percent to +error_percent
    # Calculate possible reported units
    possible_reports = N * (1 + error_range)
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
    for report, error_rate in all_scout_reports:
        if error_rate == 50:
            prob = probability_of_report(N, report, P_50)
        elif error_rate == 30:
            prob = probability_of_report(N, report, P_30)
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
    print("No possible actual unit counts could produce the given scout reports with the specified error percentages.")
