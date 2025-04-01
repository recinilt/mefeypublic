from datetime import datetime

def calculate_days_between(start_date, end_date):
    """
    Calculates the number of days between two dates.

    Args:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        int: The number of days between the two dates.
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start > end:
            raise ValueError("Start date must be earlier than end date.")

        difference = (end - start).days
        return difference
    except ValueError as e:
        print(f"Error: {e}")
        return None

# Example usage:
days_between = calculate_days_between("2024-01-17", "2024-12-27")
print(f"Number of days between: {days_between}")
