"""
Dominions Collision Calculator
This Python script simulates the army collision mechanics from the game Dominions, based on the rules described in the Army Collision section at:
https://illwiki.com/dom5/map-movement

It calculates the percentage chance of winning a collision against an opponent's army when both armies are moving into each other,
as well as the chance that the armies will move past each other without engaging.

Usage:
- Enter your army's chassis value.
- Enter your opponent's army's chassis value.
- Optionally, enter the number of simulations to run (default is 100,000).

Example:

Dominions Collision Calculator
This calculator simulates army collisions based on the rules from the Dominions game.
Refer to the Army Collision section at https://illwiki.com/dom5/map-movement for more information.

Enter your chassis value: 4394
Enter your opponent's chassis value: 850
Enter the number of simulations to run (default is 100000): 

Calculating, please wait...

With your chassis value of 4394 and your opponent's chassis value of 850:
You have approximately a 94.99% chance of winning the collision.
You have approximately a 5.01% chance of losing the collision.
There is approximately a 0.00% chance that both armies will slip past each other without engaging.

Author: Devnada
"""

import random

def open_ended_die_roll(N):
    """
    Simulates an open-ended die roll for a die with N sides.

    Args:
        N (int): Number of sides on the die (chassis value).

    Returns:
        int: Total of the die roll(s), including any explosions.
    """
    total = 0
    while True:
        roll = random.randint(1, N)
        total += roll
        if roll != N:
            break
    return total

def collision_value(chassis_value):
    """
    Calculates the collision value for a given chassis value.

    Args:
        chassis_value (int): The chassis value of the army.

    Returns:
        float: The collision value.
    """
    die_result = open_ended_die_roll(chassis_value)
    return chassis_value / 10 + die_result

def simulate_collisions(our_chassis_value, opponent_chassis_value, num_trials=100000):
    """
    Simulates the collision mechanics and calculates the win percentage.

    Args:
        our_chassis_value (int): Your army's chassis value.
        opponent_chassis_value (int): Opponent's army chassis value.
        num_trials (int): Number of simulations to run.

    Returns:
        dict: Dictionary containing win percentage, loss percentage, and slip past percentage.
    """
    our_wins = 0
    opponent_wins = 0
    slips = 0

    for _ in range(num_trials):
        # Initial random check for slipping past
        our_random = random.randint(0, 349)
        opponent_random = random.randint(0, 349)

        our_chassis_less = our_chassis_value < our_random
        opponent_chassis_less = opponent_chassis_value < opponent_random

        if our_chassis_less and opponent_chassis_less:
            # Both armies slip past each other
            slips += 1
            continue  # Skip collision resolution

        # Collision occurs
        our_collision = collision_value(our_chassis_value)
        opponent_collision = collision_value(opponent_chassis_value)

        if our_collision > opponent_collision:
            our_wins += 1
        else:
            opponent_wins += 1  # In case of tie, opponent wins (could be adjusted per rules)

    total_collisions = our_wins + opponent_wins
    total_encounters = total_collisions + slips

    win_percentage = (our_wins / total_encounters) * 100
    loss_percentage = (opponent_wins / total_encounters) * 100
    slip_percentage = (slips / num_trials) * 100  # Percentage over total trials

    return {
        'win_percentage': win_percentage,
        'loss_percentage': loss_percentage,
        'slip_percentage': slip_percentage
    }

def main():
    print("Dominions Collision Calculator")
    print("This calculator simulates army collisions based on the rules from the game Dominions.")
    print("Refer to the Army Collision section at https://illwiki.com/dom5/map-movement for more information.\n")

    # Get user inputs with validation
    while True:
        try:
            our_chassis_value = int(input("Enter your chassis value: "))
            if our_chassis_value <= 0:
                raise ValueError("Chassis value must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    while True:
        try:
            opponent_chassis_value = int(input("Enter your opponent's chassis value: "))
            if opponent_chassis_value <= 0:
                raise ValueError("Chassis value must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    # Optional input for number of simulations, default to 100000 if not provided
    num_trials_input = input("Enter the number of simulations to run (default is 100000): ")
    if num_trials_input.strip() == '':
        num_trials = 100000
    else:
        try:
            num_trials = int(num_trials_input)
            if num_trials <= 0:
                print("Number of simulations must be a positive integer. Defaulting to 100,000.")
                num_trials = 100000
        except ValueError:
            print("Invalid number of simulations. Defaulting to 100,000.")
            num_trials = 100000

    print("\nCalculating, please wait...")
    results = simulate_collisions(our_chassis_value, opponent_chassis_value, num_trials)

    print(f"\nWith your chassis value of {our_chassis_value} and your opponent's chassis value of {opponent_chassis_value}:")
    print(f"You have approximately a {results['win_percentage']:.2f}% chance of winning the collision.")
    print(f"You have approximately a {results['loss_percentage']:.2f}% chance of losing the collision.")
    print(f"There is approximately a {results['slip_percentage']:.2f}% chance that both armies will slip past each other without engaging.")

if __name__ == "__main__":
    main()
