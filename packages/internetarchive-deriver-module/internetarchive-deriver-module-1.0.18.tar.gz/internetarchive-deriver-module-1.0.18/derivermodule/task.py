from json import load, dump

from os.path import join
from os import environ

from .const import PB_TASK

def get_task_info():
    """
    Parses the /task/task.json file and returns the parsed information as native
    python dictionary.

    Returns:

    * Task arguments (``dict``)
    """
    fp = open(join(PB_TASK, 'task.json'))
    data = load(fp)
    fp.close()
    return data


def get_petabox_info():
    """
    Parses the /task/petabox.json file and returns the parsed information as
    native python dictionary.

    Returns:

    * Petabox info (``dict``)
    """
    return load(open(join(PB_TASK, 'petabox.json')))


def write_extra_targets(extra_targets):
    """
    Create /task/extras_targets.json file based on `extra_targets`.

    Args:

    * `extra_targets`: A list of dictionaries, containing the filename as str
      in 'name', and optionally if the file is to be parsed as original in
      'mark_original', as boolean.

    Returns:

    * Nothing

    Example:

    >>> from derivermodule.files import canonical_item_filename
    >>> write_extra_targets([
    >>>     {'name': canonical_item_filename(target_file.replace('.txt', '-other.txt')),
    >>>      'mark_original': False}
    >>> ])


    """
    extra_targets_file = join(PB_TASK, 'extra_targets.json')
    fp = open(extra_targets_file, 'w+')
    dump(extra_targets, fp)
    fp.close()


def write_extra_tasks(extra_tasks):
    """
    Create /task/extra_tasks.json file based on `extra_tasks`.

    Args:

    * `extra_tasks`: A list of lists with each two items. The first item being
      the name (string) of the task, and the second item being a dictionary of
      arguments for this task.

    Returns:

    * Nothing

    Example:

    >>> write_extra_tasks([
    >>>     ['book_op.php', {'op1': 'VirusCheck'}]
    >>> ])


    """
    extra_tasks_file = join(PB_TASK, 'extra_tasks.json')
    with open(extra_tasks_file, 'w') as f:
        dump(extra_tasks, f)


def get_task_args(task_info):
    """
    Args:

    * task_info (dict): task_info as returned by get_task_info()

    Returns:

    * Tasks arguments (``dict``)
    """
    if 'task' in task_info and 'args' in task_info['task']:
        return task_info['task']['args']
    return {}


def get_task_arg_or_environ_arg(task_args, name):
    """
    Returns the value of a task argument if it is present in task_args or in
    the environment.

    The naming of task arguments is using lowercase and hypens, whereas the
    enviroment variables are upper cased and use underscores. The functions
    applies the task argument to environment variable to the `name` argument.

    So if the task argument is ``'ocr-perform-foo'``, pass that as ``name``, and
    the function will also check the environment variables for
    ``'OCR_PERFORM_FOO'``.

    Environment arguments have higher precedence over task arguments by this
    function.

    Args:

    * task_args: As returned by `get_task_args`
    * name: Custom task argument name, implementation defined.

    Returns:

    * the value of the argument, if present, and None otherwise.
    """
    environ_name = name.replace('-', '_').upper()
    if environ_name in environ:
        return environ.get(environ_name)

    if name in task_args:
        return task_args.get(name)

    return None
