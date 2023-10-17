# coding: utf-8
# flake8: noqa

from typing import Dict, Any, Union, Optional, List, Tuple, Generator  # NOQA

_package_data: Dict[str, Any] = dict(
    full_package_name='ruamel.yaml.split',
    version_info=(0, 2, 2),
    __version__='0.2.2',
    version_timestamp='2023-10-11 10:14:04',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='YAML document splitter, with iterator that returns document, start linenumber and optionally data',
    keywords='yaml multi document split',
    entry_points=None,
    license='Copyright Ruamel bvba 2007-2022',
    since=2022,
    # status='α|β|stable',  # the package status on PyPI
    # data_files="",
    # universal=True,  # py2 + py3
    # install_requires=['ruamel.std.pathlib', ],
    tox=dict(env='3',),  # *->all p->pypy
    python_requires='>=3',
)  # NOQA


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

##############################################################################

from pathlib import Path  # NOQA

DOCEM = b'...'  # document-end-marker
DIREM = b'---'  # directory-end-marker
bNEWLINE = 10
bSPACE = ord(' ')
bTAB = ord('\t')

# A special consideration should be given to comments (including empty lines) after DOCEM.
# Any such comments should be part of the preceding document if there is no real content
# (i.e. no directive and no DIREM following the DOCEM), this overrules any C_ setting.
#
# It is possible to have a comment after DOCEM itself, this belongs to the preceding
# document unless C_SPLIT_AFTER_DOCEM is selected.
#
# C_PRE:
#   all of the comments "between" documents belong to the preceding document
# C_POST:
#   all of the comments/newlines up to the first directive or DIREM belongs to the
#   following document
# C_SPLIT_ON_FIRST_BLANK:
#   split on the first empty line (which will bepart of the first comment) and
#   assign to preceding resp. following document. If no blank line act like C_PRE
# C_SPLIT_AFTER_DOCEM:
#   split at the end of the line containing DOCEM, comments on that line go to the
#   preceding document. This is the default.

C_POST = 0b00
C_PRE = 0b01
C_SPLIT_ON_FIRST_BLANK = 0b10
C_SPLIT_AFTER_DOCEM = 0b11


class YamlDocStreamSplitter:
    """
    split a YAML document stream into one or more  documents.

    The stream is read in memory as bytes.
    A document starts:
    - at the beginning of the stream,
    - after a `...` (document end marker), an eol comment
      is taken to be for the next document
    - starting with `---` (directives end marker) if not preceded by
      only directives, empty lines or comments.
    directives must start with '%' in first position of line
    """

    def __init__(self, path: Path, cmnt: Optional[int] = None, verbose: int = 0) -> None:
        self._path = path
        self._cmnt = cmnt if cmnt is not None else C_SPLIT_AFTER_DOCEM
        self._start_line_no = 1
        self._line_no = 1
        self._verbose = verbose
        self._content = path.read_bytes()
        self._content_len = len(self._content)
        # list of [start_byte, end_byte, start_line]
        self._indices: List[Tuple[int, int, int]] = []
        # [start, end, line_no, test_empty_line, found_empty_line]
        self._vd: Union[List[Any], None] = None

    @property
    def vd(self) -> Union[List[Any], None]:
        return self._vd

    @vd.setter
    def vd(self, val: Union[List[Any], None]) -> None:
        self._vd = val

    def check_nl(self, content: bytes, index: int) -> bool:
        if index >= self._content_len:
            return False
        b = content[index]
        if b == bNEWLINE:
            self._line_no += 1
            # if False:
            #     from inspect import stack, getframeinfo  # NOQA
            #     caller = getframeinfo(stack()[1][0])
            #     # print("%s:%d - %s" % (caller.filename, caller.lineno, message))
            #     x0 = caller.lineno
            #     x1 = self._line_no
            #     x2 = self._start_line_no
            #     #print(f'{x0:3}/{x2:3}: increased line no before {x1:>3}', end=' ')
            #     #print(content[index + 1 : index + 20])
            return True
        return False

    def get_line_no(self) -> int:
        res = self._start_line_no
        self._start_line_no = self._line_no
        return res

    def indices(self) -> Any:
        if self._indices:
            for x in self._indices:
                yield x
            return
        content = self._content
        index = 0
        newline = True
        check_directive = True
        self.vd: Union[List[Any], None] = None
        prev = 0
        while index < self._content_len:
            if not newline:
                newline = self.check_nl(content, index)
                if newline and self._cmnt == C_SPLIT_ON_FIRST_BLANK and self.vd:
                    # print('>>>>> vd', self.vd)
                    if not self.vd[4]:  # finished?
                        self._start_line_no += 1
                        if not self.vd[3]:
                            self.vd[1] = index
                            self.vd[3] = True
                        else:
                            self.vd[1] = index
                            self.vd[4] = True
                            _ = self.get_line_no()
                index += 1
                continue
            # print('check directive', check_directive, index, content[index:index+20], self.vd, self._cmnt)
            if check_directive:
                # print('here', self.vd, )
                if self._cmnt == C_SPLIT_ON_FIRST_BLANK:
                    if self.vd and self.vd[4]:
                        #print('yielding 2', self.vd)
                        prev = self.vd[1]
                        self._indices.append(tuple(self.vd[:3]))  # type:ignore
                        yield tuple(self.vd[:3])
                        self.vd = None
                elif self._cmnt != C_PRE and self.vd:
                    # print('yielding 1', self.vd)
                    prev = self.vd[1]
                    self._indices.append(tuple(self.vd[:3]))  # type:ignore
                    yield tuple(self.vd[:3])
                    self.vd = None
                newline = False
                if content[index] == ord('%'):
                    # print('here >>>> 2', self.vd, self._cmnt, C_PRE)
                    if self._cmnt == C_PRE and self.vd:
                        self.vd[1] = index
                        self.vd[2] = self.get_line_no()
                        self._indices.append(tuple(self.vd[:3]))  # type:ignore
                        yield self.vd[:3]
                        self.vd = None
                    index += 1
                    while index < self._content_len:
                        index += 1
                        if self.check_nl(content, index):
                            break
                    newline = True
                    index += 1
                    continue
                # check if this line is empty or starts with a comment
                ti = index
                while check_directive and ti < self._content_len:
                    if content[index] == bNEWLINE:  # don't use check_nl here
                        index = ti
                        newline = True
                        break
                    if content[ti] in (bSPACE, bTAB):
                        ti += 1
                        continue
                    if content[ti] == ord('#'):
                        # found a comment, skip to end of line
                        # print('>>>>> found comment', content[ti:ti+20])
                        if self.vd and self.vd[3]:
                            self.vd[3] = False
                        index = ti + 1
                        while index < self._content_len:
                            index += 1
                            if self.check_nl(content, index):
                                break
                        newline = True
                        index += 1
                        break
                    # print('unsetting directive', index)
                    check_directive = False
                    newline = False
            if not newline:
                # print('unset newline')
                continue
            # print('check directive2', check_directive,
            #       content[index:index+20], self._start_line_no, self._line_no, self.vd)
            if check_directive and index < self._content_len and content[index] == ord('%'):
                if self.vd is not None:
                    if self._cmnt == C_SPLIT_ON_FIRST_BLANK and self.vd[4]:
                        # print('here<<<<<<<<<<<<<<<<<', self.vd)
                        self._indices.append(tuple(self.vd[0:3]))  # type:ignore
                        yield tuple(self.vd[0:3])
                        prev = self.vd[1]
                        self.vd = None
                    elif self._cmnt == C_PRE or (
                        self._cmnt == C_SPLIT_ON_FIRST_BLANK and not self.vd[4]
                    ):
                        lnx = self.vd[2]
                        _ = self.get_line_no()
                        self._indices.append((self.vd[0], index, lnx))
                        yield self.vd[0], index, lnx
                        prev = index
                        self.vd = None
            if (
                content[index : index + 3] == DOCEM
                and content[index + 3 : index + 4] in b'\n \t'
            ):
                check_directive = True
                if content[index + 3] == bNEWLINE:
                    self._line_no += 1
                    index += 4
                    ln = self.get_line_no()
                    # print('setting directive nl', content[index:index+20],
                    #      newline, self._start_line_no)
                    # self._indices.append((prev, index, ln))
                    # yield prev, index, ln  # ToDo check if only when not check_directive
                    self.vd = [prev, index, ln, True, False]
                    # print('>>>1b vd', self.vd)
                    prev = index
                    # newline = True  # is already True, otherwise we wouldn't check for DOCEM
                else:
                    index += 4
                    # if C_POST, then do not gobble to the end of line
                    if self._cmnt != C_POST:
                        while not self.check_nl(content, index):
                            index += 1
                        newline = True
                        index += 1
                    ln = self.get_line_no()
                    # print('setting directive sp', content[index:index+20], newline, ln)
                    # self._indices.append((prev, index, ln))
                    # yield prev, index, ln  # ToDo check if only when not check_directive
                    self.vd = [prev, index, ln, False, False]
                    # print('>>>1a vd', self.vd)
                    prev = index
                    newline = False
                    continue
            # the following also recognizes a --- without newline at the end
            # of a file, as then content[3:3] is empty and part of any string
            if (
                content[index : index + 3] == DIREM
                and content[index + 3 : index + 4] in b'\n \t'
            ):
                if self.vd is not None:
                    if self._cmnt == C_PRE:
                        lnx = self.vd[2]
                        _ = self.get_line_no()
                        self._indices.append((self.vd[0], index, lnx))
                        yield self.vd[0], index, lnx
                        prev = index
                    else:
                        self._indices.append(tuple(self.vd[:3]))  # type:ignore
                        yield tuple(self.vd[:3])
                    # print('yielded', self.vd)
                    self.vd = None
                # print('<<<<<<<<<<< ending directive', check_directive,
                #       content[index:index+20], self._start_line_no, self._line_no)
                if not check_directive:
                    ln = self.get_line_no()
                    self._indices.append((prev, index, ln))
                    yield prev, index, ln
                    prev = index
                else:
                    check_directive = False
                index += 3
            newline = self.check_nl(content, index)
            if newline and self.vd is not None and self._cmnt == C_SPLIT_ON_FIRST_BLANK:
                # print('##/ ', self.vd)
                if self.vd[3] and not self.vd[4]:
                    self.vd[1] = index + 1
                    self.vd[4] = True
                    self._start_line_no += 1
                # print('##\\ ', self.vd)
            index += 1
        ln = self.get_line_no()
        if self.vd:
            # print('>>>1 vd', self.vd)
            prev = self.vd[0]
            ln = self.vd[2]
            self.vd = None
        self._indices.append((prev, self._content_len, ln))
        yield prev, self._content_len, ln

    def __iter__(self) -> Any:
        return YamlDocStreamIterator(self)

    def iter(self, yaml: Optional[Any] = None) -> Any:
        return YamlDocStreamIterator(self, yaml=yaml)


class YamlDocStreamIterator:
    def __init__(self, ys: YamlDocStreamSplitter, yaml: Optional[Any] = None) -> None:
        self.ys = ys
        self.indices = list(self.ys.indices())
        self._verbose = self.ys._verbose
        self._yaml = yaml
        self.index = 0

    def __next__(self) -> Tuple[bytes, int]:
        if self.index >= len(self.indices):
            raise StopIteration
        s, e, ln = self.indices[self.index]
        self.index += 1
        return self.ys._content[s:e], ln

    def si_next(self, yaml: Optional[Any] = None) -> Any:
        # returns the bytes of the next document + linenumber, or data if yaml passed in
        # an emtpy doc returns None that is not ok.
        if yaml is None and self._yaml is not None:
            yaml = self._yaml
        if yaml is None:
            return self.__next__()
        else:
            n, ln = self.__next__()
            return n, yaml.load(n), ln

    def next(self, yaml: Optional[Any] = None) -> Any:
        # returns the bytes of the next document + linenumber, or data if yaml passed in
        # an emtpy doc returns None that is not ok.
        try:
            if yaml is None and self._yaml is not None:
                yaml = self._yaml
            if yaml is None:
                return self.__next__()
            else:
                n, ln = self.__next__()
                return n, yaml.load(n), ln
        except StopIteration:
            return None

    def __iter__(self) -> Any:
        # returns the bytes of the next document + linenumber, or data if yaml passed in
        # an emtpy doc returns None that is not ok.
        if self._yaml is None:
            yield self.__next__()
        else:
            n, ln = self.__next__()
            yield n, self._yaml.load(n), ln

    def skip(self) -> None:
        # skip a document
        self.index += 1

    def done(self) -> bool:
        return self.index >= len(self.indices)


def split(
    path: Path, yaml: Optional[Any] = None, cmnt: Optional[int] = None, verbose: int=0
) -> Generator[Any, None, None]:
    # for res in YamlDocStreamSplitter(path=path, cmnt=cmnt, verbose=verbose).iter(yaml=yaml):
    #    yield res
    it = YamlDocStreamSplitter(path=path, cmnt=cmnt, verbose=verbose).iter(yaml=yaml)
    while not it.done():
        yield it.si_next()
