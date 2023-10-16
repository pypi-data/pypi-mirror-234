try:  # pragma: nocover
    import gnureadline as readline
except ImportError:  # pragma: nocover
    import readline
import sys


# Use tab for completion
readline.parse_and_bind('tab: complete')

# Only a space separates words
readline.set_completer_delims(' ')


# Readline defaults to complete with local filenames. Definitely not what we
# want.

def null_complete(text, start):  # pragma: nocover
    return None


readline.set_completer(null_complete)


def rlinput(prompt: str = "", default: str = "",
            options: list = None):  # pragma: nocover
    """
    Get input with preset default and/or tab completion of options

    Parameters:

    prompt:str - string to output before requesting input, same as in the
    input() function

    default:str - value with which to prepopulate the response, can be cleared
    with ctrl-a, ctrl-k

    options:list - list of choices for tab completion
    """

    # Clean out the options
    options = [o.strip() + " " for o in options] if options else []

    # Create the completer using the options
    def complete(text, state):
        results = [x for x in options if x.startswith(text)] + [None]
        return results[state]
    readline.set_completer(complete)

    # Insert the default when we launch
    def start():
        readline.insert_text(default)
    readline.set_startup_hook(start)

    # Actually perform the input
    try:
        value = input(prompt)
    finally:
        readline.set_startup_hook()
        readline.set_completer(null_complete)
    return value.strip()


def tryit():  # pragma: nocover
    """Quick and dirty tester function"""
    return rlinput(prompt='>',
                   options=['a-b', 'a-c', 'b-a'])


if __name__ == '__main__':
    tryit()
