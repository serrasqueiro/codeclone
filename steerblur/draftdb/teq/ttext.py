"""
Module for textual TSV and related files

(c)2020  Henrique Moreira (part of 'draftdb', teq)
"""

# pylint: disable=missing-docstring, invalid-name, no-self-use, no-member

from util.osindependent import TaPath, list_dir
from util.strlist import dict_order

class AnyBTable:
    """
    Abstract class for Any basic tables.
    """
    def get_encoding(self):
        enc = self._default_encoding
        return enc if enc else "ascii"

    def _get_header(self, s):
        enc_str = ":::encoding="
        pos = s.rfind(enc_str)
        if pos > 0:
            encoding = s[pos + len(enc_str):]
            header = s[:pos]
        else:
            encoding = self._default_encoding
            header = s
        spl_header = []
        if header[0] != "#":
            return None, spl_header, encoding
        header = header[1:].strip()
        spl_header = header.replace(" ", "_").split(";")
        return header, spl_header, encoding


class TsvBase(AnyBTable):
    def __init__(self, name=""):
        assert name is not None
        self.name = name
        self.names = []
        self.ext = ".tsv"
        self._default_encoding = "ISO-8859-1"
        self._processors = {"pre": dict(),
                            }
        self._path_dict = dict()
        self._all = dict()

    def _process_read(self, f_in, rel_name, debug=0):
        assert f_in is not None
        info = ((rel_name,), (None, tuple()), (0, self._default_encoding, []), tuple())
        data = f_in.read()
        idx, pos = 0, -1
        for dig in data:
            if dig == ord("\r"):
                return None
            if dig == ord("\n"):
                pos = idx
                break
            idx += 1
        if pos < 0:
            return info
        msg = []
        header, spl_header, enc = self._get_header(data[:pos].decode("ascii"))
        tail = data[pos+1:].decode(enc)
        if header is None:
            msg.append("Header should start with '#'")
        if debug > 0:
            print("Header={}, spl_header={}".format(header, spl_header))
            print("Tail >>>\n{}<<<\n".format(tail))
        s = self.pre_process(rel_name, tail)
        if s.endswith("\n"):
            lines = s.split("\n")[:-1]
        else:
            lines = s.split("\n")
        self._sanity_check(rel_name, lines, msg)
        info = ((rel_name,), (header, tuple(spl_header)), (len(lines), enc, lines), tuple(msg))
        return info


    def _replace_content(self, info):
        names, _, payload, _ = info
        _, _, lines = payload
        assert isinstance(lines, list)
        rel_name = names[0]
        self._all[rel_name] = info
        return rel_name


    def get_table(self, rel_name):
        return self._all.get(rel_name)


    def _get_content(self, rel_name):
        if rel_name not in self._all:
            return None
        names, _, payload, _ = self._all[rel_name]
        assert isinstance(names, tuple)
        _, _, lines = payload
        return lines


    def _sanity_check(self, rel_name, lines, msg):
        assert isinstance(msg, list)
        idx = 0
        for line in lines:
            idx += 1
            if line:
                if line.strip() != line:
                    msg.append("{}:Line {}: unstripped line".format(rel_name, idx))
            else:
                msg.append("{}:Line {}: empty".format(rel_name, idx))

    def _add_path_info(self, d, sub_name):
        if sub_name in self._path_dict:
            self._path_dict[sub_name].append(d)
        else:
            self._path_dict[sub_name] = [d]


    def set_processor(self, rel_name, processor):
        self._processors["pre"][rel_name] = processor
        return True


    def pre_process(self, rel_name, data, encoding=None):
        if encoding is None:
            enc = self._default_encoding
        else:
            enc = encoding
        assert isinstance(enc, str)
        if rel_name in self._processors["pre"]:
            processor = self._processors["pre"][rel_name]
        else:
            processor = None
        if processor is None:
            return data
        return processor(data)


    def scan_tsv(self, dirs):
        res = []
        if not self.ext or len(self.ext) < 2:
            return None
        if isinstance(dirs, str):
            ds = [dirs]
        elif isinstance(dirs, (list, tuple)):
            ds = dirs
        else:
            assert False
        for d in ds:
            ta = TaPath(d)
            ls = list_dir(ta)
            for name in ls:
                rel_name = name.lower()
                if rel_name.endswith(self.ext):
                    sub_name = rel_name[:-len(self.ext)]
                    res.append(sub_name)
                    self._add_path_info(d, sub_name)
        return res


    def read_files(self, rel_paths, debug=0) -> int:
        assert self.ext
        count_fail = 0
        for p in rel_paths:
            sub_paths = self._path_dict[p]
            sub_path = sub_paths[0]
            if sub_path:
                pre_name = sub_path + "/" + p
            else:
                pre_name = p
            ta = TaPath(pre_name + self.ext)
            is_ok = ta.is_file()
            if debug > 0:
                print("is_file({}): {}".format(ta, is_ok))
            if is_ok:
                with open(ta.path, "rb") as f_in:
                    info = self._process_read(f_in, p)
                    assert info is not None
                    rel_name = self._replace_content(info)
            else:
                count_fail += 1
                rel_name = "!" + ta.path
            self.names.append(rel_name)
        self.names.sort()
        return count_fail

    def get_content(self, rel_name):
        return self._get_content(rel_name)

    def get_multiple_subnames(self) -> list:
        """
        Returns a list with pairs of ("sub_name", "path") for sub_names which are
        'ambiguous'. I.e. more than one path.
        :return: list
        """
        res = []
        names, dct = dict_order(self._path_dict)
        for sub_name in names:
            path_list = dct[sub_name]
            if len(path_list) > 1:
                res.append((sub_name, path_list))
        return res


# Main script
#
if __name__ == "__main__":
    print("Module, please run tests using ttext.test.py")
