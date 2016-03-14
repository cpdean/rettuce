__version__ = '0.0.0'

import sys


def next_line():
    while True:
        yield input()


class DBState(object):
    """
    for the course of the run, maintains
    the interface for the db.
    """

    def __init__(self):
        # keep track of {variable: value}
        self.namespace = dict()
        # keep track of {value: count}
        self.vals = dict()

    def get(self, name):
        return self.namespace.get(name, "nil")

    def set(self, name, value):
        if name in self.namespace:
            old_value = self.namespace[name]
            self.vals[old_value] -= 1
        self.namespace[name] = value
        old_count = self.vals.get(value, 0)
        self.vals[value] = old_count + 1

    def unset(self, name):
        if name in self.namespace:
            old_value = self.namespace[name]
            self.vals[old_value] -= 1
        del self.namespace[name]

    def num_equal_to(self, value):
        return self.vals.get(value, 0)

    def begin_transaction(self):
        pass

    def commit_transaction(self):
        pass

    def rollback_transaction(self):
        pass


def _main(inputs, outputs):
    write = lambda s: outputs.write(str(s) + "\n")
    the_db = DBState()
    for line in (i.lower() for i in inputs):
        try:
            if line == "end":
                break

            elif line.startswith("set "):
                cmd, varname, value = line.split()
                the_db.set(varname, value)
                write("")

            elif line.startswith("unset "):
                cmd, varname = line.split()
                the_db.unset(varname)
                write("")

            elif line.startswith("get "):
                cmd, varname = line.split()
                o = the_db.get(varname)
                write(o)

            elif line.startswith("numequalto "):
                cmd, value = line.split()
                o = the_db.num_equal_to(value)
                write(o)

            else:
                write("WHAT? " + line)
        except:
            write("failed on: " + line)
            write(line.split())
            raise


def main():
    return _main(next_line(), sys.stdout)

if __name__ == '__main__':
    main()
