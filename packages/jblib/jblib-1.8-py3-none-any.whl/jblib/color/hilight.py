class hilight:
    """
        class hilight(string).color(highlight=True, bold=True)

        WARNING:
            This version no longer works as of Python v3.9. Use hilightV2 instead

        EXAMPLE:
            print (hilight("Hello World").red(bold=True))

            Or you could make an object:
                text = hilight("Bar")

                print ("Foo "+text.blue())

            To return the original string:
                print (text.string)
        
        COLORS:
            red
            green
            yellow
            blue
            purple
            teal
            white

        FUN FACTS:
            * This class is loosely based off the very first bit of python code I ever wrote. It was initially created while teaching myself python. 
            * This module was intentionally misspelled to shorten the keystrokes needed during use. 
    """
    def __init__(self, string):
        self.string = string


    def red(self, bold=False, highlight=False):
        """ hilight(string).red(bold=False, highlight=False) """
        attr = []

        if highlight:
            attr.append('41')
        else:
            attr.append('31')

        if bold:
            attr.append('1')

        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), self.string)


    def green(self, bold=False, highlight=False):
        """ hilight(string).green(bold=False, highlight=False) """
        attr = []

        if highlight:
            attr.append('42')
        else:
            attr.append('32')

        if bold:
            attr.append('1')

        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), self.string)


    def yellow(self, bold=False, highlight=False):
        """ hilight(string).yellow(bold=False, highlight=False) """
        attr = []

        if highlight:
            attr.append('43')
        else:
            attr.append('33')

        if bold:
            attr.append('1')

        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), self.string)


    def blue(self, bold=False, highlight=False):
        """ hilight(string).blue(bold=False, highlight=False) """
        attr = []

        if highlight:
            attr.append('44')
        else:
            attr.append('34')

        if bold:
            attr.append('1')

        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), self.string)


    def purple(self, bold=False, highlight=False):
        """ hilight(string).purple(bold=False, highlight=False) """
        attr = []

        if highlight:
            attr.append('45')
        else:
            attr.append('35')

        if bold:
            attr.append('1')

        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), self.string)


    def teal(self, bold=False, highlight=False):
        """ hilight(string).teal(bold=False, highlight=False) """
        attr = []

        if highlight:
            attr.append('46')
        else:
            attr.append('36')

        if bold:
            attr.append('1')

        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), self.string)


    def white(self, bold=False, highlight=False):
        """ hilight(string).white(bold=False, highlight=False) """
        attr = []

        if highlight:
            attr.append('47')
        else:
            attr.append('37')

        if bold:
            attr.append('1')

        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), self.string)

class hilightV2:
    """
    A class for creating colored and formatted terminal output.

    Example:
        print(hilightV2("Hello World").red(bold=True))

        Or you could make an object:
            text = hilightV2("Bar")
            print("Foo " + text.blue())

        To return the original string:
            print(text.get_text())

    Colors:
        - red
        - green
        - yellow
        - blue
        - purple
        - teal
        - white

    Fun Facts:
        - This class is loosely based on Python code I wrote while learning the language.
        - The module name is intentionally misspelled to shorten keystrokes.
    """

    def __init__(self, text):
        """
        Initialize the hilightV2 object with the input text.
        """
        self._text = text

    def _apply_format(self, color_code, bold):
        """
        Apply formatting using ANSI escape codes.
        """
        attr = [color_code]

        if bold:
            attr.append('1')

        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), self._text)

    def red(self, bold=False):
        """Format the text with red color."""
        return self._apply_format('31', bold)

    def green(self, bold=False):
        """Format the text with green color."""
        return self._apply_format('32', bold)

    def yellow(self, bold=False):
        """Format the text with yellow color."""
        return self._apply_format('33', bold)

    def blue(self, bold=False):
        """Format the text with blue color."""
        return self._apply_format('34', bold)

    def purple(self, bold=False):
        """Format the text with purple color."""
        return self._apply_format('35', bold)

    def teal(self, bold=False):
        """Format the text with teal color."""
        return self._apply_format('36', bold)

    def white(self, bold=False):
        """Format the text with white color."""
        return self._apply_format('37', bold)

    def get_text(self):
        """Return the original text."""
        return self._text
