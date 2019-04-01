class ASCII_Graphs():

    def __init__(self):
        pass

    def percent_bar(self, percent):
        if not percent:
            raise ValueError("Needs one argument: percent(int 0-100)")

        else:
            if percent < 1 or percent > 100:
                raise ValueError("Needs one argument: percent(int 0-100)")

            else:
                percent = percent // 2
                bar = '|' + ('█' * percent)
                empty = 50 - percent
                bar = bar + ' ' * empty + '|'
                return bar
