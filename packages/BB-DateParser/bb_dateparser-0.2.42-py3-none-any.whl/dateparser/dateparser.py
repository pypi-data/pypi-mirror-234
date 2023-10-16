import sys, os, logging, re
from datetime import datetime as dt
from itertools import ( product,
                        permutations as perms )

log = logging.getLogger(__name__)

class ParsedDate:
    """
    DateParser object
    """
    separators      = []
    original_string = ''
    data            = {}
    alldata         = {}
    formatting      = ''
    format_list     = []
    dateObject      = None
    isValid         = False

    def __init__(self):
        self.created = dt.now().timestamp()

class DateData(dict):
    """
    DateParser data class
    """
    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        self.update(*args, **kwargs)

        self['months'] = { 'long' : ( ( 'January',   '%B' ),
                                      ( 'February',  '%B' ),
                                      ( 'March',     '%B' ),
                                      ( 'April',     '%B' ),
                                      ( 'May',       '%B' ),
                                      ( 'June',      '%B' ),
                                      ( 'July',      '%B' ),
                                      ( 'August',    '%B' ),
                                      ( 'September', '%B' ),
                                      ( 'October',   '%B' ),
                                      ( 'November',  '%B' ),
                                      ( 'December',  '%B' )),
                           'short': ( ( 'Jan',  '%b' ),
                                      ( 'Feb',  '%b' ),
                                      ( 'Mar',  '%b' ),
                                      ( 'Apr',  '%b' ),
                                      ( 'May',  '%b' ),
                                      ( 'Jun',  '%b' ),
                                      ( 'Jul',  '%b' ),
                                      ( 'Aug',  '%b' ),
                                      ( 'Sep',  '%b' ),
                                      ( 'Oct',  '%b' ),
                                      ( 'Nov',  '%b' ),
                                      ( 'Dec',  '%b' ))}

        self['days'] = { 'long' : ( ( 'Monday',    '%A' ),
                                    ( 'Tuesday',   '%A' ),
                                    ( 'Wednesday', '%A' ),
                                    ( 'Thursday',  '%A' ),
                                    ( 'Friday',    '%A' ),
                                    ( 'Saturday',  '%A' ),
                                    ( 'Sunday',    '%A' )),
                         'short': ( ( 'Mon',  '%a' ),
                                    ( 'Tues', '%a' ),
                                    ( 'Wed',  '%a' ),
                                    ( 'Thur', '%a' ),
                                    ( 'Fri',  '%a' ),
                                    ( 'Sat',  '%a' ),
                                    ( 'Sun',  '%a' ))}

        cardinal = { 'zero'     : '0',
                     'ten'      : '10',
                     'eleven'   : '11',
                     'twelve'   : '12',
                     'thirteen' : '13',
                     'fourteen' : '14',
                     'fifteen'  : '15',
                     'sixteen'  : '16',
                     'seventeen': '17',
                     'eighteen' : '18',
                     'nineteen' : '19' }

        for db, N in ( ( 'twenty', ( '20', '2' )),
                       ( 'thirty', ( '30', '3' )),
                       ( 'forty',  ( '40', '4' )),
                       ( 'fifty',  ( '50', '5' ))):

            for num, n  in (( 'one',   '1' ),
                            ( 'two',   '2' ),
                            ( 'three', '3' ),
                            ( 'four',  '4' ),
                            ( 'five',  '5' ),
                            ( 'six',   '6' ),
                            ( 'seven', '7' ),
                            ( 'eight', '8' ),
                            ( 'nine',  '9' )):

                cardinal[num] = n
                cardinal[ db + '.*' + num ] = N[1] + n

            cardinal[db] = N[0]

        ordinal = { 'first' : '1',
                    'second': '2',
                    'third' : '3' }
        ordTMP = {}

        for k, v in cardinal.items():
            skip = False
            if k in ( 'zero', 'one', 'two', 'three' ):
                continue

            elif k in ( 'twenty', 'thirty', 'forty', 'fifty' ):
                ordinal[ k[:-1] + 'ieth' ] = v[0]
                continue

            elif re.match( '.*ve$', k ):
                word = k[:-2] + 'fth'

            elif re.match( '.*t$', k ):
                word = k + 'h'

            elif re.match( '.*e$', k ):
                word = k[:-1] + 'th'

            else:
                word = k + 'th'

            ordinal[word] = v

        self['spelled'] = { 'cardinal': cardinal,
                            'ordinal' : ordinal }

        self['format codes'] = { 'single': ( ( '^[MondayTuesWhrFiSt]{6,9}$', '%A' ),
                                             ( '^[MonTuesWdhrFiSat]{3}$', '%a' ),
                                             ( '^[JanuryFebMchApilgstSmOoNv]{4,9}$', '%B' ),
                                             ( '^[JanFebMrApyulgSOctNovD]{3}$', '%b' ),
                                             ( '^(0[0-9]{1}|1[0-2]{1})[AaPp]{1}[Mm]{1}$', '%I%p' ),
                                             ( '^([0-2]{1}[0-9]{2}|3[0-6]{1}[0-9]{1})$', '%j' ),
                                             ( '^\n$', '%n' ),
                                             ( '^[AaPp]{1}[Mm]{1}$', '%p' ),
                                             ( '^\t$', '%t' ),
                                             ( '^[+\-]{1}([01]{1}[0-9]{1}|2[0-4]{1})[0-5]{1}[0-9]{1}$', '%z' )),
                                 'full'  : ( ( '^[MonTuesWdhrFiSat]{3}( )+[JanFebMrApyulgSOctNovD]{3}( )+([1-9]{1}|[12]{1}[0-9]{1}|3[01]{1})( )+([01]{1}[0-9]{1}|2[0-4]{1}):[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}( )+(1[0-9]{3}|20[0-9]{2})$', '%c' ),
                                             ( '^(0[1-9]{1}|1[0-2]{1})/(0[1-9]{1}|[1-2]{1}[0-9]{1}|3[01]{1})/[12]{1}[0-9]{1}$', '%D' ),
                                             ( '^(1[0-9]{3}|20[0-9]{2})-(0?[1-9]{1}|1[0-2]{1})-(0?[1-9]{1}|1[0-2]{1})-(0?[1-9]{1}|[12]{1}[0-9]{1}|3[01]{1})$', '%F' ),
                                             ( '^(0[0-9]{1}|1[0-2]{1}):[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}( ){1}(AM|PM){1}$', '%r' ),
                                             ( '^([01]{1}[0-9]{1}|2[0-3]{1}):[0-5]{1}[0-9]{1}$', '%R' ),
                                             ( '^[0-9]+$', '%s' ),
                                             ( '^([01]{1}[0-9]{1}|2[0-3]{1}):[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$', '%T' ),
                                             ( '^(0[1-9]{1}|1[0-2]{1})/([0-2]{1}[0-9]{1}|3[01]{1})/[0-9]{2}$', '%x' ),
                                             ( '^([01]{1}[0-9]{1}|2[0-3]{1}):[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$', '%X' )),
                                 'nums'  : ( ( '^([1-9]{1}|0[1-9]{1}|[12]{1}[0-9]{1}|3[01]{1})$', '%d' ),   # 0
                                             ( '^([01]{1}[0-9]{1}|2[0-3]{1})$', '%H' ),                     # 1
                                             ( '^([1-9]{1}|0[1-9]{1}|1[0-2]{1})$', '%m' ),                  # 2
                                             ( '^[0-5]{1}[0-9]{1}$', '%M' ),                                # 3
                                             ( '^[0-9]{6}$', '%f' ),                                        # 4
                                             ( '^[0-5]{1}[0-9]{1}$', '%S' ),                                # 5
                                             ( '^(1[0-9]{3}|20[0-9]{2})$', '%Y' ),                          # 6
                                             ( '^[0-9]{2}$', '%y' ),                                        # 7
                                             ( '^(0[0-9]{1}|1[0-2]{1})$', '%I' ))}                          # 8

        split_sep = '(?:([0-9]+)|( )|(AM|am|PM|pm)'

        for i in ( 'long', 'short' ):
            for d in self['days'][i]:
                split_sep = split_sep + '|(' + d[0] + ')'

            for m in self['months'][i]:
                split_sep = split_sep + '|(' + m[0] + ')'

        for i in self['spelled']:
            for t in self['spelled'][i]:
                split_sep = split_sep + '|(' + t + ')'

        self['split sep'] = split_sep + ')'
        self['match sep'] = self['split sep'].replace( '(?:', '^(' ).replace( '|( )', '') + '$'

class DateParser(DateData):
    """
    Figure out date formats
      - only years (1000 - 2099)
    """

    def __init__(self):
        self.date = ParsedDate()
        super().__init__()

    def date_split(self, DATE):
        """
        Returns a 2 part tuple of lists
            ( [ date list ], [ full list with date list objects ] )
        """
        split_date = list(filter( None, re.split( self['split sep'], DATE, flags = re.IGNORECASE )))
        log.debug(f"Split date = {str(split_date)}")

        c = 0
        for i in split_date:
            if re.match( self['match sep'], str(i), flags = re.IGNORECASE ):
                self.date.data[c] = str(i)
                self.date.alldata[c] = self.date.data[c]
            else:
                self.date.alldata[c] = str(i)
                self.date.separators.append(str(i))

            c += 1

        return ( self.date.data, self.date.alldata )

    def __parse_nums(self, numstr):
        numstr = str(numstr)
        codes = self['format codes']['nums']
        log.debug(f"Attempting to decypher {numstr} into a valid date")
        formats, numlist, indexes_used = {}, [], []
        return_list = []

        for i in numstr:
            numlist.append(i)

        def l_year(str_):
            if re.match( codes[6][0], str_ ):
                return codes[6][1]

            return None

        def s_year(str_):
            if re.match( codes[7][0], str_ ):
                return codes[7][1]

            return None

        def month(str_):
            if re.match( codes[2][0], str_ ):
                return codes[2][1]

            return None

        def day(str_):
            if re.match( codes[0][0], str_ ):
                return codes[0][1]

            return None

        def hour24(str_):
            if re.match( codes[1][0], str_ ):
                return codes[1][1]

            return None

        def hour12(str_):
            if re.match( codes[8][0], str_ ):
                return codes[8][1]

            return None

        def mins(str_):
            if re.match( codes[3][0], str_ ):
                return codes[3][1]

            return None

        def secs(str_):
            if re.match( codes[5][0], str_ ):
                return codes[5][1]

            return None

        def msecs(str_):
            if re.match( codes[4][0], str_ ):
                return codes[4][1]

            return None

        code_list = { 'Lyear' : ( l_year, 4 ),
                      'Syear' : ( s_year, 2 ),
                      'month' : ( month, 2 ),
                      'day'   : ( day, 2 ),
                      'hour24': ( hour24, 2 ),
                      'hour12': ( hour12, 2 ),
                      'mins'  : ( mins, 2 ),
                      'secs'  : ( secs, 2 ),
                      'msecs' : ( msecs, 6 ) }

        dates = list(perms([ code_list['Lyear'],
                             code_list['month'],
                             code_list['day'] ]))

        dates2 = list(perms([ code_list['Syear'],
                              code_list['month'],
                              code_list['day'] ]))

        fulltime24 = ( code_list['hour24'],
                       code_list['mins'],
                       code_list['secs'],
                       code_list['msecs'] )

        fulltime12 = ( code_list['hour12'],
                       code_list['mins'],
                       code_list['secs'],
                       code_list['msecs'] )

        time12  = tuple(fulltime12[:3])
        time24  = tuple(fulltime24[:3])

        stime12 = tuple(fulltime12[:2])
        stime24 = tuple(fulltime24[:2])

        guesses = []

        if len(numlist) == 20:
            for i in dates:
                guesses.append( fulltime12 + i )

            for i in dates:
                guesses.append( i + fulltime12 )

            for i in dates:
                guesses.append( fulltime24 + i )

            for i in dates:
                guesses.append( i + fulltime24 )

        elif len(numlist) == 18:
            for i in dates2:
                guesses.append( fulltime12 + i )

            for i in dates2:
                guesses.append( i + fulltime12 )

            for i in dates2:
                guesses.append( fulltime24 + i )

            for i in dates2:
                guesses.append( i + fulltime24 )

        elif len(numlist) == 14:
            for i in dates:
                guesses.append( time12 + i )
                guesses.append( i + time12 )
                guesses.append( time24 + i )
                guesses.append( i + time24 )

        elif len(numlist) == 12:
            for i in list(perms(fulltime24)) + list(perms(fulltime12)):
                guesses.append(i)

            for i in dates:
                guesses.append( stime12 + i )
                guesses.append( i + stime12 )
                guesses.append( stime24 + i )
                guesses.append( i + stime24 )

        elif len(numlist) == 8:
            guesses = dates

        elif len(numlist) == 6:
            guesses.append([ code_list['msecs'] ])
            guesses = dates

        elif len(numlist) == 4:
            guesses.append([ code_list['Lyear'] ])
            guesses.append( stime12 )
            guesses.append( stime24 )

        elif len(numlist) == 2:
            guesses = [ [ code_list['month'] ],
                        [ code_list['Syear'] ]]
                        [ code_list['day'] ],
                        [ code_list['hour24'] ],
                        [ code_list['hour12'] ],
                        [ code_list['mins'] ],
                        [ code_list['secs'] ],

        elif len(numlist) == 1:
            numlist.insert( 0, '0' )
            guesses = [ [ code_list['month'] ],
                        [ code_list['day'] ],
                        [ code_list['hour24'] ],
                        [ code_list['hour12'] ]]

        else:
            log.debug(f"No valid formatting found for {numstr}")
            return []

        for i in guesses:
            alldata = []
            guess_fmt = ''
            startnum = 0
            for c in i:
                section = ''.join( numlist[ startnum : startnum + c[1] ] )
                code = c[0](section)
                if not code:
                    break

                alldata.append(section)
                guess_fmt = guess_fmt + code
                startnum = startnum + c[1]

            if not code:
                continue

            log.debug(f"Trying format {guess_fmt} for {numstr}")
            if self.try_fmt(numstr, guess_fmt):
                return_list.append( guess_fmt )

        if not return_list:
            log.error(f"No valid formatting found for {numstr}")
            return []

        return return_list

    def parse_date(self, str_):
        """
        Attempt to find time format for strptime
            - returns format string by default
            - returns a list of all possible results if 'list_all' is True
        """

        @staticmethod
        def chk_spelled(SPL, DN):
            for S in SPL:
                if DN in SPL[S]:
                    log.debug(f"Found number {DN} - {SPL[S][DN]}")
                    return SPL[S][DN]

            return None

        self.date = ParsedDate()
        self.date.original_string = str_

        log.debug("Trying entire string with full date formats")

        for i in self['format codes']['full']:
            log.debug(f"Trying {i[0]}")
            if re.match( i[0], str_ ):
                log.debug(f"Found a match - trying {i[1]}")
                if not self.try_fmt( str_, i[1] ):
                    log.debug(f"String does not match datetime object - date is INVALID")
                    break

                log.debug(f"String matches datetime object - date is VALID")
                self.date.isValid = True
                self.date.alldata = [ str_ ]
                self.date.dateObject = dt.strptime( str_, i[1] )
                self.date.formatting = i[1]
                return self.date

        log.debug(f"Attempting to split the string and trying each individual piece of data")
        self.date_split( str_ )
        data_matches = {}

        change_data, pastnum = [], None
        for i in self.date.data:
            num = chk_spelled(self['spelled'], self.date.data[i])

            if pastnum:
                try:
                    assert num
                    change_data.append(( pastnum[0], pastnum[1] + num, i ))

                except AssertionError:
                    change_data.append(( pastnum[0], pastnum[1], None ))

                pastnum = None
                continue

            try:
                assert num
                pastnum = ( i, num )

            except AssertionError:
                pass

        for CH in change_data:
            self.date.data[ CH[0] ] = CH[1]
            self.date.alldata[ CH[0] ] = CH[1]
            if CH[2]:
                self.date.data[ CH[2] ] = ''
                self.date.alldata[ CH[2] ] = ''

        for i in self.date.data:
            DN = self.date.data[i]
            data_matches[DN] = []

            if re.match( '^[0-9]+$', DN ):
                for M in self.__parse_nums( DN ):
                    data_matches[DN].append(M)
                    log.debug(f"Found a match for {DN} - adding {M} to list of possibilities")

            else:
                for F in self['format codes']['single']:
                    if re.match( F[0], self.date.data[i], flags = re.IGNORECASE ):
                        log.debug(f"Found a match for {self.date.data[i]} - adding {F[1]} to list of possibilities")
                        data_matches[DN].append( F[1] )

        list_ = []
        for i in data_matches:
            list_.append( data_matches[i] )

        cbo = list(product( *list_ ))
        combos = []
        c = 0
        for i in cbo:
            if len(set(i)) != len(i):
                log.debug(f"Skipping {str(i)} - reduntant format codes found in string")
            elif not i:
                log.debug(f"Nothing found in cbo[{c}] - skipping...")
            else:
                combos.append(i)
            c += 1

        log.debug(f"self.date.data = {str(self.date.data)}")
        for i in combos:
            log.debug(f"Combo = {str(i)}")
            code_len = 0
            foundH = foundI = foundM = foundS = foundd = foundm = foundy = foundP = False
            for c in i:
                code_len += len(list(filter( None, c.split('%') )))
                if re.match( '.*(%H)+.*', c ):
                    foundH = True
                if re.match( '.*(%I)+.*', c ):
                    foundI = True
                if re.match( '.*(%M)+.*', c ):
                    foundM = True
                if re.match( '.*(%S)+.*', c ):
                    foundS = True
                if re.match( '.*(%d)+.*', c ):
                    foundd = True
                if re.match( '.*(%m)+.*', c ):
                    foundm = True
                if re.match( '.*(%y)+.*', c ):
                    foundy = True

            if '%H' in i or foundH:
                log.debug("'%H' found in combo")
                foundH = True
            if '%I' in i or foundI:
                log.debug("'%I' found in combo")
                foundI = True
            if '%M' in i or foundM:
                log.debug("'%M' found in combo")
                foundM = True
            if '%S' in i or foundS:
                log.debug("'%S' found in combo")
                foundS = True
            if '%d' in i or foundd:
                log.debug("'%d' found in combo")
                foundd = True
            if '%m' in i or foundm:
                log.debug("'%m' found in combo")
                foundm = True
            if '%y' in i or foundy:
                log.debug("'%y' found in combo")
                foundy = True
            if '%p' in i:
                log.debug("'%p' found in combo")
                foundP = True

            code_str = ''.join(i)
            log.debug(f"Analyzing code string - {code_str}")

            if foundH and foundI:
                log.debug(f"Skipping {str(i)} - reduntant hour codes found in string")
                continue

            if ( foundH or foundI ) and foundS and not foundM:
                log.debug(f"Skipping {str(i)} - '%H' or '%I' and '%S' found in string but no minutes")
                continue

            if foundS:
                if code_len > 2:
                    if not foundM and ( not foundH and not foundI ):
                        log.debug(f"Skipping {str(i)} - '%S' found in string but no hours or minutes")
                        continue
                    if not re.match( '.*(%H|%I)%M%S.*', code_str ):
                        log.debug(f"Skipping {str(i)} - Incorrect timestamp order")
                        continue
                if code_len == 2:
                    if not foundM:
                        log.debug(f"Skipping {str(i)} - '%S' found in string but no minutes")
                        continue
                    if not re.match( '^%M%S$', code_str ):
                        log.debug(f"Skipping {str(i)} - Incorrect timestamp order")
                        continue

            if foundM:
                if code_len > 1:
                    if not foundH and not foundI:
                        log.debug(f"Skipping {str(i)} - '%M' found in string but no hours")
                        continue
                    if not re.match( '.*(%H|%I)%M.*', code_str ):
                        log.debug(f"Skipping {str(i)} - Incorrect timestamp order")
                        continue

            if foundy and not foundd and ( not foundm and not set(['%A', '%a']) & set(i) ):
                log.debug(f"Skipping {str(i)} - '%y' found without month and day")
                continue

            if foundy and not re.match( '.*((%m|%b|%B|%d|%a|%A){1}|(%m|%b|%B|%d|%a|%A){1})%y.*', code_str ):
                log.debug(f"Skipping {str(i)} - '%y' doubtful this would be used without the month and day preceding it")
                continue

            if foundI and not foundP:
                log.debug(f"Skipping {str(i)} - no am/pm found in string, should be '%H' instead of '%I'")
                continue

            if foundP and not foundI:
                log.debug(f"Skipping {str(i)} - am/pm found in string and no '%I'")
                continue

            if re.match( '.*(%I|%H)(%m|%d|%y|%Y).*', code_str ) or re.match( '.*(%I|%M|%S)(%m|%d|%y|%Y)%p.*', code_str ):
                log.debug(f"Skipping {str(i)} - Bad order of time codes")
                continue

            count = 0
            fmt   = []
            alldata = []
            chk_str = []
            for c in range( 0, len( self.date.alldata )):
                if c in self.date.data:
                    fmt.append( str(i[count]) )
                    count += 1

                    if fmt[c] in ('%d', '%m', '%H', '%I', '%M', '%S') and re.match( '^[0-9]{1}$', str(self.date.alldata[c]) ):
                        log.debug(f"Changing date/time data to 2 digits instead of one - ({fmt[c]}) ({self.date.alldata[c]})")
                        alldata.append( '0' + str(self.date.alldata[c]) )

                    elif self.date.alldata[c].lower() in ('am,', 'pm'):
                        log.debug(f"Changing am/pm data to uppercase")
                        alldata.append( self.date.alldata[c].upper() )

                    else:
                        alldata.append( str(self.date.alldata[c]) )

                else:
                    fmt.append( str(self.date.alldata[c]) )
                    alldata.append( str(self.date.alldata[c]) )


            log.debug(f"Alldata = {str(fmt)}")

            formatting = ''.join(fmt)
            log.debug(f"Trying format - {formatting} for {''.join( alldata )}")
            if self.try_fmt( ''.join( alldata ), formatting ):
                log.debug(f"Found a working format string for '{''.join( alldata )}'! - '{formatting}'")
                DObj = dt.strptime( ''.join( alldata ), formatting )

                log.debug(f"Checking if datetime.strftime({formatting}) matches {str_}")
                if DObj.strftime( formatting ) == ''.join(alldata):
                    self.date.isValid = True

                    self.date.format_list.append(formatting)

                    self.date.alldata = alldata
                    self.date.dateObject = DObj
                    self.date.formatting = formatting
                    log.debug(f"String matches datetime object - date is VALID")
                    return self.date
                else:
                    log.debug(f"String does not match datetime object - date is INVALID")
                    self.date.isValid = False
                    if self.date.formatting:
                        continue

                    self.date.alldata = alldata
                    self.date.dateObject = DObj
                    self.date.formatting = formatting

        if not self.date.formatting:
            try:
                if re.match( '^-?[0-9]+$', str_ ):
                    log.debug("Formatting cannot be found - trying timestamp")
                    x = dt.fromtimestamp(int( str_ ))
                    self.date.dateObject = x
                    log.warning("Time is given as timestamp - formatting will be None")
                    self.date.formatting = ''
                else:
                    raise ValueError
            except ValueError:
                log.error(f"Could not parse date string '{str_}'")
            except Exception as E:
                log.exception(E)
            finally:
                return self.date

        return self.date

    # def __setVars(self):
    #     self.date.separators      = []
    #     self.date.original_string = ''
    #     self.date.data            = {}
    #     self.date.alldata         = {}
    #     self.date.formatting      = ''
    #     self.date.format_list     = []
    #     self.date.dateObject      = None
    #     self.date.isValid         = False

    @staticmethod
    def try_fmt(str_, fmt):
        try:
            x = dt.strptime( str_, fmt )
            return True
        except:
            return False
