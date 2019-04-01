# -*- coding: utf-8 -*-

import sys
import time


class ASCIIGraphs():
    """
    class ASCIIGraphs():
        The class for creating graphs, splashes,
        animations, and progress bars.
    """

    def __init__(self):
        """
        def __init__():
            Initialization method of ASCIIGraphs() class.
        """

        pass

    def progress_bar(self, length, description='Loading...',
            progress_bar_length=20):
        """
        def progress_bar():
            Print progress bar while waiting for a specified time.

            :param length: How long the progress bar will show up.
            :type float:
        """

        length = float(length)
        start = time.time()
        end = start + length
        iteration_counter = 0
        while True:
            iteration_counter = end - time.time()
            total_items = length
            percent = float(iteration_counter) / total_items
            spaces = ' ' * int(round(percent * progress_bar_length))
            hashes = '#' * (progress_bar_length - len(spaces))
            per = int(100 - round(percent * 100))
            if per > 100:
                per = 100

            sys.stdout.write("\r{0} [{1}] {2}%".format(description,
                hashes + spaces, per))
            sys.stdout.flush()
            if int(100 - round(percent * 100)) >= 100:
                print('\r')
                if length > 1:
                    time.sleep(1)

                else:
                    time.sleep(length)

                break

            else:
                if length > 1:
                    time.sleep(1)

                else:
                    time.sleep(length)

                continue

    def progress_bar_manual(self, description='Loading...', iteration_counter=0,
            total_items=100, progress_bar_length=20):
        """
        def progress_bar():
            Print progress bar
            :param description: Description
            :type description: str

            :param iteration_counter: Incremental counter
            :type iteration_counter: int

            :param total_items: total number items
            :type total_items: int

            :param progress_bar_length: Progress bar length
            :type progress_bar_length: int

            :returns: void
            :rtype: void
        """

        percent = float(iteration_counter) / total_items
        hashes = '#' * int(round(percent * progress_bar_length))
        spaces = ' ' * (progress_bar_length - len(hashes))
        sys.stdout.write("\r{0} [{1}] {2}%".format(description,
            hashes + spaces, int(round(percent * 100))))
        sys.stdout.flush()
        if total_items == iteration_counter:
            print("\r")

    def animated_loading_screen(self, length,
            description='Loading...', animation='loading',
            delay=0.15):
        """
        def animated_loading_screen():
            Print an animated loading screen while waiting for a specified
            time.

            :param length: How long the loading screen will show up.
            :type float:

            :param description: Message in the loading screen.
            :type str:

            :param animation: Animation to use.
            :type str: `loading`, `swapcase`

            :param delay: Delay on each frame.
            :type float:
        """

        if animation.lower() == 'loading':
            length = float(time.time()) + float(length)
            splashes = ['-', '\\', '|', '/']
            iterator = 0
            while time.time() < length:
                sys.stdout.write("\r{0} {1}".format(description,
                    splashes[iterator]))
                sys.stdout.flush()
                iterator += 1
                if iterator > 3 or iterator < 0:
                    iterator = 0

                time.sleep(delay)

            sys.stdout.write('\r{0}{1}'.format(description, '  '))
            sys.stdout.flush()
            print('\r')

            return None

        elif animation.lower() == 'swapcase':
            length = float(time.time()) + float(length)
            characters = list(description)
            iterator = 0
            while time.time() < length:
                if characters[iterator].isupper():
                    characters[iterator] = characters[iterator].lower()

                elif characters[iterator].islower():
                    characters[iterator] = characters[iterator].upper()

                else:
                    pass

                desc = ''
                for character in characters:
                    desc += character

                sys.stdout.write("\r{0}".format(desc))
                if characters[iterator].isupper():
                    characters[iterator] = characters[iterator].lower()

                elif characters[iterator].islower():
                    characters[iterator] = characters[iterator].upper()

                else:
                    pass

                iterator += 1
                if iterator > (len(characters) - 1):
                    iterator = 0

                time.sleep(delay)

            sys.stdout.write('\r{0}{1}'.format(description, '  '))
            sys.stdout.flush()
            print('\r')

            return None

        else:
            print("[i] Unknown animation `{0}`!".format(animation))
            return None

    def animated_loading_screen_manual(self, last_load=False,
            description='Loading...', animation='loading', delay=0.15):
        """
        def animated_loading_screen_manual():
            Print an animated loading screen.

            :param last_load: Prints a \r in the screen,
                              which means the end of the loading.
            :type bool:

            :param description: Message in the loading screen.
            :type str:

            :param animation: Animation to use.
            :type str: `loading`, `swapcase`

            :param delay: Length of each animation to play.
            :type float:
        """

        if animation.lower() == 'loading':
            splashes = ['-', '\\', '|', '/']
            iterator = 0
            while not iterator >= (len(splashes) - 1):
                sys.stdout.write("\r{0} {1}".format(description,
                    splashes[iterator]))
                sys.stdout.flush()
                iterator += 1
                if iterator > 3 or iterator < 0:
                    iterator = 0

                time.sleep(delay)

            if last_load is True:
                sys.stdout.write('\r{0}{1}'.format(description, '  '))
                sys.stdout.flush()
                print('\r')
                return None

            else:
                return None

        elif animation.lower() == 'swapcase':
            characters = list(description)
            iterator = 0
            while True:
                if characters[iterator].isupper():
                    characters[iterator] = characters[iterator].lower()

                elif characters[iterator].islower():
                    characters[iterator] = characters[iterator].upper()

                else:
                    pass

                desc = ''
                for character in characters:
                    desc += character

                sys.stdout.write("\r{0}".format(desc))
                if characters[iterator].isupper():
                    characters[iterator] = characters[iterator].lower()

                elif characters[iterator].islower():
                    characters[iterator] = characters[iterator].upper()

                else:
                    pass

                iterator += 1
                if iterator > (len(characters) - 1):
                    break

                time.sleep(delay / (len(characters) - 1))

            if last_load is True:
                sys.stdout.write('\r{0}{1}'.format(description, '  '))
                sys.stdout.flush()
                print('\r')

            return None

        else:
            print("[i] Unknown animation `{0}`!".format(animation))
            return None