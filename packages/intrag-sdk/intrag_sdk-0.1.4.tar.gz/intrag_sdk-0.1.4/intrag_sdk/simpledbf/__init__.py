from io import BufferedReader, BytesIO
import struct
import datetime
import os
import codecs

# Check for optional dependencies.
import pandas as pd


class DbfBase(object):
    """
    Base class for DBF file processing objects.

    Do not instantiate this class. This provides some of the common functions
    for other subclasses.
    """

    def _chunker(self, chunksize):
        """Return a list of chunk ints from given chunksize.

        Parameters
        ----------
        chunksize : int
            The maximum chunk size

        Returns
        -------
        list of ints
            A list of chunks necessary to break up a given file. These will
            all be equal to `chunksize`, except for the last value, which is
            the remainder (<= `chunksize).
        """
        num = self.numrec // chunksize
        # Chunksize bigger than numrec
        if num == 0:
            return [
                self.numrec,
            ]
        else:
            chunks = [
                chunksize,
            ] * num
            remain = self.numrec % chunksize
            if remain != 0:
                chunks.append(remain)
            return chunks

    def _na_set(self, na):
        """Set the value used for missing/bad data.

        Parameters
        ----------
        na : various types accepted
            The value that will be used to replace missing or malformed
            entries. Right now this accepts pretty much anything, and that
            value will be used as a replacement. (May not do what you expect.)
            However, the strings 'na' or 'nan' (case insensitive) will insert
            float('nan'), the string 'none' (case insensitive) or will insert
            the Python object `None`.  Float/int columns are always
            float('nan') regardless of this setting.
        """
        if na.lower() == "none":
            self._na = None
        elif na.lower() in ("na", "nan"):
            self._na = float("nan")
        else:
            self._na = na

    def mem(self, chunksize=None):
        """Print the memory usage for processing the DBF File.

        Parameters
        ----------
        chunksize : int, optional
            The maximum chunk size that will be used to process this file.

        Notes
        -----
        This method will print the maximum amount of RAM that will be
        necessary to process and load the DBF file. (This is ~2x the file
        size.) However, if the optional chunksize is passed, this function
        will also print memory usage per chunk as well, which can be useful
        for efficiently chunking and processing a file.
        """
        if chunksize:
            if chunksize > self.numrec:
                print("Chunksize larger than number of recs.")
                print("Chunksize set to {:d}.".format(self.numrec))
            else:
                smallmem = 2.0 * (self.fmtsiz * chunksize / 1024**2)
                chkout = "Each chunk will require {:.4g} MB of RAM."
                print(chkout.format(smallmem))
        memory = 2.0 * (self.fmtsiz * self.numrec / 1024**2)
        out = "This total process would require more than {:.4g} MB of RAM."
        print(out.format(memory))

    def to_dataframe(self, chunksize=None, na="nan"):
        """Return the DBF contents as a DataFrame.

        Parameters
        ----------
        chunksize : int, optional
            Maximum number of records to process at any given time. If 'None'
            (defalut), process all records.

        na : various types accepted, optional
            The value that will be used to replace missing or malformed
            entries. Right now this accepts pretty much anything, and that
            value will be used as a replacement. (May not do what you expect.)
            However, the strings 'na' or 'nan' (case insensitive) will insert
            float('nan'), the string 'none' (case insensitive) or will insert
            the Python object `None`. Default for DataFrame is NaN ('nan');
            however, float/int columns are always float('nan')

        Returns
        -------
        DataFrame (chunksize == None)
            The DBF file contents as a Pandas DataFrame

        Generator (chunksize != None)
            This generator returns DataFrames with the maximum number of
            records equal to chunksize. (May be less)

        Notes
        -----
        This method requires Pandas >= 0.15.2.
        """
        self._na_set(na)
        if not chunksize:
            # _get_recs is a generator, convert to list for DataFrame
            results = list(self._get_recs())
            df = pd.DataFrame(results, columns=self.columns)
            del results  # Free up the memory? If GC works properly
            return df
        else:
            # Return a generator function instead
            return self._df_chunks(chunksize)

    def _df_chunks(self, chunksize):
        """A DataFrame chunk generator.

        See `to_dataframe`.
        """
        chunks = self._chunker(chunksize)
        # Keep track of the index, otherwise every DataFrame will be indexed
        # starting at 0
        idx = 0
        for chunk in chunks:
            results = list(self._get_recs(chunk=chunk))
            num = len(results)  # Avoids skipped records problem
            df = pd.DataFrame(
                results, columns=self.columns, index=range(idx, idx + num)
            )
            idx += num
            del results
            yield df


class Dbf5(DbfBase):
    """
    DBF version 5 file processing object.

    This class defines the methods necessary for reading the header and
    records from a version 5 DBF file.  Much of this code is based on an
    `ActiveState DBF example`_, which only worked for Python2.

    .. ActiveState DBF example: http://code.activestate.com/recipes/
            362715-dbf-reader-and-writer/

    Parameters
    ----------

    dbf : string
        The name (with optional path) of the DBF file.

    codec : string, optional
        The codec to use when decoding text-based records. The default is
        'utf-8'. See Python's `codec` standard lib module for other options.

    Attributes
    ----------

    dbf : string
        The input file name.

    f : file object
        The opened DBF file object

    numrec : int
        The number of records contained in this file.

    lenheader : int
        The length of the file header in bytes.

    numfields : int
        The number of data columns.

    fields : list of tuples
        Column descriptions as a tuple: (Name, Type, # of bytes).

    columns : list
        The names of the data columns.

    fmt : string
        The format string that is used to unpack each record from the file.

    fmtsiz : int
        The size of each record in bytes.
    """

    def __init__(self, dbf: bytes, codec="utf-8"):
        bytes_io = BytesIO(dbf)

        buffer_reader = BufferedReader(bytes_io)

        self._enc = codec
        self._esc = None
        # Reading as binary so bytes will always be returned
        self.f = buffer_reader

        self.numrec, self.lenheader = struct.unpack("<xxxxLH22x", self.f.read(32))
        self.numfields = (self.lenheader - 33) // 32

        # The first field is always a one byte deletion flag
        fields = [
            ("DeletionFlag", "C", 1),
        ]
        for fieldno in range(self.numfields):
            name, typ, size = struct.unpack("<11sc4xB15x", self.f.read(32))
            # eliminate NUL bytes from name string
            name = name.strip(b"\x00")
            fields.append((name.decode(self._enc), typ.decode(self._enc), size))
        self.fields = fields
        # Get the names only for DataFrame generation, skip delete flag
        self.columns = [f[0] for f in self.fields[1:]]

        terminator = self.f.read(1)
        assert terminator == b"\r"

        # Make a format string for extracting the data. In version 5 DBF, all
        # fields are some sort of structured string
        self.fmt = "".join(["{:d}s".format(fieldinfo[2]) for fieldinfo in self.fields])
        self.fmtsiz = struct.calcsize(self.fmt)

    def _get_recs(self, chunk=None):
        """Generator that returns individual records.

        Parameters
        ----------
        chunk : int, optional
            Number of records to return as a single chunk. Default 'None',
            which uses all records.
        """
        if chunk == None:
            chunk = self.numrec

        for i in range(chunk):
            # Extract a single record
            record = struct.unpack(self.fmt, self.f.read(self.fmtsiz))
            # If delete byte is not a space, record was deleted so skip
            if record[0] != b" ":
                continue

            # Save the column types for later
            self._dtypes = {}
            result = []
            for idx, value in enumerate(record):
                name, typ, size = self.fields[idx]
                if name == "DeletionFlag":
                    continue

                # String (character) types, remove excess white space
                if typ == "C":
                    if name not in self._dtypes:
                        self._dtypes[name] = "str"
                    value = value.strip()
                    # Convert empty strings to NaN
                    if value == b"":
                        value = self._na
                    else:
                        value = value.decode(self._enc)
                        # Escape quoted characters
                        if self._esc:
                            value = value.replace('"', self._esc + '"')

                # Numeric type. Stored as string
                elif typ == "N":
                    # A decimal should indicate a float
                    if b"." in value:
                        if name not in self._dtypes:
                            self._dtypes[name] = "float"
                        value = float(value)
                    # No decimal, probably an integer, but if that fails,
                    # probably NaN
                    else:
                        try:
                            value = int(value)
                            if name not in self._dtypes:
                                self._dtypes[name] = "int"
                        except:
                            # I changed this for SQL->Pandas conversion
                            # Otherwise floats were not showing up correctly
                            value = float("nan")

                # Date stores as string "YYYYMMDD", convert to datetime
                elif typ == "D":
                    try:
                        y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                        if name not in self._dtypes:
                            self._dtypes[name] = "date"
                    except:
                        value = self._na
                    else:
                        value = datetime.date(y, m, d)

                # Booleans can have multiple entry values
                elif typ == "L":
                    if name not in self._dtypes:
                        self._dtypes[name] = "bool"
                    if value in b"TyTt":
                        value = True
                    elif value in b"NnFf":
                        value = False
                    # '?' indicates an empty value, convert this to NaN
                    else:
                        value = self._na

                # Floating points are also stored as strings.
                elif typ == "F":
                    if name not in self._dtypes:
                        self._dtypes[name] = "float"
                    try:
                        value = float(value)
                    except:
                        value = float("nan")

                else:
                    err = 'Column type "{}" not yet supported.'
                    raise ValueError(err.format(value))

                result.append(value)
            yield result
