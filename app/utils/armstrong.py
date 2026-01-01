"""
Armstrong number calculation utilities.
"""
from typing import List, Tuple


def is_armstrong_number(number: int) -> bool:
    """
    Check if a number is an Armstrong number.
    
    An Armstrong number is a number that is equal to the sum of its own digits
    raised to the power of the number of digits.
    
    Args:
        number: The number to check
        
    Returns:
        True if the number is an Armstrong number, False otherwise
    """
    if number < 0:
        return False
    
    # Convert number to string to get digits
    digits = str(number)
    num_digits = len(digits)
    
    # Calculate sum of digits raised to the power of number of digits
    sum_of_powers = sum(int(digit) ** num_digits for digit in digits)
    
    return sum_of_powers == number


def find_armstrong_numbers_in_range(min_num: int, max_num: int) -> List[int]:
    """
    Find all Armstrong numbers within a given range.
    
    Args:
        min_num: Minimum number in the range (inclusive)
        max_num: Maximum number in the range (inclusive)
        
    Returns:
        List of Armstrong numbers found in the range
    """
    if min_num < 0:
        min_num = 0
    if max_num < min_num:
        return []
    
    armstrong_numbers = []
    for num in range(min_num, max_num + 1):
        if is_armstrong_number(num):
            armstrong_numbers.append(num)
    
    return armstrong_numbers


def check_armstrong_with_details(number: int) -> Tuple[bool, dict]:
    """
    Check if a number is an Armstrong number and return calculation details.
    
    Args:
        number: The number to check
        
    Returns:
        Tuple of (is_armstrong, details_dict)
        details_dict contains:
            - is_armstrong: bool
            - number: int
            - digits: list of digits
            - num_digits: int
            - calculation: str showing the calculation
            - sum_of_powers: int
    """
    if number < 0:
        return False, {
            "is_armstrong": False,
            "number": number,
            "error": "Negative numbers cannot be Armstrong numbers"
        }
    
    digits = [int(d) for d in str(number)]
    num_digits = len(digits)
    sum_of_powers = sum(d ** num_digits for d in digits)
    is_armstrong = sum_of_powers == number
    
    # Create calculation string
    calculation_parts = [f"{d}^{num_digits}" for d in digits]
    calculation = " + ".join(calculation_parts) + f" = {sum_of_powers}"
    
    return is_armstrong, {
        "is_armstrong": is_armstrong,
        "number": number,
        "digits": digits,
        "num_digits": num_digits,
        "calculation": calculation,
        "sum_of_powers": sum_of_powers
    }
