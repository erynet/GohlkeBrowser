# -*- coding:utf-8 -*-
from __future__ import print_function

__author__ = 'ery'

# thank you for your dedication, Christoph Gohlke

import sys, os
import cmd


def get_url_of_modules_from_gohlke(keywords, base="""http://www.lfd.uci.edu/~gohlke/pythonlibs/"""):
    def dl(ml, mi):
        def dl1(ml, mi):
            import cStringIO
            sio = cStringIO.StringIO()
            for i in range(len(mi)):
                sio.write(chr(ml[ord(mi[i]) - 48]))

            return sio.getvalue()

        mi = mi.replace('&lt;', '<')
        mi = mi.replace('&#62;', '>')
        mi = mi.replace('&#38;', '&')
        return dl1(ml, mi)

    if not isinstance(keywords, (list, tuple)):
        raise AssertionError("keywords's type is must list or tuple")

    import re, urllib2
    user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
    req = urllib2.Request(url=base)
    req.add_header("User-agent", user_agent)

    candidate = []
    try:
        res = urllib2.urlopen(req)
        # headers = res.info().headers
        body = res.read()

        found = re.findall("""javascript:dl\\((\\[.+\\]), \\"(.+)\\"\\)\\' title""", body)
        for entry in found:
            try:
                translated = dl(eval(entry[0]), str(entry[1]))
                if translated.lower()[-4:] == ".whl":
                    candidate.append(translated)
            except Exception as err:
                print(str(err))
                continue
    except Exception as err:
        print(str(err))
        return []

    if len(keywords) == 0:
        candidate.sort()
        return map(lambda x: base + x, candidate)

    result = []
    lower_keywords = map(str.lower, keywords)

    for entry in candidate:
        is_ok = True
        lower_entry = str.lower(entry)
        for keyword in lower_keywords:
            if keyword not in lower_entry:
                is_ok = False
                break
        if is_ok:
            result.append(entry)

    result.sort()
    return map(lambda x: base + x, result)


def download_and_install_from_web(url):
    try:
        import pip
    except ImportError:
        import urllib2
        res = urllib2.urlopen(url="https://bootstrap.pypa.io/get-pip.py")
        print("Install pip ...")
        exec (res.read())

    import tempfile
    temp_path = os.path.join(tempfile.gettempdir(), "temp.whl")
    with open(temp_path) as fp:
        import urllib2
        user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
        req = urllib2.Request(url=url)
        req.add_header("User-agent", user_agent)

        chunk_size = 2 ** 13
        res = urllib2.urlopen(req)
        while True:
            d = res.read(chunk_size)
            if not d:
                break
            fp.write(d)
    res.close()

    pip.main(["install", "--upgrade", temp_path])


class Telescope(object):
    def __init__(self, base="""http://www.lfd.uci.edu/~gohlke/pythonlibs/"""):
        self.base = base
        self.libset = set()
        self.verset = set()
        self.pverset = set()
        self.platformset = set()
        self.files = []
        self.d = {}
        self.catd = {}
        self.named = {}

    def open(self):
        def dl(ml, mi):
            def dl1(ml, mi):
                import cStringIO
                sio = cStringIO.StringIO()
                for i in range(len(mi)):
                    sio.write(chr(ml[ord(mi[i]) - 48]))

                return sio.getvalue()

            mi = mi.replace('&lt;', '<')
            mi = mi.replace('&#62;', '>')
            mi = mi.replace('&#38;', '&')
            return dl1(ml, mi)
        import re, urllib2

        ml_mi_regex = """javascript:dl\\((\\[.+\\]), \\"(.+)\\"\\)\\' title"""
        sub_regex = """/([^/^-]+?)-([^/^-]+?)-([^/^-]+?)-.*?(win32|amd64|any).whl"""

        user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
        req = urllib2.Request(url=self.base)
        req.add_header("User-agent", user_agent)

        entries = []
        try:
            res = urllib2.urlopen(req)

            found = re.findall(ml_mi_regex, res.read())
            for entry in found:
                if len(entry) != 2:
                    assert(len(entry) == 2)

                try:
                    translated = dl(eval(entry[0]), str(entry[1]))
                    if translated.lower()[-4:] == ".whl":
                        entries.append(translated)
                        self.files.append(translated.split("/")[1])
                except Exception as err:
                    print(str(err))
                    continue
        except Exception as err:
            print(str(err))
            return

        counter = 0
        entries.sort()
        for entry in entries:
            try:
                m = re.findall(sub_regex, entry)
                if len(m) == 1:
                    lib, ver, pver, platform = m[0]

                    lib = lib.lower()
                    ver = ver.lower()
                    pver = pver.lower()
                    platform = platform.lower()

                    self.libset.add(lib)
                    self.verset.add(ver)
                    self.pverset.add(pver)
                    self.platformset.add(platform)

                    if lib not in self.d:
                        self.d[lib] = {}
                    if ver not in self.d[lib]:
                        self.d[lib][ver] = {}
                    if pver not in self.d[lib][ver]:
                        self.d[lib][ver][pver] = {}
                    if platform not in self.d[lib][ver][pver]:
                        v = {"82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89": entry.split("/")[1],
                             "28e5ebabd9d8f6e237df63da2b503785093f0229241bc7021198f63c43b93269": self.base + entry,
                             "77af778b51abd4a3c51c5ddd97204a9c3ae614ebccb75a606c3b6865aed6744e": counter}
                        self.d[lib][ver][pver][platform] = v
                        self.catd[counter] = (entry.split("/")[1], self.base + entry)
                        self.named[v["82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89"]] = counter
                        counter += 1
                else:
                    print("Anomaly: " + entry)
            except Exception as err:
                print(str(err))
                return

        self.files.sort()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def raw_search(self, keywords):
        if len(keywords) == 0:
            return self.files

        result = []
        lower_keywords = map(str.lower, keywords)

        for entry in self.files:
            is_ok = True
            lower_entry = str.lower(entry)
            for keyword in lower_keywords:
                if keyword not in lower_entry:
                    is_ok = False
                    break
            if is_ok:
                result.append(entry)

        result.sort()
        return result

    def download(self, url, path):
        only_path, fname = os.path.split(path)[:2]
        with open(path, "wb") as fp:
            import urllib2
            user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
            req = urllib2.Request(url=url)
            req.add_header("User-agent", user_agent)

            res = urllib2.urlopen(req)
            total_size = res.info().getheader('Content-Length').strip()
            total_size = int(total_size)

            byte_to_read = total_size
            chunk_size = 2 ** 13
            while byte_to_read > 0:
                yield False, byte_to_read, total_size, None, None
                d = res.read(chunk_size)
                if d:
                    fp.write(d)
                    fp.flush()
                    byte_to_read -= len(d)
                else:
                    break
            assert(byte_to_read == 0)
            yield True, byte_to_read, total_size, only_path, fname

    def download_by_index(self, idx, only_path):
        return self.download(url=self.catd[idx][1], path=os.path.join(only_path, self.catd[idx][0]))


class GohlkeBrowser(cmd.Cmd):
    intro = "Welcome to the GohlkeBrowser.\nType help or ? to list commands.\n"
    prompt_fmt = "[%s]>> "
    cli = Telescope()
    cli.open()

    path = []

    @property
    def prompt(self):
        base = ""
        try:
            import __pypy__
            base += "pypy"
        except ImportError:
            base += "cp"
        base += (str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro) + "-")
        import platform
        if platform.architecture()[0] == "64bit":
            base += "amd64@"
        else:
            base += "win32@"

        if len(self.path) > 0:
            base += "/".join(self.path)
        else:
            base += "/"

        return self.prompt_fmt % (base,)

    # -----
    def do_search(self, arg):
        "search by keywords : search pillow cp27 amd64"
        s = arg.split(" ")
        candidate_ = self.cli.raw_search(s)
        if len(candidate_) > 20:
            print("too many candidates")
            return

        for entry in candidate_:
            print(" %5d: %s" % (self.cli.named[entry], entry))
    # -----

    # -----
    def do_install(self, arg):
        "search by keywords : install 672"
        n = 0
        try:
            n = int(arg)
        except Exception as err:
            print("Invalid argument")
            return

        if n not in self.cli.catd:
            print("Invalid module number")
            return

        try:
            import pip
        except ImportError:
            import urllib2
            res = urllib2.urlopen(url="https://bootstrap.pypa.io/get-pip.py")
            print("Install pip ...")
            exec (res.read())

        import tempfile
        is_initial = True
        progress = 0
        for is_complete, byte_to_read, total_size, only_path, fname in self.cli.download_by_index(idx=n, only_path=tempfile.gettempdir()):#url=self.cli.catd[n][1], path=os.path.join(tempfile.gettempdir(), self.cli.catd[n][0])):
            if is_initial:
                print("Total %d bytes -> " % (total_size,), end="")
                is_initial = False

            if is_complete:
                print("100%")
                pip.main(["install", "--upgrade", os.path.join(only_path, fname)])
                break
            else:
                current_progress = (total_size - byte_to_read) * 100. / total_size
                if current_progress >= (progress + 16):
                    print("%d%% .. " % current_progress, end="")
                    progress = current_progress

    # def complete_install(self, text, line, begidx, endidx):
    #     if not text:
    #         return ("",)
    #     else:
    #         candidate_ = []
    #         for lib in self.cli.libset:
    #             if lib.startswith(text):
    #                 candidate_.append(lib)
    #
    #         return candidate_ if len(candidate_) > 0 else ("",)
    # -----

    # -----
    def do_download(self, arg):
        "search by keywords : download 672 d:\\download"
        s = arg.split(" ")
        n = 0
        try:
            n = int(s[0])
        except Exception as err:
            print("Invalid argument")
            return

        if n not in self.cli.catd:
            print("Invalid module number")
            return

        if not os.path.isdir(s[1]):
            print("Invalid path")
            return

        is_initial = True
        progress = 0
        for is_complete, byte_to_read, total_size, only_path, fname in self.cli.download_by_index(idx=n, only_path=s[1]):
            if is_initial:
                print("Total %d bytes -> " % (total_size,), end="")
                is_initial = False

            if is_complete:
                print("100%")
                print("%s ... done" % (os.path.join(only_path, fname),))
                break
            else:
                current_progress = (total_size - byte_to_read) * 100. / total_size
                if current_progress >= (progress + 16):
                    print("%d%% .. " % current_progress, end="")
                    progress = current_progress

    # def complete_download(self, text, line, begidx, endidx):
    #     if not text:
    #         return ("",)
    #     else:
    #         return ("",)
    # -----

    # -----
    def do_bye(self, arg):
        "exit shell : bye"
        return True
    # -----

    def precmd(self, line):
        line = line.lower()
        return line

if __name__ == "__main__":
    sh = GohlkeBrowser()
    try:
        sh.cmdloop()
    except KeyboardInterrupt:
        sh.do_bye("")
