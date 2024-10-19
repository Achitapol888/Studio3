from django.test import TestCase

from datetime import datetime
# Define the dates
receiver_date_limit = datetime(2024, 12, 28)
giver_date_limit = datetime(2024, 10, 24)      

# Calculate the difference
date_difference = (receiver_date_limit - giver_date_limit).days

print(f"Date Difference: {date_difference} days")

