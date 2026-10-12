"""
BMI Logic Module for Smart BMI Calculator
Handles BMI calculation, category classification, and input validation.
"""

def validate_inputs(user_name: str, weight_str: str, height_str: str):
    """
    Validates user input fields.

    Returns:
        (is_valid: bool, error_message_or_data: str | tuple)
    """
    # 1. Empty user name
    if not user_name or not user_name.strip():
        return False, "Please enter your name."

    # 2. Empty weight
    if not weight_str or not weight_str.strip():
        return False, "Please enter your weight in kg."

    # 3. Empty height
    if not height_str or not height_str.strip():
        return False, "Please enter your height in meters."

    # 4. Non-numeric weight
    try:
        weight = float(weight_str.strip())
    except ValueError:
        return False, "Please enter a valid numeric weight."

    # 5. Non-numeric height
    try:
        height = float(height_str.strip())
    except ValueError:
        return False, "Please enter a valid numeric height."

    # 6. Negative or zero weight
    if weight <= 0:
        return False, "Weight must be greater than zero."

    # 7. Negative or zero height
    if height <= 0:
        return False, "Height must be greater than zero."

    # Realistic range checks
    if height > 3.0:
        return False, "Height seems unrealistically high. Please enter height in meters (e.g., 1.75)."
    if weight > 500:
        return False, "Weight seems unrealistically high. Please enter weight in kilograms (e.g., 70)."

    return True, (user_name.strip(), weight, height)


def calculate_bmi(weight: float, height: float) -> float:
    """
    Calculates BMI using formula: BMI = weight / (height^2)
    Returns BMI rounded to 2 decimal places.
    """
    bmi = weight / (height ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float):
    """
    Classifies BMI value into official categories with corresponding color scheme.

    Categories:
    - Underweight: BMI < 18.5
    - Normal: 18.5 <= BMI <= 24.9
    - Overweight: 25.0 <= BMI <= 29.9
    - Obese: BMI >= 30.0

    Returns:
        tuple: (category_name, hex_color_bg, hex_color_fg)
    """
    if bmi < 18.5:
        # Underweight -> Informational Blue
        return "Underweight", "#3182CE", "#FFFFFF"
    elif bmi < 25.0:
        # Normal -> Green
        return "Normal", "#38A169", "#FFFFFF"
    elif bmi < 30.0:
        # Overweight -> Warning/Orange
        return "Overweight", "#DD6B20", "#FFFFFF"
    else:
        # Obese -> Red
        return "Obese", "#E53E3E", "#FFFFFF"
