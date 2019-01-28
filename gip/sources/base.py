import os
import tarfile

from gip import logger
from gip import exceptions

LOG = logger.get_logger(__name__)


class Source():
    """ Superclass which interfaces all the sources """

    def get_commit_hash(self):
        raise NotImplementedError

    def get_archive(self, repo, version):
        raise NotImplementedError

    def untar_archive(self, src, dest, name, remove_src=True):
        """ Extract archive to destination, zip and tar supported """
        if tarfile.is_tarfile(src):
            archive = tarfile.open(src)
            archive.extractall(path=dest)
            if remove_src:
                # No need for try/except only raises on directory.
                os.remove(src)

            # Rename when name is passed
            if name:
                extracted_folder_name = archive.getmembers()[0].name
                try:
                    os.rename(
                        src=dest.joinpath(extracted_folder_name),
                        dst=dest.joinpath(name)
                    )
                except OSError as e:
                    raise exceptions.DirectoryNotEmpty(
                        directory=e.filename2
                    )
        else:
            raise TypeError
