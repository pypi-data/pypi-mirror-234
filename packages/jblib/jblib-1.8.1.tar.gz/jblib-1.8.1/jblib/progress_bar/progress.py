import sys

def progress_bar(progress, barLength=50, text_field="Progress"):
    """
    Displays or updates a console progress bar.

    Accepts a float between 0 and 1. Any int will be converted to a float.
    A value under 0 represents a 'halt'.
    A value at 1 or bigger represents 100%.

    Parameters:
    - progress: A float between 0 and 1.
    - barLength: Length of the progress bar in characters.
    - text_field: Text to display before the progress bar.
    """
    status = " \r"
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "ERROR: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    text = "\r{3}: [{0}] {1}%  {2}".format("#" * block + "-" * (barLength - block), round(progress * 100), status, text_field)
    print(text, end='\r')

def colored_progress_bar(progress, barLength=50, text_field="Progress"):
    """
    Displays or updates a console progress bar with color changing when it's greater than 99%.

    Parameters:
    - progress: A float between 0 and 1.
    - barLength: Length of the progress bar in characters.
    - text_field: Text to display before the progress bar.
    """
    def set_color_code(color):
        colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'white': '\033[97m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
        }
        return colors.get(color, '\033[0m')

    if progress >= 0.94:
        color = 'green'
    elif progress >= 0.4:
        color = 'yellow'
    else:
        color = 'red'
    color_code = set_color_code(color)

    status = " \r"
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "ERROR: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    text = f"{text_field}: {color_code}[{'#'*block + '-'*(barLength-block)}] {round(progress*100)}% {status}\033[0m"
    sys.stdout.write(text)
    sys.stdout.flush()