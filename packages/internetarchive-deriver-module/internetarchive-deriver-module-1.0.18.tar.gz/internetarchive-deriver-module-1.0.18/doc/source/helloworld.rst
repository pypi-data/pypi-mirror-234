.. _helloworld:

Example deriver module
======================

This modules calls ``hocr-fold-chars`` from the ``archive-hocr-tools`` package,
and then gzips the content.

.. code-block:: python

    #!/usr/bin/env python3
    """
    Character-based hOCR to word-based hOCR converter

    Relies heavily on archive-hocr-tools
    """
    import sys

    from os.path import join, basename
    from subprocess import check_call, CalledProcessError

    import hocr
    import derivermodule
    from derivermodule.logger import get_logger
    from derivermodule.files import canonical_item_filename
    from derivermodule.task import get_task_info
    from derivermodule.metadata import load_item_metadata, write_item_metadata, \
            write_files_metadata
    from derivermodule.const import PB_TMP


    VERSION = '1.0.0'

    logger = get_logger('hocr-char-to-word')


    if __name__ == '__main__':
        # Log our module version
        logger.info('hocr-char-to-word module version %s '
                    '(python-derivermodule version: %s; hocr version: %s).',
                    VERSION, derivermodule.__version__, hocr.__version__)

        # Read task.json
        info = get_task_info()

        # Get item identifier
        identifier = info['identifier']

        # Read _meta.xml
        metadata = load_item_metadata(identifier)

        # sourceFile does not necessarily have to match the item identifier plus
        # a suffix, and can also be in a directory.
        source_file = info['sourceFile']
        target_file = info['targetFile']
        target_format = info['targetFormat']

        # Let's state our intentions
        logger.info('sourceFile: \'%s\' -> targetFile \'%s\'',
                    source_file, target_file)

        # Strip '.gz', create in /tmp - we could consider PB_FAST, but I'm afraid
        # it will not always fit.
        target_file_plain = join(PB_TMP, basename(target_file[:-3]))
        target_fd = open(target_file_plain, 'w+')

        # Call hocr-fold-chars from our hocr package
        try:
            check_call(['hocr-fold-chars', '-f', source_file], stdout=target_fd)
        except CalledProcessError:
            print('FATAL: hocr-fold-chars failed in conversion', file=sys.stderr)
            sys.exit(1)

        target_fd.close()

        # Compress with gzip
        target_fd = open(target_file, 'w+')
        try:
            check_call(['gzip', '-c', target_file_plain], stdout=target_fd)
        except CalledProcessError:
            print('FATAL: hocr-fold-chars failed in compression', file=sys.stderr)
            sys.exit(1)
        target_fd.close()

        # Write changes, if any.
        write_item_metadata(identifier, metadata)

        # Write file specific metadata, in this case, just our version.
        file_md = {'hocr_char_to_word_module_version': VERSION,
                   'hocr_char_to_word_hocr_version': hocr.__version__}
        files_metadata = {canonical_item_filename(target_file): file_md}
        write_files_metadata(files_metadata)
