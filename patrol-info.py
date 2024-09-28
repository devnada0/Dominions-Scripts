import numpy as np

def calculate_stealth_strength(leader_stealth_ability=40, units_under_command_lt50=0, units_under_command_ge50=0):
    """
    Calculates the stealth strength of the sneaking units.
    """
    stealth_strength = leader_stealth_ability - units_under_command_lt50 - 0.5 * units_under_command_ge50
    return stealth_strength

def calculate_destealth_strength(patrol_strength=29, unrest=10, province_defense=6):
    """
    Calculates the destealth strength based on patrol strength, unrest, and province defense.
    """
    destealth_strength = patrol_strength - min(unrest, 100)/2 + max(0, province_defense - 14)
    return destealth_strength

def exploding_dice_roll(sides):
    """
    Simulates an exploding die roll.
    """
    total = 0
    while True:
        roll = np.random.randint(1, sides+1)
        total += roll
        if roll < sides:
            break
    return total

def simulate_detection_probability(stealth_strength, destealth_strength, simulations=100000):
    """
    Simulates the detection process to estimate the probability of finding stealth units.
    """
    successes = 0
    for _ in range(simulations):
        stealth_roll = exploding_dice_roll(25) + exploding_dice_roll(25)
        destealth_roll = exploding_dice_roll(25) + exploding_dice_roll(25)
        stealth_total = stealth_strength + stealth_roll
        destealth_total = destealth_strength + destealth_roll
        if destealth_total > stealth_total:
            successes += 1
    probability = successes / simulations
    return probability

def simulate_unrest_reduction(patrol_strength, unrest, simulations=100000):
    """
    Simulates the unrest reduction process to calculate the average unrest reduced and its standard deviation.
    """
    unrest_reductions = []
    for _ in range(simulations):
        unrest_roll = exploding_dice_roll(50)
        if unrest_roll > patrol_strength + 25:
            continue
        unrest_reduced = np.random.randint(0, int(patrol_strength) + 1)
        unrest_reductions.append(unrest_reduced)
    if unrest_reductions:
        average_unrest_reduced = np.mean(unrest_reductions)
        std_unrest_reduced = np.std(unrest_reductions)
        probability = len(unrest_reductions) / simulations
    else:
        average_unrest_reduced = 0
        std_unrest_reduced = 0
        probability = 0
    return probability, average_unrest_reduced, std_unrest_reduced

def main():
    """
    Main function that runs the script. It collects user inputs, performs calculations,
    and displays the results.
    """
    # Default values
    leader_stealth_ability = 40
    units_under_command_lt50 = 0
    units_under_command_ge50 = 0
    patrol_strength = 29
    unrest = 10
    province_defense = 6
    simulations = 100000

    # Input from the user
    leader_stealth_ability = float(input("Enter leader's stealth ability (default 40): ") or 40)
    units_under_command_lt50 = int(input("Enter number of stealthy units under command with stealth ability < 50 (default 0): ") or 0)
    units_under_command_ge50 = int(input("Enter number of stealthy units under command with stealth ability >= 50 (default 0): ") or 0)
    patrol_strength = float(input("Enter patrol strength (default 29): ") or 29)
    unrest = float(input("Enter unrest value (default 10): ") or 10)
    province_defense = int(input("Enter province defense (default 6): ") or 6)
    simulations = int(input("Enter number of iterations to run (default 100000): ") or 100000)

    # Calculations
    stealth_strength = calculate_stealth_strength(leader_stealth_ability, units_under_command_lt50, units_under_command_ge50)
    destealth_strength = calculate_destealth_strength(patrol_strength, unrest, province_defense)
    detection_probability = simulate_detection_probability(stealth_strength, destealth_strength, simulations=simulations)
    unrest_probability, average_unrest_reduced, std_unrest_reduced = simulate_unrest_reduction(patrol_strength, unrest, simulations=simulations)

    # Outputs
    print("\nResults:")
    print(f"Chance of finding the unit: {detection_probability*100:.2f}%")
    print(f"Average amount of unrest reduced with STD: {average_unrest_reduced:.2f} (±{std_unrest_reduced:.2f})")
    print(f"Chance of reducing unrest: {unrest_probability*100:.2f}%")

if __name__ == "__main__":
    main()
