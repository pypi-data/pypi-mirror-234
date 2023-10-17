from os import rename, stat, remove, fsync, posix_fadvise, \
        POSIX_FADV_DONTNEED, chmod, close, stat
from shutil import move
from os.path import join
from tempfile import mkstemp

from xml.etree import ElementTree as ET
from xml.dom import minidom

import hashlib, zlib

from json import dump

from subprocess import check_output, check_call, CalledProcessError, \
        DEVNULL, STDOUT
from collections import OrderedDict

import xmltodict

from .const import PB_ITEM, PB_TASK, PB_TMP


def parse_item_metadata(path):
    tree = ET.parse(path)
    root = tree.getroot()
    if root.tag != 'metadata':
        raise ValueError('No \'metadata\' in _meta.xml')
    md = {}

    for elem in root:
        if elem.text is None:
            continue
        if elem.tag in md:
            if isinstance(md[elem.tag], list):
                md[elem.tag].append(elem.text)
            else:
                md[elem.tag] = [md[elem.tag], elem.text]
        else:
            md[elem.tag] = elem.text

    return md


def load_item_metadata(identifier):
    """
    Returns the metadata of an item as a (modifiable) dictionary.

    Args:

    * identifier (``str``): Identifier of the item

    Returns:

    * item metadata (``dict``)

    Example usage::

        from derivermodule.task import get_task_info
        from derivermodule.metadata import load_item_metadata

        info = get_task_info()
        identifier = info['identifier']
        metadata = load_item_metadata(identifier)
    """
    path = open(join(PB_ITEM, '%s_meta.xml' % identifier))
    return parse_item_metadata(path)


def metadata_to_metaxml(metadata):
    meta_root = ET.Element('metadata')

    for key, value in metadata.items():
        if isinstance(value, list):
            for val in value:
                elem = ET.SubElement(meta_root, key)
                elem.text = val
        elif isinstance(value, str):
            elem = ET.SubElement(meta_root, key)
            elem.text = value
        else:
            raise ValueError('Unknown value type: %s' % type(value))

    # TODO: I think we can get rid of minidom here
    result = minidom.parseString(
        ET.tostring(meta_root, encoding='UTF-8')
    ).toprettyxml(
        encoding='UTF-8',
        indent=' ' * 2
    )

    xml = check_output(['xmllint', '--format', '-'], input=result)

    return xml.decode('utf-8')


def write_item_metadata(identifier, metadata):
    """
    Write the (changed) item metadata dictionary to disk.
    This is required if changes made to the `metadata` are to persist.
    The `metadata` should be loaded using `load_item_metadata`.

    Args:

    * identifier (``str``): Identifier of the item
    * metadata (``dict``): Metadata, loaded by `load_item_metadata` and
                           potentially modified.

    Returns:

    * Nothing
    """
    metaxml = metadata_to_metaxml(metadata)
    fp, tmp_path = mkstemp(suffix='.xml', dir=PB_TMP, text=True)
    close(fp)

    # We write the XML to a temporary file, flush it, sync it to disk, and
    # finally tell Linux to drop it from the cache, to prevent the disk from
    # silently corrupted the file before xmllint performs the final validation.
    # Alternatively, we could write it to disk and read it from disk with
    # O_DIRECT, and pass that to xmllint's stdin.
    fp = open(tmp_path, 'w+')
    fp.write(metaxml)
    fp.flush()
    fsync(fp.fileno())
    posix_fadvise(fp.fileno(), 0, 0, POSIX_FADV_DONTNEED)
    fp.close()

    try:
        check_call(['xmllint', '--format', tmp_path], stdout=DEVNULL, stderr=STDOUT)
    except CalledProcessError:
        remove(tmp_path)
        raise

    meta_xml_path = join(PB_ITEM, '%s_meta.xml' % identifier)
    st = stat(meta_xml_path)
    chmod(tmp_path, st.st_mode)
    move(tmp_path, meta_xml_path)


def load_files_metadata(identifier):
    """
    Returns the file-level metadata of an item as an opaque (not to be directly
    modified) object. Use `lookup_file_metadata` to get a reference to the
    metadata of a specific file.

    There is no way to save changes made to this structure, so users have to
    treat the result as read-only.

    Args:

    * identifier (``str``): Identifier of the item

    Returns:

    * object containing the file-level metadata of an item.
    """
    path = open(join(PB_ITEM, '%s_files.xml' % identifier))
    data = path.read()
    path.close()
    return xmltodict.parse(data, strip_whitespace=False)


def write_files_metadata(files_metadata):
    """
    Write additional metadata for a set of files.
    This function cannot add metadata to arbitrary files, only to the target
    file and any extra targets specified in
    ``derivermodule.task.write_extra_targets``. It also cannot delete metadata
    values, nor does it have to: any files that are created by this module will
    have no metadata associated with it, so there will be nothing to delete.

    Metadata values can be of type ``str`` or ``list (of str)``.

    Args:

    * files_metadata: a dictionary where the key is a canonical item filename
                      (see ``derivermodule.files.canonical_item_filename``)
                      and the value is a key-value metadata pairs.

    Returns:

    * Nothing

    Example:

    >>> from derivermodule.files import canonical_item_filename
    >>> md = {'foo_module_version': '0.0.1'}
    >>> write_files_metadata({canonical_item_filename(target_file): md})
    """
    files_metadata_file = join(PB_TASK, 'extra_metadata.json')
    fp = open(files_metadata_file, 'w+')
    dump(files_metadata, fp)
    fp.close()


## TODO: Perform a *LOT* of testing on this
#def write_files_metadata(identifier, metadata):
#    """
#    Writes the (changed) file level metadata dictionary to disk.
#    This is required if changes made to the `metadata` are to persist.
#    The `metadata` should be loaded using `load_files_metadata` and not changed
#    directly, only by calling `lookup_file_metadata` and changing the values in
#    the result of that function.
#
#    Args:
#
#    * identifier (``str``): Identifier of the item
#    * metadata (``dict``): Metadata, loaded by `load_files_metadata` and
#                           potentially modified.
#
#    Returns:
#
#    * Nothing
#    """
#    # TODO: Sort by @name entries, alphabetically?
#    result = xmltodict.unparse(metadata, pretty=True).encode('utf-8')
#    metafilesxml = check_output(['xmllint', '--format', '-'], input=result)
#    fp = open(join(PB_ITEM, '%s_files.xml_tmp' % identifier), 'wb+')
#    fp.write(metafilesxml)
#    fp.close()
#    rename(join(PB_ITEM, '%s_files.xml_tmp' % identifier), join(PB_ITEM, '%s_files.xml' % identifier))


def lookup_file_metadata(files_metadata, filename):
    """
    Fetch file-level metadata for a specific file, as a dictionary
    (``collections.OrderedDict``)

    Args:

    * files_metadata: files metadata as returned by `load_files_metadata`.
    * filename (``str``): filename/path canonical (relative) to the item

    Returns:

    File-level metadata if it exists (``dict``) or ``None``.
    """
    # XXX: in doc, mention that changing the properties here should reflect in
    # final written file
    file_list = files_metadata['files']['file']

    for file_info in file_list:
        if file_info['@name'] == filename:
            return file_info

    return None


def lookup_file_derivative_path(files_metadata, filename):
    """
    Lookup the derivation path of a given file and return it as a list.

    For example, a $foo_page_numbers.json file is typically derived from a
    $foo_djvu.xml, which is derived from a $foo_hocr.html, which is derived from
    a $foo_chocr.html.gz file, which can be derived from a $foo_jp2.zip file,
    which could be derived from a $foo.pdf file.

    If the derivative path is requested for the 'foo_page_numbers.json' file,
    the return value would be as follows:

    ['foo_page_numbers.json',
     'foo_djvu.xml',
     'foo_hocr.html',
     'foo_chocr.html.gz',
     'foo_jp2.zip',
     'foo.pdf']

    Args:

    * files_metadata: files metadata as returned by `load_files_metadata`.
    * filename (``str``): filename/path canonical (relative) to the item

    Returns:

    Derivative path as a list of filenames in the item.

    May raise an ValueError if the path is abrupted unexpectedly.
    """
    count = 0
    path = []

    md = lookup_file_metadata(files_metadata, filename)
    if md is None:
        raise ValueError('Cannot look up filename in _files.xml: \'%s\'' % filename)
    # If the file is an original, just return an empty path
    if md['@source'] == 'original':
        return path

    while True:
        count += 1
        path.append(md['@name'])

        deriv = md['@source']
        if deriv == 'original':
            return path

        md = lookup_file_metadata(files_metadata, md['original'])

        if md is None:
            break

        if count > 1000:
            raise ValueError('Refusing to recursive beyond 1000 files, corrupted files metadata?')

    raise ValueError('Derivation chain does not end with source original '
                     'for file \'%s\'' % filename)


def ensure_list(value):
    """
    Simple function to turn a non-list value into a list. If the value is
    already a list, then the function is essentially a no-op and just returns
    the value as is.
    If the value is ``None`` - then the function returns ``None``.

    Args:

    * value (None or str or list): Value to turn into a list

    Returns:

    ``None`` or list
    """
    if value is None:
        return None

    if isinstance(value, list):
        return value
    else:
        return [value]


##: Indicates that a file is an original file (used with create_file_metadata)
#SOURCE_ORIGINAL = 'original'
#
##: Indicates that a file is a derivative file (used with create_file_metadata)
#SOURCE_DERIVATIVE = 'derivative'
#
#def create_file_metadata(files_metadata, filename, source=SOURCE_ORIGINAL, fileformat=None):
#    if lookup_file_metadata(files_metadata, filename) is not None:
#        raise ValueError('%s already exists in files_metadata' % filename)
#
#    # XXX: in doc, mention that one should be really careful with this
#    if source not in (SOURCE_ORIGINAL, SOURCE_DERIVATIVE):
#        raise ValueError('Invalid source type.')
#
#    if fileformat is None:
#        raise ValueError('Please specify a valid fileformat')
#
#    entry = OrderedDict([('@name', filename),
#             ('@source', source),
#             ('format', fileformat)])
#
#    return entry
#
#
#def append_file_metadata(files_metadata, file_entry):
#    # TODO: for doc, requires file to exist on disk in PB_ITEM
#
#    #md = _calculate_file_metadata(join(PB_ITEM, file_entry['@name']))
#    #file_entry.update(md)
#    files_metadata['files']['file'].append(file_entry)
#
#
#def _calculate_file_metadata(filename):
#    data = {}
#    data.update(_calc_hashes(filename))
#
#    stat_data = stat(filename)
#    data['mtime'] = stat_data.st_mtime
#    data['size'] = stat_data.st_size
#
#    return data
#
#
#def _calc_hashes(filename):
#    fd = open(filename, 'rb')
#    crc32 = 0
#    md5 = hashlib.md5()
#    sha1 = hashlib.sha1()
#
#    while True:
#        s = fd.read(65536)
#        if not s:
#            break
#        crc32 = zlib.crc32(s, crc32)
#        md5.update(s)
#        sha1.update(s)
#
#    fd.close()
#
#    data = {'crc32': ('%08X' % crc32).lower(),
#            'md5': md5.hexdigest(),
#            'sha1': sha1.hexdigest() }
#
#    return data
