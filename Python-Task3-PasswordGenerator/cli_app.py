"""
CLI Application for Random Password Generator (Beginner Tier)
Interactive command-line interface with input validation and generation loop.
"""

import sys
import generator_logic

def prompt_bool(question: str, default: bool = True) -> bool:
    """Helper to prompt user for yes/no choice."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        choice = input(question + suffix).strip().lower()
        if not choice:
            return default
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        print("Invalid input. Please enter 'y' or 'n'.")


def prompt_int(question: str, min_val: int = 8) -> int:
    """Helper to prompt user for password length with validation."""
    while True:
        try:
            val_str = input(question).strip()
            val = int(val_str)
            if val < min_val:
                print(f"❌ Input Validation Error: Length must be at least {min_val} characters.")
                continue
            return val
        except ValueError:
            print("❌ Input Validation Error: Please enter a valid integer number.")


def run_cli():
    print("==================================================")
    print("  🔐 RANDOM PASSWORD GENERATOR (CLI Edition)")
    print("  Cryptographically Secure (Python secrets module)")
    print("==================================================\n")

    while True:
        print("--- Configure Password Requirements ---")
        length = prompt_int("Enter desired password length (minimum 8): ", min_val=8)

        print("\nSelect character types to include (at least 2 required):")
        use_upper = prompt_bool("Include Uppercase letters (A-Z)?", default=True)
        use_lower = prompt_bool("Include Lowercase letters (a-z)?", default=True)
        use_digits = prompt_bool("Include Numbers (0-9)?", default=True)
        use_symbols = prompt_bool("Include Symbols (!@#$%...)?", default=True)
        exclude_ambiguous = prompt_bool("Exclude Ambiguous characters (0, O, l, 1, I, |)?", default=False)

        # Generate password
        success, result = generator_logic.generate_password(
            length=length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
            use_symbols=use_symbols,
            exclude_ambiguous=exclude_ambiguous
        )

        if not success:
            print(f"\n❌ ERROR: {result}\n")
        else:
            strength_info = generator_logic.calculate_strength(
                result, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous
            )
            print("\n" + "=" * 50)
            print(f"  🔑 GENERATED PASSWORD:  {result}")
            print(f"  📊 STRENGTH LEVEL:     {strength_info['label']}")
            print(f"  🧮 BIT ENTROPY:         {strength_info['entropy']} bits")
            print("=" * 50 + "\n")

        if not prompt_bool("Would you like to generate another password?", default=True):
            print("\nThank you for using Random Password Generator! Goodbye 👋")
            break
        print("\n")


if __name__ == "__main__":
    run_cli()
