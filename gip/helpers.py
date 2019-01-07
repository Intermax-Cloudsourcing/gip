import yaml


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Requirements:

    def __init__(self, path, logger):
        self.logger = logger
        self.requirements = self._parse(path)

    def _parse(self, requirements_file):
        try:
            file_stream = open(requirements_file, 'r')
        except OSError as e:
            self.logger.error(e)
        else:
            try:
                return yaml.safe_load(file_stream)
            except yaml.YAMLError as e:
                # TODO: Write nice to logfile/Docker log output?
                self.logger.error(e)
                raise
            finally:
                file_stream.close()


class Logger:
    def error(self, e):
        print(e)
