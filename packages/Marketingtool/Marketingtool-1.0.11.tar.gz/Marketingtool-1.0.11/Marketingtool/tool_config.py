action=''
inputfile=''
outputfile=''
srtfile=''
sourcelang=''
targetlang=''
insertvideo=''
# Set the debug level of the application. Use the string representation
# instead of the numbers. High numbers will output less, lower numbers more.
# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0
log_level = 'INFO'

# Log format string
log_format = '[%(threadName)s] - %(asctime)s - %(name)s ' \
    '- %(levelname)s - %(message)s - {%(pathname)s:%(lineno)d}'

# Logfile
log_file = 'maeketing.log'