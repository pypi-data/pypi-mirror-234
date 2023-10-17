import tempfile
import zipfile
from subprocess import check_call
from os.path import exists, splitext, join

import xmltodict

from .const import PB_ITEM, PB_TMP
from .logger import logger


def get_scandata_xml(identifier, source_file):
    """
    Parses the scandata.xml file for a given identifier and source_file.

    Args:

    * identifier (``str``): Identifier of the item
    * source_file (``str``): sourceFile to be operated on

    Returns:

    * Path to the scandata (``str``) or None
    """
    zip_path = join(PB_ITEM, 'scandata.zip')
    raw_xml_path = join(PB_ITEM, 'scandata.xml')

    # First try to transform source_file to matching scandata:
    #
    # - Special case _page_numbers.json
    # - Then try generic _suffix.genericextension(s)
    # - Then try .genericextension
    # - (We don't currently do this: try .genericextension.anothergenericextension)
    # - Then try the scandata.xml
    # - Then try the zip path containing the scandata

    if source_file:
        if source_file.endswith('page_numbers.json'):
            source_xml_path = source_xml_path = f'{source_file[:-18]}_scandata.xml'
            if exists(source_xml_path):
                return source_xml_path

        source_xml_path = f'{source_file.rsplit("_", 1)[0]}_scandata.xml'
        if exists(source_xml_path):
            return source_xml_path

        source_xml_path = splitext(source_file)[0] + '_scandata.xml'
        if exists(source_xml_path):
            return source_xml_path

    if exists(raw_xml_path):
        return raw_xml_path
    elif exists(zip_path):
        try:
            # XXX: We don't clean up the temporary directory when we're done,
            # since the Docker container will remove all files upon completion.
            directory = tempfile.mkdtemp(dir=PB_TMP)
            xml_path = join(directory, 'scandata.xml')

            zf = zipfile.ZipFile(zip_path)
            sf = zf.open('scandata.xml')
            f = open(xml_path, 'wb+')
            f.write(sf.read())
            f.close()
            sf.close()
            zf.close()

            if not exists(xml_path):
                logger.warning('Found scandata.xml in zip but could not extract it!')
                return None
        except Exception as e:
            logger.warning('Unable to extract scandata.xml from scandata.zip')
            logger.exception(e)
            return None

        return xml_path

    logger.warning(f'Unable to find scandata file')
    return None


def scandata_parse(scandata_path):
    """
    Parse scandata.xml to native Python format

    Args:

    * scandata_path (``str``): Path to the scandata

    Returns:

    * Scandata as dictionary
    """
    scandata = xmltodict.parse(open(scandata_path, 'rb').read())
    return scandata


def scandata_get_page_count(scandata):
    """
    Get the number of page elements in a parsed scandata object

    Args:

    * scandata (``dict``): Scandata as returned by `scandata_parse`.

    Returns:

    * The number of page elements (``int``)
    """
    pages = scandata.get('book', {}).get('pageData', {}).get('page', [])
    if not isinstance(pages, list):
        pages = [pages]

    return len(pages)


def scandata_get_skip_pages(scandata):
    """
    Returns a list of indexes of pages in scandata.xml that have
    addToAccessFormats = false

    Args:

    * scandata: Parsed scandata as returned by scandata_parse

    Returns:

    * Indexes of pages that should not added to access formats
      (``list of int``)
    """
    skip = []

    pages = scandata['book']['pageData']['page']

    # If there is just one page, pages is not a list.
    if not isinstance(pages, list):
        pages = [pages]

    for idx in range(len(pages)):
        try:
            add_to_access_format = pages[idx]['addToAccessFormats']
            if add_to_access_format == 'false':
                skip.append(idx)
        except KeyError:
            pass

    return skip

def scandata_get_pagetype_pages(scandata, page_type):
    """
    Returns a list of indexes of pages in scandata.xml that have
    a specific page_type - case insensitive

    Args:

    * scandata: Parsed scandata as returned by scandata_parse
    * page_type: Page type as string, e.g. 'Cover', 'Normal', etc (full list not provided)

    Returns:

    * Indexes of pages that match a specific page type
      (``list of int``)
    """
    page_type_match = []

    pages = scandata['book']['pageData']['page']

    # If there is just one page, pages is not a list.
    if not isinstance(pages, list):
        pages = [pages]

    page_type = page_type.lower()

    for idx in range(len(pages)):
        try:
            if pages[idx]['pageType'].lower() == page_type:
                page_type_match.append(idx)
        except KeyError:
            pass

    return page_type_match
