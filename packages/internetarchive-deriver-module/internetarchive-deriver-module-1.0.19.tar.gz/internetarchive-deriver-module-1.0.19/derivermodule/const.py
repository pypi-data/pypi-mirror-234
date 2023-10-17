from os import environ

#: Directory of the item files within the container
PB_ITEM = environ.get('PB_ITEM', '/item')
#: Directory of the task related JSON files within the container
PB_TASK = environ.get('PB_TASK', '/task')
#: Temporary (hard disk backed) temporary directory (auto cleaned upon exit)
PB_TMP = environ.get('PB_TMP', '/tmp')
#: Temporary fast (memory backed) temporary directory (auto cleaned upon exit)
#: Limited in size, currently 1.5G
PB_FAST = environ.get('PB_FAST', '/var/tmp/fast')

# For certain collections (movies) derives will keep running regardless of the
# exit code of a program. For some unknown reasons the code itself cannot be
# changed to catch failures and continue gracefully, so it was decided that
# programs exiting with a special exit code *would* fail.
#
# The number 66 was chosen as a reference to star wars "execute order 66"
#
# You probably won't need to use this variable, as in most instances any
# non-zero exit code will cause the task to red-row.
PB_MOVIES_EXIT_CODE_ACTUALLY_FAIL = 66
