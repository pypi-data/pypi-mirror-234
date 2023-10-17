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
    text = "\r{3}: {0} {1}%  {2}".format("█" * block + "▬" * (barLength - block), round(progress * 100), status, text_field)
    print(text, end='\r')

def colored_progress_bar(progress, barLength=50, text_field="Progress"):
    """
    Displays or updates a console progress bar with a gradient effect along the '▬' characters.

    Parameters:
    - progress: A float between 0 and 1.
    - barLength: Length of the progress bar in characters.
    - text_field: Text to display before the progress bar.
    """
    def interpolate_color(color1, color2, t):
        """
        Interpolate between two colors based on a parameter t.
        """
        colors = {
            'green': (0, 255, 0),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'white': (255, 255, 255),
            'purple': (128, 0, 128),
            'cyan': (0, 255, 255),
        }

        r1, g1, b1 = colors[color1]
        r2, g2, b2 = colors[color2]
        r = int(r1 + t * (r2 - r1))
        g = int(g1 + t * (g2 - g1))
        b = int(b1 + t * (b2 - b1))
        return f'\033[38;2;{r};{g};{b}m'

    colors = ['red', 'yellow', 'green']
    num_colors = len(colors)

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

    text = text_field + ": "
    for i in range(barLength):
        char_progress = i / barLength
        color_idx1 = int(char_progress * num_colors)
        color_idx2 = color_idx1 + 1 if color_idx1 < num_colors - 1 else num_colors - 1
        t = (char_progress * num_colors) - color_idx1
        char_color1 = colors[color_idx1]
        char_color2 = colors[color_idx2]
        char_color = interpolate_color(char_color1, char_color2, t)
        if char_progress <= progress:
            text += char_color + '▬'
        else:
            text += ' '
    text += ' {:.0f}% {}'.format(progress * 100, status)
    sys.stdout.write(text + '\033[0m')
    sys.stdout.flush()