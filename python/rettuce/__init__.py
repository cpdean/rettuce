__version__ = '0.0.0'

import sys


def next_line():
    while True:
        yield input()


class ItemDeleted(object):
    def __str__(self):
        return "nil"


# constant whose id in memory will be unique
# placeholder for anything that's been deleted during a transaction
DELETED = ItemDeleted()


class DBState(object):
    """
    for the course of the run, maintains
    the interface for the db.

    doesn't make any promises on multi-users yet
    """

    def __init__(self):
        # keep track of {variable: value}
        self.namespace = dict()
        # keep track of {value: count}
        self.vals = dict()
        self.transaction_depth = 1

    def get(self, name):
        cell = self.namespace.get(name, [DELETED])
        return cell[-1]

    def _set_var(self, name, value):
        """
        additional record keeping because
        cells have history
        """
        if name not in self.namespace:
            self.namespace[name] = []
        cell = self.namespace.get(name)
        if len(cell) < self.transaction_depth:
            cell.append(value)
        elif len(cell) == self.transaction_depth:
            cell[-1] = value

    def _is_set(self, name):
        """
        transaction-aware namespaces get tricky
        """
        return self.get(name) != DELETED

    def _get_val(self, val):
        if val not in self.vals:
            self.vals[val] = [0]
        return self.vals[val]

    def _increment_val(self, val):
        cell = self._get_val(val)
        if len(cell) == 0:
            cell.append(1)
            return
        elif len(cell) < self.transaction_depth:
            current = cell[-1]
            cell.append(current + 1)
        elif len(cell) == self.transaction_depth:
            current = cell[-1]
            cell[-1] = current + 1

    def _decrement_val(self, val):
        cell = self._get_val(val)
        if len(cell) < self.transaction_depth:
            current = cell[-1]
            cell.append(current + 1)
        elif len(cell) == self.transaction_depth:
            current = cell[-1]
            cell[-1] = current - 1

    def set(self, name, value):
        if self._is_set(name):
            old_value = self.get(name)
            self._decrement_val(old_value)
        self._set_var(name, value)
        self._increment_val(value)

    def _unset(self, name):
        cell = self.namespace.get(name, [])
        if len(cell) == 0:
            return
        if len(cell) < self.transaction_depth:
            cell.append(DELETED)
        elif len(cell) == self.transaction_depth:
            cell[-1] = DELETED

    def unset(self, name):
        if self._is_set(name):
            old_value = self.get(name)
            self._decrement_val(old_value)

        self._unset(name)

    def num_equal_to(self, value):
        return self._get_val(value)[-1]

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
