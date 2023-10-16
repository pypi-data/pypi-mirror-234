import sys, logging, atexit
from logging import Manager, Logger, Formatter
from re import match
from .COLORS import *

class CustomFormatter(Formatter):
    """
    Custom Formatter # Color logging output with ansi or html

        mode = 'console'
                Colors text using ansi escapes to help with reading logs being
                sent to stdout in the terminal

               'html'
                Uses html format to color logs to send to an html file or gui
                program that supports html formatting

               'file'
                No escapes inserted for logging plaintext to a file

        A lot of information on colored logging here:
     - https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

        One of my sources for the original credited the site below:
     - adapted from https://stackoverflow.com/a/56944256/3638629
    """

    def __init__(self, mode='console'):

        super().__init__()

        _time   = C_gr()           # time
        _num    = C_W()            # lineno
        _debug  = C_Gr()           # debug    ##
        _infoo  = C_C()            # info     ##
        _warnn  = C_Y()            # warning  ##
        _error  = C_O()            # error    ##                                  # time     = #aec2b1
        _critt  = C_R()            # critical ##                                  # message  = #5c675e
        _msg    = C_gri()          # msg                                          # debug    = #3b4442
        _res    = C__()            # reset                                        # info     = #2b3b4f
        __      = f"{_num}.{_res}" # white dot                                    # warning  = #8d891c
        _time_  = '%(asctime)s'    # TIMESTAMP                                    # error    = #4f1b1b
        _class_ = __name__         # CLASS                                        #    txt   = #cf6d6d
        _mod_   = '%(module)s'     # MODULE                                       # critical = #fc0202
        _num_   = '-%(lineno)s-'   # LINE NO                                      #    txt   = #a33e3e

        __debug    = f"{_time} {_time_}{_num}"+f" {_num_ : ^14}{_debug}{_mod_}{__}{_debug}"+"%(funcName)s"+f"{_debug}"+"%(levelname)9s"+f":{_msg} "+"%(message)s"+f"{_res}"
        __info     = f"{_time} {_time_}{_num}"+f" {_num_ : ^14}{_infoo}{_mod_}{__}{_infoo}"+"%(funcName)s"+f"{_infoo}"+"%(levelname)9s"+f":{_msg} "+"%(message)s"+f"{_res}"
        __warning  = f"{_time} {_time_}{_num}"+f" {_num_ : ^14}{_warnn}{_mod_}{__}{_warnn}"+"%(funcName)s"+f"{_warnn}"+"%(levelname)9s"+f":{_msg} "+"%(message)s"+f"{_res}"
        __error    = f"{_time} {_time_}{_num}"+f" {_num_ : ^14}{_error}{_mod_}{__}{_error}"+"%(funcName)s"+f"{_error}"+"%(levelname)9s"+f":{_num} "+"%(message)s"+f"{_res}"
        __critical = f"{_time} {_time_}{_num}"+f" {_num_ : ^14}{_critt}{_mod_}{__}{_critt}"+"%(funcName)s"+f"{_critt}"+"%(levelname)9s"+f":{_num} "+"%(message)s"+f"{_res}"
        self.__crit = __critical

        FORMATS = { 'console': { logging.DEBUG    : __debug,
                                 logging.INFO     : __info,
                                 logging.WARNING  : __warning,
                                 logging.ERROR    : __error,
                                 logging.CRITICAL : __critical },

                    'file'   : { logging.DEBUG    : " %(asctime)s"+f" {_num_ : ^14}"+"%(name)s.%(module)s.%(funcName)s %(levelname)8s: %(message)s",
                                 logging.INFO     : " %(asctime)s"+f" {_num_ : ^14}"+"%(name)s.%(module)s.%(funcName)s %(levelname)8s: %(message)s",
                                 logging.WARNING  : " %(asctime)s"+f" {_num_ : ^14}"+"%(name)s.%(module)s.%(funcName)s %(levelname)8s: %(message)s",
                                 logging.ERROR    : " %(asctime)s"+f" {_num_ : ^14}"+"%(name)s.%(module)s.%(funcName)s %(levelname)8s: %(message)s",
                                 logging.CRITICAL : " %(asctime)s"+f" {_num_ : ^14}"+"%(name)s.%(module)s.%(funcName)s %(levelname)8s: %(message)s" },

                    'html'   : { logging.DEBUG    : ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                                              "<span style=\"color: #474f48;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                                              "<b>[ %(lineno)d ]</b>", "<span style=\"color: #474f48;\"> %(levelname)s: </span>",
                                                              "<span style=\"color: #5c675e; font-style: italic;\">%(message)s</span></p>" ]),
                                 logging.INFO     : ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                                              "<span style=\"color: #2b3b4f;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                                              "<b>[ %(lineno)d ]</b>", "<span style=\"color: #2b3b4f;\"> %(levelname)s: </span>",
                                                              "<span style=\"color: #5c675e; font-style: italic;\">%(message)s</span></p>" ]),
                                 logging.WARNING  : ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                                              "<span style=\"color: #8d891c;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                                              "<b>[ %(lineno)d ]</b>", "<span style=\"color: #8d891c;\"> %(levelname)s: </span>",
                                                              "<span style=\"color: #5c675e; font-style: italic;\">%(message)s</span></p>" ]),
                                 logging.ERROR    : ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                                              "<span style=\"color: #4f1b1b;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                                              "<b>[ %(lineno)d ]</b>", "<span style=\"color: #4f1b1b;\"> %(levelname)s: </span>",
                                                              "<span style=\"color: #cf6d6d; font-style: italic;\">%(message)s</span></p>" ]),
                                 logging.CRITICAL : ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                                              "<span style=\"color: #fc0202;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                                              "<b>[ %(lineno)d ]</b>", "<span style=\"color: #fc0202;\"> %(levelname)s: </span>",
                                                              "<span style=\"color: #a33e3e; font-style: italic;\">%(message)s</span></p>" ]) } }

        self.FORMAT = FORMATS[mode]
        self.mode = mode

    def formatException(self, exc_info):
        if self.mode == 'console':
            return self.__crit + f'\n        {C_R()}> {C__()}' + traceback.print_exception().replace('\n', f'\n        {C_R()}> {C__()}')
        elif self.mode == 'html':
            return ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                             "<span style=\"color: #fc0202;\"> %(name)s>%(module)s.%(funcName)s </span>",
                             "<b>[ %(lineno)d ]</b>", "<span style=\"color: #fc0202;\"> %(levelname)s: </span>",
                             "<code>%(message)s</code></p>" ])

    def format(self, record):
        log_fmt = self.FORMAT.get(record.levelno)
        if self.mode == 'console':
            formatter = logging.Formatter(log_fmt, '[%R:%S]')
        elif self.mode == 'html' or self.mode == 'file':
            formatter = logging.Formatter(log_fmt, '%a, %m/%d/%y [%R:%S]:')
        return formatter.format(record)

class CustomLogger(Logger):
    """
    Logger # Colorized logging with CustomFormatter

    """

    def __init__( self, name, level=0 ):
        """
        Initiate logger class
        """

        super().__init__( name )

        try:
            lvl = self.getEffectiveLevel()
        except:
            lvl = 0

        if lvl == 0:
            if level == 0:
                lvl = 3
            else:
                lvl = level

        self.level = self.get_level(lvl)

        hdlr = logging.StreamHandler(sys.stdout)
        hdlr.setFormatter( CustomFormatter() )
        hdlr.setLevel( self.level )

        self.addHandler( hdlr )
        self.propagate = False

        atexit.register( self.onExit )

    def set_level(self, level):
        lvl = self.get_level(level)
        self.parent.setLevel( lvl )
        self.level = lvl

    def onExit(self):
        logging.shutdown()

    @staticmethod
    def get_level(L):
        """
        Translate verbosity from level parameter
        """
        verbosity = { '0': logging.DEBUG,
                      '1': logging.DEBUG,
                      '2': logging.INFO,
                      '3': logging.WARNING,
                      '4': logging.ERROR,
                      '5': logging.CRITICAL }

        if isinstance(L, int):
            if L == 10 or L == 20 or L == 30 or L == 40 or L == 50:
                return L
            elif L >= 1 and L <= 5:
                return verbosity[str(L)]

        elif isinstance(L, str):
            l = L.lower()
            if L == '1' or L == '2' or L == '3' or L == '4' or L == '5':
                return verbosity[L]
            elif l == 'critical':
                return verbosity['5']
            elif l == 'error':
                return verbosity['4']
            elif l == 'warning':
                return verbosity['3']
            elif l == 'info':
                return verbosity['2']
            elif l == 'debug':
                return verbosity['1']

        raise ValueError(f"{L} is not a valid log level")
