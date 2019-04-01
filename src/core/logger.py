# Made by Shadow Team
# Encoding=UTF-8

import os
from time import asctime

def log(TYPE=9999, MSG="Logger called.", LOGFILE="logfile.txt", SESSION_ID=123456):
    TYPE = int(TYPE)
    line = '=' * 50
    date = asctime()
    session = "Session ID: "

    # Legacy algorithm to log...
    # boundary = os.system('echo ' + line + " >> " + LOGFILE)
    # date = os.system("date >> " + LOGFILE)

    ### Basic types ###
    # 0 == Normal message
    # 1 == Warning message
    # 2 == Error message

    ### Extended Types ###
    # 3 == Important message
    # 4 == Serious warning message
    # 5 == Fatal error message

    if TYPE == 0:
        ICO = '[INF]: '

    elif TYPE == 1:
        ICO = '[WRN]: '

    elif TYPE == 2:
        ICO = '[ERR]: '

    elif TYPE == 3:
        ICO = '[***INF***]: '

    elif TYPE == 4:
        ICO = '[***WRN***]: '

    elif TYPE == 5:
        ICO = '[***ERR***]: '

    else:
        ICO = '[**UNK**]: '

    # Old algorithm to log...
    """
    boundary
    date
    message = os.system('echo ' + ICO + MSG + " >> " + LOGFILE)
    boundary
    """

    # New algorithm to log...
    try:
        open(LOGFILE, 'r').read()
        open(LOGFILE, 'r').close()

    except FileNotFoundError:
        open(LOGFILE, 'w').write('')
        open(LOGFILE, 'w').close()

    with open(LOGFILE, 'a') as f:
        f.write(line + '\n')
        f.write(date + '\n')
        f.write(session + str(SESSION_ID) + '\n')
        f.write(ICO + MSG + '\n')
        f.write('\n')
