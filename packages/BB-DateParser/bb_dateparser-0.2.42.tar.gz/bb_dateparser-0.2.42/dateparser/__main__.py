import os, sys, logging
log = logging.getLogger(__name__)

if __name__ == "__main__":
    from .dateparser import DateParser

    try:
        log.set_format('debug')
        print( f"\n\x1b[1;37m  Testing DateParser.parse_date()\x1b[0m\n" )
        date_string = sys.argv[1]
        date = DateParser().parse_date( date_string )
        if not date.isValid:
            print('\x1b[1;31m  [ERROR]\x1b[0;2;37;3m Could not parse date string\x1b[0m\n')
            sys.exit(1)

        print( f"\n\x1b[1;37m  DateParser Test Result\x1b[0m" )
        print( f"\x1b[1;37m    {'Original String:':<17}\x1b[0;1;33m {date.original_string}\x1b[0m" )
        print( f"\x1b[1;37m    {'Format Code:':<17}\x1b[0;1;33m {date.formatting}\x1b[0m\n" )
        sys.exit(0)

    except IndexError:
        print('\x1b[1;31m  [ERROR]\x1b[0;2;37;3m Requires a date for testing\x1b[0m\n')
        sys.exit(1)
