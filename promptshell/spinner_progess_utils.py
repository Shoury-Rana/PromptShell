"""
Spinner and Progress Bar Utilities for PromptShell
-------------------------------------------------

This module provides decorators for adding loading indicators to functions.
You can use different spinner styles or progress bars to give users feedback
during long-running operations.

--------------------------
Common Spinner Styles:
--------------------------
- "dots"
- "line"
- "bouncingBar"
- "moon"
- "earth"
- "clock"
- "aesthetic"
- "material"
- "weather"
- "arrow3"
- "toggle10"

Example usage:
    @spinner(spinner_type="moon", message="Loading...")
    def my_function():
        ...

--------------------------
Progress Bar Example:
--------------------------
For tasks where you know the total steps, use a progress bar.

Example usage:
    @progress_bar(total=100, description="Processing items...")
    def process_items():
        for i in range(100):
            # do work
            yield 1  # Each yield advances the bar by 1

--------------------------
How to Add More Styles:
--------------------------
- See all spinner styles: from rich.spinner import SPINNERS; print(list(SPINNERS.keys()))
- Customize messages and colors as needed.

--------------------------
"""

from rich.console import Console
from rich.progress import Progress
from rich.spinner import SPINNERS
from functools import wraps
import random


#--------SPINNER-------
def spinner(spinner_type="dots", message=" [cyan]Working..."):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            console = Console()
            chosen_spinner = (
                random.choice(list(SPINNERS.keys()))
                if spinner_type == "random"
                else spinner_type
            )
            with console.status(f"{message}", spinner=chosen_spinner):
                return func(*args, **kwargs)
        return wrapper
    return decorator

#--------PROGRESS BAR-------
def progress_bar(description="Downloading..."):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # The wrapped function must yield (downloaded, total) tuples
            with Progress() as progress:
                downloaded, total = 0, 1  # Defaults
                task = None
                for downloaded, total in func(*args, **kwargs):
                    if task is None:
                        # Create the progress bar with the real total
                        task = progress.add_task(description, total=total)
                    progress.update(task, completed=downloaded)
        return wrapper
    return decorator


# To test the progress bar
if __name__ == "__main__":
    import time

    @progress_bar(description="Simulating work...")
    def hey():
        totalSteps = 20
        print("healds;kf")
        for i in range(1, totalSteps + 1):
            print(f"test {i}")
            time.sleep(0.2)
            yield i, totalSteps
    
    hey()
