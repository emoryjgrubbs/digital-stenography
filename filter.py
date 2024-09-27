import sys
import zlib

sfile = sys.argv[-1]
dfile = "out-test.png"
sourceopen = True
destopen = True
eof = 0


# read source chunk, alter any idat data, write it to dest
def convertchunk(source, dest):
    clen = source.read(4)
    ctype = source.read(4)
    cdata = source.read(int.from_bytes(clen))
    ccrc = source.read(4)
    if (ctype.decode("ascii") == "IHDR"):
        printheader(cdata)
    if (ctype.decode("ascii") == "IDAT"):
        cdata = zlib.decompress(cdata)  # may truncate data stream if the image is too large
        cdata = alteridata(clen, cdata)
        ccrc = zlib.crc32(ctype)
        ccrc = zlib.crc32(cdata, ccrc).to_bytes(4, signed=False)
    dest.write(int.to_bytes(len(cdata), length=4))
    dest.write(ctype)
    dest.write(cdata)
    dest.write(ccrc)


def printheader(cdata):
    print("-IMAGE HEADER-")
    print("width", end=' ')
    print(int.from_bytes(cdata[0:4]))
    print("height", end=' ')
    print(int.from_bytes(cdata[4:8]))
    print("bit depth", end=' ')
    print(cdata[8])
    print("color type", end=' ')
    print(cdata[9])
    print("compression method", end=' ')
    print(cdata[10])
    print("filter method", end=' ')
    print(cdata[11])
    print("interlace method", end=' ')
    print(cdata[12])
    print()


# perform bitwise operation on idat data, call altercrc so crc data matches
def alteridata(clen, cdata):
    newcdata = []
    for i in range(len(cdata)):
        # newcdata.append(cdata[i] & 255)
        newcdata.append(cdata[i])
    newcdata = zlib.compress(bytes(newcdata))
    return newcdata


# attempt to open source and dest files
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
    # check for png signature
    sigbytes = source.read(8)
    if (int.from_bytes(sigbytes) == 9894494448401390090):
        dest.write(sigbytes)
        # while there is data in the source, convert it and write to dest
        while (source.tell() < eof):
            convertchunk(source, dest)
    else:
        print("Not PNG")
    source.close()
    dest.close()
