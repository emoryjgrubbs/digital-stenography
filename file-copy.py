import sys

sfile = sys.argv[-1]
dfile = "out-test.png"
eof = 0

sourceopen = True
destopen = True
try:
    source = open(sfile, "rb")
    geteof = open(sfile, "a")
    eof = geteof.tell()
    geteof.close()
except OSError:
    print("Bad Path")
    sourceopen = False
if (sourceopen):
    try:
        # dest = open(dfile, "xb")
        dest = open(dfile, "wb")
    except FileExistsError:
        print("File already Exists")
        destopen = False
        source.close()
    except OSError:
        print("Bad Path")
        destopen = False
        source.close()

if (sourceopen and destopen):
    sigbytes = source.read(8)

    if (int.from_bytes(sigbytes) == 9894494448401390090):
        dest.write(sigbytes)
        while (dest.tell() < eof):
            clen = source.read(4)
            ctype = source.read(4)
            cdata = source.read(int.from_bytes(clen))
            ccrc = source.read(4)
            dest.write(clen)
            dest.write(ctype)
            dest.write(cdata)
            dest.write(ccrc)

    else:
        print("Not PNG")

    source.close()
    dest.close()
