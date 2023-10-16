# BB-DateParser

Attempts to convert any written date into a datetime object. To make it more useful for my needs (and easier to write :P), it only works for years 1000 - 2099.

## Usage

```python

from dateparser import DateParser

parser = DateParser()
my_date = "October 1st, 1985 4:35pm"

dp = parser.parse_date( my_date )

# To view format string

print( dp.formatting )
'%B %dst, %Y %I:%M%p'

# The DateParser class holds the data object from the last result. This is
# cleared and recreated each time self.parse_date() is used. Below are the
# data created and returned in a ParsedDate object from each date parsed

# separated list of the date string
dp.alldata = ['October', ' ', '01', 'st,', ' ', '1985', ' ', '04', ':', '35', 'PM']

# list of actual date data in dictionary form { 'alldata index': str(data) }
dp.data = { 0: 'October', 2: '1', 5: '1985', 7: '4', 9: '35', 10: 'pm' }

# created datetime object from date string
dp.dateObject = datetime.datetime(1985, 1, 1, 16, 35)

# format code for datetime
dp.formatting = '%B %mst, %Y %I:%M%p'

# boolean - True only if successful in parsing the date
dp.isValid = True

# list of non date data pulled from date string
dp.separators = [' ', 'st,', ' ', ' ', ':']

# list of all possible results (is returned when 'list_all' = True)
dp.format_list = ['%B %dst, %Y %I:%M%p']

# DateParser is a subclass of DateData which is a subclass of the builtin
# dict class. Therefore, all the parsing variables are also available through
# the DateParser class.

```

### Changelog

- 0.1.0
    - Initial release

- 0.2.0
    - DateParser.parse_date() now returns a DateParser object
    - Changed logging to an external module
    - Added timestamp support
    - Updated README

- 0.2.1
    - Now returns a separate parser object instead of self

- 0.2.40
    - Parses date based on more common date formats
