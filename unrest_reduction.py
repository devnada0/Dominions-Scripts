def get_input(prompt, default):
    try:
        value = input(f"{prompt} [{default}]: ")
        return int(value) if value.strip() != "" else default
    except ValueError:
        print("Please enter a valid integer.")
        return get_input(prompt, default)

def calculate_unrest_reduction(PD, dominion, unrest, order):
    # First Reduction
    first_reduction = 1 + (PD // 10) + -(-dominion // 2)  # Ceiling division for Dominion
    # Denominator for Second Reduction
    denominator = 10 - order
    if denominator == 0:
        denominator = 1  # Avoid division by zero
    # Second Reduction
    second_reduction = unrest // denominator
    total_reduction = first_reduction + second_reduction
    return total_reduction

def main():
    print("Dominions 6 Unrest Reduction Calculator")
    print("--------------------------------------")
    PD = get_input("Enter Province Defense (PD)", 6)
    dominion = get_input("Enter Dominion", 5)
    unrest = get_input("Enter Current Unrest", 20)
    order = get_input("Enter Order Level (-5 to 5)", 0)
    unrest_increase = get_input("Enter Unrest Increase per Turn", 0)
    num_turns = get_input("Enter Number of Turns", 10)

    print("\nCalculating unrest over {} turns...\n".format(num_turns))
    for turn in range(1, num_turns + 1):
        # Unrest increases first
        unrest += unrest_increase
        print(f"Turn {turn}:")
        print(f"  Unrest before reduction: {unrest}")
        # Calculate unrest reduction
        reduction = calculate_unrest_reduction(PD, dominion, unrest, order)
        new_unrest = max(unrest - reduction, 0)
        print(f"  Unrest reduced by: {reduction}")
        print(f"  Unrest after reduction: {new_unrest}\n")
        unrest = new_unrest
        if unrest == 0 and unrest_increase == 0:
            print("Unrest has been reduced to 0.")
            break

if __name__ == "__main__":
    main()
