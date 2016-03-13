__version__ = '0.0.0'

import sys


def next_line():
    while True:
        yield input()


def _main(inputs, outputs):
    namespace = dict()
    write = lambda s: outputs.write(s + "\n")
    for line in (i.lower() for i in inputs):
        try:
            if line == "end":
                break

            elif line.startswith("set "):
                cmd, varname, value = line.split()
                namespace[varname] = value
                write("")

            elif line.startswith("unset "):
                cmd, varname = line.split()
                del namespace[varname]
                write("")

            elif line.startswith("get "):
                cmd, varname = line.split()
                o = namespace.get(varname, "nil")
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
