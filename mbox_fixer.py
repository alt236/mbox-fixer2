#!/usr/bin/python

import argparse
import hashlib
import codecs
import io
import time
import os

FROM_HEADER = "From "
FROM_DASH_HEADER = "From -"
ENCODING_UTF8 = "utf-8"
ENCODING_FALLBACK = "windows-1252"


def hash(fname):
    blocksize = 4096
    hasher = hashlib.new('md5')
    with codecs.open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(blocksize), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def are_files_same(file1, file2):
    file1_file_size = os.path.getsize(file1)
    file2_file_size = os.path.getsize(file2)
    if file1_file_size == file2_file_size:
        file1_file_hash = hash(file1)
        file2_file_hash = hash(file2)

        if file1_file_hash == file2_file_hash:
            return True
        else:
            return False
    else:
        return False


def encoding_error_handler(err):
    if not isinstance(err, UnicodeDecodeError):
        raise TypeError("don't know how to handle %r" % err)
    flagged = err.object[err.start:err.end]
    hexIn = ":".join("{:02x}".format(ord(c)) for c in flagged)
    repl = flagged.decode(ENCODING_FALLBACK).encode(
        ENCODING_UTF8).decode(ENCODING_UTF8)
    hexOut = ":".join("{:02x}".format(ord(c)) for c in repl)

    print "  Encoding Error: Bytes in", hexIn, "out", hexOut, "human", repl
    return (repl, err.end)


def is_target_from_line(line):
    strippedLine = line.rstrip('\r\n')
    if line.startswith(FROM_HEADER) and not line.startswith(FROM_DASH_HEADER) and strippedLine != FROM_HEADER:
        return True
    else:
        return False


parser = argparse.ArgumentParser(
    description='Read an mbox file and try to escape runaway "From " lines')
parser.add_argument('--input',
                    help='The mbox file to read',
                    dest='input',
                    required=True)
parser.add_argument('--encoding-fallback',
                    help='If reading a line using {} fails, try to recover using {}'.format(
                        ENCODING_UTF8, ENCODING_FALLBACK),
                    dest='encoding_fallback',
                    action="store_true")
args = parser.parse_args()

out_filename = args.input + "_fixed"

print "Reading:", args.input
print "Will save as:", out_filename

if args.encoding_fallback:
    print "Will try to recover encoding errors using " + ENCODING_FALLBACK
    codecs.register_error("encoding_error_handler", encoding_error_handler)
else:
    print "Will NOT try to recover encoding errors"

out_file = open(out_filename, 'w')
with codecs.open(args.input, 'r', encoding=ENCODING_UTF8, errors='encoding_error_handler') as f:
    line_number = 1
    for line in f:
        # print line_number, line.rstrip()
        encoded_line = line.encode(ENCODING_UTF8)
        if is_target_from_line(encoded_line):
            print "  Escaping:", line_number, encoded_line.rstrip()
            out_file.write(">" + encoded_line)
        else:
            out_file.write(encoded_line)

        line_number = line_number + 1
out_file.flush()
out_file.close()


if are_files_same(args.input, out_filename):
    print "Files are identical, deleting the new one..."
    os.remove(out_filename)
