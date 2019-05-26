# -*- coding: utf-8 -*-

import sys

from core import simplelib

class Printer:
    """
    Print an object to the screen using number of methods..
    """

    def __init__(self):
        """
        def __init__():
            Initialization method of Printer() class.
        """

        pass

    def print_with_status(self, obj, status=0):
        """
        def print():
            Print <obj> with status number <status>.

            :param obj: Object to print.
            :type object:

            :param status: Status number.
            :type int:
                0 = Normal;
                1 = Warning;
                2 = Error
        """

        if status == 0:
            print('{2}[{0}+{2}]{1}'.format(simplelib.CG, simplelib.END, simplelib.CGR),
                    simplelib.CG, obj, simplelib.END)
            return None

        elif status == 1:
            print('{2}[{0}!{2}]{1}'.format(simplelib.CY, simplelib.END, simplelib.CGR),
                    simplelib.CY, obj, simplelib.END)
            return None

        elif status == 2:
            print('{2}[{0}E{2}]{1}'.format(simplelib.CR, simplelib.END, simplelib.CGR),
                    simplelib.CR, obj, simplelib.END)
            return None

        else:
            raise exceptions.InvalidParameterError("Unknown status mode!")

    def print_and_flush(self, obj):
        """
        def print_and_flush():
            Print <obj> and then flush.
        """

        sys.stdout.write(obj)
        sys.stdout.flush()
        return None

    def printt(self, obj="", mode=0, temp_objs=[]):
        """
        def print():
            Print <obj> in a number of ways.

            :param obj: Object to print.
            :type str:

            :param mode: How <obj> will be treated.
            :type int:
                0 = Normal print using print function.
                1 = Append <obj> to temporary list.
                2 = Reset the temporary list.
        """

        if mode == 0:
            print(obj)
            return temp_objs

        elif mode == 1:
            temp_objs.append(obj)
            return temp_objs

        elif mode == 2:
            temp_objs = []
            return temp_objs

        else:
            raise exceptions.InvalidParameterError("Mode must be between 0 ~ 2!")
