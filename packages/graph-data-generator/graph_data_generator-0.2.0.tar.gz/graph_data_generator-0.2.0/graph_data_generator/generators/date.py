from datetime import timedelta, datetime
import random

# Do not change function name or arguments
def generate(args: list[any]):
    # oldest ISO datetime
    min = args[0]
    # most recent ISO datetime
    max = args[1]
    # Convert values to datetime
    if isinstance(min, str):
        min = datetime.fromisoformat(min)
    if isinstance(max, str):
        max = datetime.fromisoformat(max)
        
    # Alt method
    # Generate random timedelta between min and max      
    # delta = timedelta(random.randint((max - min).days + 1))
    # # Add timedelta to min to get random datetime between min and max
    # random_date = min + delta
    # return random_date.isoformat()

    # Alt method
    between = max - min
    days = between.days
    random.seed(a=None)
    random_days = random.randrange(days)
    result = min + timedelta(days=random_days)
    return result