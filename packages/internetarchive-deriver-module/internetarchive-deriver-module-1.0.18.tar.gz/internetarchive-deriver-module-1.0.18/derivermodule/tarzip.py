import tarfile
import zipfile


class TarZipReader(object):
    """
    Interface for reading zip and tar files, currently supports getting a
    listing of files (excludes directories) and opening files within the archive
    through buffered readers.
    """

    def __init__(self, path):
        """
        Open a tar or zip file.

        Args:

        * path (str): Path to the zip file
        """
        self.is_zip = False
        self.is_tar = False
        self.archive = None

        try:
            self.archive = zipfile.ZipFile(path)
            self.is_zip = True
        except zipfile.BadZipFile:
            try:
                self.archive = tarfile.open(path)
                self.is_tar = True
            except tarfile.ReadError:
                raise

    def get_archive_file(self, filepath):
        """
        Get a file object to a file within the archive for reading purposes

        Args:

        * filepath (str): Path to the file within the archive

        Returns: file-like object
        """
        if self.is_zip:
            return self.archive.open(filepath)
        if self.is_tar:
            return self.archive.extractfile(filepath)

        raise NotImplementedError('')

    def get_file_list(self):
        """
        Returns an iterator that returns the paths of each file in the archive,
        ignores directories.
        """
        if self.is_zip:
            return self._get_file_list_zip()
        if self.is_tar:
            return self._get_file_list_tar()

        raise NotImplementedError('')

    def _get_file_list_zip(self):
        for fi in self.archive.namelist():
            info = self.archive.getinfo(fi)
            if info.is_dir():
                continue

            yield fi

    def _get_file_list_tar(self):
        for fi in self.archive:
            if not fi.isfile():
                continue

            yield fi.name

    def close(self):
        if self.archive:
            self.archive.close()
            self.archive = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    import sys
    with TarZipReader(sys.argv[1]) as tzr:
        print(list(tzr.get_file_list()))

    tzr = TarZipReader(sys.argv[1])
    print(list(tzr.get_file_list()))
    tzr.close()
    
