import os

from uritemplate import URITemplate, variables

from pysubyt.api import Sink


def assert_writable(file_path: str, force_output: bool = False):
    if not force_output:
        assert not os.path.isfile(file_path), (
            "File to write '%s' alread exists" % file_path
        )
    parent_path = os.path.dirname(os.path.abspath(file_path))
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    assert os.access(parent_path, os.W_OK), (
        "Can not write to folder '%s' for creating new files" % parent_path
    )


class SinkFactory:
    @staticmethod
    def make_sink(identifier: str, force_output: bool = False) -> Sink:
        if identifier is None:
            return StdOutSink()
        # else:
        if len(variables(identifier)) == 0:  # identifier is not a pattern
            return SingleFileSink(identifier, force_output)
        # else:                                        #identifier is a pattern
        return PatternedFileSink(identifier, force_output)


class StdOutSink(Sink):
    def __init__(self):
        pass

    def __repr__(self):
        return "StdOutSink"

    def close(self):
        pass

    def add(self, part: str, item: dict = None):
        print(part)


class SingleFileSink(Sink):
    def __init__(self, file_path: str, force_output: bool = False):
        assert_writable(file_path, force_output)
        self._file_path = file_path
        self._fopen = open(file_path, "w")
        self._force_output = force_output

    def __repr__(self):
        return "SingleFileSink('%s', %s)" % (
            os.path.abspath(self._file_path),
            self._force_output,
        )

    def close(self):
        self._fopen.close()
        self._fopen = None

    def add(self, part: str, item: dict = None):
        assert self._fopen is not None, "File to Sink to already close()d"
        self._fopen.write(part)


class PatternedFileSink(Sink):
    def __init__(self, name_pattern: str, force_output: bool = False):
        self._name_template = URITemplate(name_pattern)
        self._force_output = force_output

    def __repr__(self):
        return "PatternedFileSink('%s', %s)" % (
            self._name_template.uri,
            self._force_output,
        )

    def close(self):
        pass

    def add(self, part: str, item: dict = None):
        assert item is not None, "No data context available to expand template"
        file_path = self._name_template.expand(item)
        assert_writable(file_path, self._force_output)
        fopen = open(file_path, "w")
        fopen.write(part)
        fopen.close()
