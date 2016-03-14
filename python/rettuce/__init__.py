__version__ = '0.0.0'

import sys


def next_line():
    while True:
        yield input()


def _main(inputs, outputs):
    # keep track of {variable: value}
    namespace = dict()
    # keep track of {value: count}
    vals = dict()
    write = lambda s: outputs.write(str(s) + "\n")
    for line in (i.lower() for i in inputs):
        try:
            if line == "end":
                break

            elif line.startswith("set "):
                cmd, varname, value = line.split()
                if varname in namespace:
                    old_value = namespace[varname]
                    vals[old_value] -= 1
                namespace[varname] = value
                old_count = vals.get(value, 0)
                vals[value] = old_count + 1
                write("")

            elif line.startswith("unset "):
                cmd, varname = line.split()
                if varname in namespace:
                    old_value = namespace[varname]
                    vals[old_value] -= 1
                del namespace[varname]
                write("")

            elif line.startswith("get "):
                cmd, varname = line.split()
                o = namespace.get(varname, "nil")
                write(o)

            elif line.startswith("numequalto "):
                cmd, value = line.split()
                o = vals.get(value, 0)
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
