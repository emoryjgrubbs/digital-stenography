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
        head = 0
        pal = 0
        eb = 0
        imgcs = []
        aidat = False
        ea = 0
        end = 0
        while (source.tell() < eof):
            clen = int.from_bytes(source.read(4))
            ctype = source.read(4)
            source.read(4 + clen)
            # print(ctype.decode("ascii"))
            if (ctype.decode("ascii") == "IDAT"):
                imgcs.append(clen + 12)
                aidat = True
                # print("adding image data")
            elif (ctype.decode("ascii") == "IHDR"):
                head = clen + 12
                # print("adding header")
            elif (ctype.decode("ascii") == "IEND"):
                end = clen + 12
                # print("adding end")
            elif (ctype.decode("ascii") == "PLTE"):
                pal = clen + 12
                # print("adding palette")
            else:
                if aidat:
                    ea += clen + 12
                else:
                    eb += clen + 12
                print("disregarding " + ctype.decode("ascii"))

        print("reversing " + str(len(imgcs)) + " IDAT chunks")
        imgcs.reverse()

        dest.write(sigbytes)  # writing png signature (0)
        source.seek(8)
        dest.write(source.read(head))  # writing image info (header) (1)
        dest.write(source.read(pal))  # writing image palette (2) (must preceed first idat)
        readloc = eof - end - ea  # set read location at the end of last idat block
        # readloc = 8 + head + pal + eb  # set read locatin at the start of first idat
        for chunk in imgcs:
            readloc -= chunk
            source.seek(readloc)
            clen = source.read(4)
            ctype = source.read(4)
            cdata = source.read(int.from_bytes(clen))
            ccrc = source.read(4)
            dest.write(clen)
            dest.write(ctype)
            dest.write(cdata)
            dest.write(ccrc)
            # readloc += chunk
        source.seek(eof - end)
        dest.write(source.read(end))

    else:
        print("Not PNG")

    source.close()
    dest.close()
