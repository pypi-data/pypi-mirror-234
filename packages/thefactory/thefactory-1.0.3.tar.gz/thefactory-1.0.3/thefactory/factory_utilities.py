#!/opt/thefactory_venv/bin/python
import os
import magic
from binaryornot.check import is_binary
from zipfile import ZipFile


class FileTyper:
    """Detects the filetype of a file.
    filetyper = factory_utilities.FileTyper()
    file_type = filetyper.file_type(filename)
    """

    def __init__(self):
        import thefactory.config as config
        db = config.DBaseLive()
        bytes_sql = """SELECT CAST(Header_offset AS UNSIGNED)                                       AS Header,
           REPLACE(`Header (hex)`, ' ', '')                                      AS header,
           IF(`Trailer (hex)` = '(null)', '', REPLACE(`Trailer (hex)`, ' ', '')) AS trailer,
           Extension,
           file_type
    FROM workshop.file_signatures
    ORDER BY LENGTH(`Header (hex)`) DESC, file_type"""
        db.curs.execute(bytes_sql)
        self.byte_rows = db.curs.fetchall()
        db.conn.close()
        self.mt = magic.Magic(mime=True)

    def file_type(self, filename):
        if os.path.isfile(filename):
            if is_binary(filename):
                with open(filename, 'rb') as file:
                    if bytes.hex(file.read(4)) == '504b0304':
                        with ZipFile(file, 'r') as zip_rep:
                            f_list = set([x.split('/')[0] for x in list(zip_rep.NameToInfo.keys())])
                            if [i for i in ['xl', 'styles.xml'] if i in f_list]:
                                return 2
                            else:
                                return 5
                    else:
                        for (offset, header, trailer, ext, ft) in self.byte_rows:
                            file.seek(offset, 0)
                            b_header = bytes.fromhex(header)
                            b = file.read(len(b_header))
                            if b == b_header:
                                return ft
                        return 999
            else:
                return 0
        else:
            return -1


class FileTyperStatic:
    """Detects the filetype of a file.
    filetyper = factory_utilities.FileTyper()
    file_type = filetyper.file_type(filename)
    """

    def __init__(self):
        self.magic_beans = [
            {
                "byte_desc": "XLS file",
                "offset": 0,
                "length": 8,
                "whence": 0,
                "byte_hex": "D0CF11E0A1B11AE1",
                "file_type": 1,
            },
            {
                "byte_desc": "XLSX file",
                "offset": 0,
                "length": 4,
                "whence": 0,
                "byte_hex": "504B0506",
                "file_type": 2,
            },
            {
                "byte_desc": "XLS",
                "offset": 512,
                "length": 8,
                "whence": 0,
                "byte_hex": "0908100000060500",
                "file_type": 1,
            },
            {
                "byte_desc": "XLSX",
                "offset": 0,
                "length": 8,
                "whence": 0,
                "byte_hex": "504B030414000600",
                "file_type": 2,
            },
            {
                "byte_desc": "XLS",
                "offset": 0,
                "length": 8,
                "whence": 0,
                "byte_hex": "D0CF11E0A1B11AE1",
                "file_type": 1,
            },
            {
                "byte_desc": "XLS",
                "offset": 512,
                "length": 4,
                "whence": 0,
                "byte_hex": "FDFFFFFF",
                "file_type": 1,
            },
            {
                "byte_desc": "XLS",
                "offset": 512,
                "length": 8,
                "whence": 0,
                "byte_hex": "0908100000060500",
                "file_type": 1,
            },
            {
                "byte_desc": "XLS",
                "offset": 22,
                "length": 4,
                "whence": 2,
                "byte_hex": "504B0506",
                "file_type": 1,
            },
            {
                "byte_desc": "XLSX",
                "offset": 0,
                "length": 7,
                "whence": 0,
                "byte_hex": "504B0304140008",
                "file_type": 2,
            },
            # {
            #     "byte_desc": "XLSX",
            #     "offset": 0,
            #     "length": 4,
            #     "whence": 0,
            #     "byte_hex": "504B0304",
            #     "file_type": 2,
            # },
            {
                "byte_desc": "PDF File",
                "offset": 0,
                "length": 4,
                "whence": 0,
                "byte_hex": "25504446",
                "file_type": 3,
            },
            {
                "byte_desc": "ACCDB",
                "offset": 0,
                "length": 19,
                "whence": 0,
                "byte_hex": "000100005374616E64617264204A6574204442",
                "file_type": 4,
            },
            {
                "byte_desc": "MDB",
                "offset": 0,
                "length": 19,
                "whence": 0,
                "byte_hex": "000100005374616E6461726420414345204442",
                "file_type": 4,
            },
            {
                "byte_desc": "PKZIP archive_1",
                "offset": 0,
                "length": 4,
                "whence": 0,
                "byte_hex": "504B0304",
                "file_type": 5,
            },
            {
                "byte_desc": "PKLITE archive",
                "offset": 30,
                "length": 6,
                "whence": 0,
                "byte_hex": "504B4C495445",
                "file_type": 5,
            },
            {
                "byte_desc": "PKSFX self-extracting archive",
                "offset": 526,
                "length": 5,
                "whence": 0,
                "byte_hex": "504B537058",
                "file_type": 5,
            },
            {
                "byte_desc": "PKZIP archive_2",
                "offset": 0,
                "length": 4,
                "whence": 0,
                "byte_hex": "504B0506",
                "file_type": 5,
            },
            {
                "byte_desc": "PKZIP archive_3",
                "offset": 0,
                "length": 4,
                "whence": 0,
                "byte_hex": "504B0708",
                "file_type": 5,
            },
            {
                "byte_desc": "7z archive",
                "offset": 0,
                "length": 6,
                "whence": 0,
                "byte_hex": "377ABCAF271C",
                "file_type": 5,
            },
            {
                "byte_desc": "WinZip compressed archive",
                "offset": 29152,
                "length": 6,
                "whence": 0,
                "byte_hex": "57696E5A6970",
                "file_type": 5,
            },
            {
                "byte_desc": "ZLock Pro encrypted ZIP",
                "offset": 0,
                "length": 8,
                "whence": 0,
                "byte_hex": "504B030414000100",
                "file_type": 5,
            },
            {
                "byte_desc": "WinRAR compressed archive",
                "offset": 0,
                "length": 7,
                "whence": 0,
                "byte_hex": "526172211A0700",
                "file_type": 6,
            },
            {
                "byte_desc": "PNG",
                "offset": 0,
                "length": 8,
                "whence": 0,
                "byte_hex": "89504E470D0A1A0A",
                "file_type": 7,
            },
            {
                "byte_desc": "GIF87a",
                "offset": 0,
                "length": 6,
                "whence": 0,
                "byte_hex": "474946383761",
                "file_type": 7,
            },
            {
                "byte_desc": "GIF89a",
                "offset": 0,
                "length": 6,
                "whence": 0,
                "byte_hex": "474946383961",
                "file_type": 7,
            },
            {
                "byte_desc": "Winmail.DAT",
                "offset": 0,
                "length": 4,
                "whence": 0,
                "byte_hex": "789F3E22",
                "file_type": 8,
            },
        ]

    def file_type(self, filename):

        # testf = Path(filename)
        # if testf.is_file():
        if os.path.isfile(filename):
            with open(filename, "rb") as f:
                if is_binary(filename):
                    file_type = 999
                    for bm in self.magic_beans:
                        f.seek(bm["offset"], bm["whence"])
                        b = f.read(bm["length"])
                        b_bytes = bytes.fromhex(bm["byte_hex"])
                        if b == b_bytes:
                            file_type = bm["file_type"]
                            break
                else:
                    file_type = 0
            return file_type
        else:
            return -1

    def file_type_verbose(self, filename):

        # testf = Path(filename)
        # if testf.is_file():
        if os.path.isfile(filename):
            with open(filename, "rb") as f:
                if is_binary(filename):
                    file_type = 999
                    file_desc = "Unknown file"
                    for bm in self.magic_beans:
                        f.seek(bm["offset"], bm["whence"])
                        b = f.read(bm["length"])
                        b_bytes = bytes.fromhex(bm["byte_hex"])
                        if b == b_bytes:
                            file_type = bm["file_type"]
                            file_desc = bm["byte_desc"]
                            break
                else:
                    file_type = 0
                    file_desc = "Text File"
            return file_type, file_desc
        else:
            return -1, ""


def charset_detect(filename):
    """
    Gets likely encoding for file
    :param filename: filename
    :return: charset
    Lets eat 4MB of data, if it's there, otherwise eat the whole thing
    """
    from cchardet import UniversalDetector
    from chardet import UniversalDetector as Uni2
    detector = UniversalDetector()
    detector2 = Uni2()
    detector.reset()
    detector2.reset()
    r_size = os.path.getsize(filename)
    siz = min(4096000, r_size)
    with open(filename, "rb") as f:
        if r_size > siz:
            while True:
                chunk = f.read(siz)
                detector.feed(chunk)
                if detector.done or not chunk:
                    break
        else:
            detector.feed(f.read())
    detector.close()
    if detector.result:
        return detector.result["encoding"]
    else:
        with open(filename, "rb") as f:
            if r_size > siz:
                while True:
                    chunk = f.read(siz)
                    detector2.feed(chunk)
                    if detector2.done or not chunk:
                        break
            else:
                detector2.feed(f.read())
        detector2.close()
        return detector2.result["encoding"]


def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def charset_detect_string(test_text):
    from chardet.universaldetector import UniversalDetector

    detector = UniversalDetector()
    enc_list = [
        "ascii",
        "utf-8",
        "utf-16le",
        "utf-16be",
        "UTF-8-SIG",
        "Windows-1252",
    ]
    for enc in enc_list:
        try:
            out_text = test_text.decode(enc)
            return out_text
        except UnicodeDecodeError:
            continue

    detector.reset()
    detector.feed(test_text)
    detector.close()
    out_text = test_text.decode(detector.result["encoding"])
    return out_text


def get_key(parent_dict, keys, default=None):
    """Looks inside nested dict to see if a key exists"""
    for key in keys:
        parent_dict = parent_dict.get(key, None)
        if parent_dict is None:
            return default
    return parent_dict


def make_sql(table, fld_dict, ins_type="r"):
    """
    Makes an sql statement from a table name and a list or a dict of fields
    :param table: table name referenced in sql
    :param fld_dict: a dict of the fields in the table
    :param ins_type: r or i - replace query or insert query. Defaults to replace.
    :return:
    """

    if ins_type == "i":
        ins = "INSERT"
    else:
        ins = "REPLACE"
    if isinstance(fld_dict, dict):
        vals = dict.fromkeys(fld_dict)
        columns = "`" + "`, `".join(vals.keys()) + "`"
    else:
        vals = fld_dict
        columns = "`" + "`, `".join(vals) + "`"
    placeholders = ", ".join(["%s"] * len(vals))
    return f"{ins} INTO {table} ( {columns} ) VALUES ( {placeholders} )"


def safe_str(v, t):
    """
    Converts to/ensures a value is the desired type
    :param v: The value
    :param t: The type of the value. Datetime etc.
    :return: The cleaned up value
    """
    from datetime import datetime
    import timestring

    if v is None or v == "":
        return ""
    else:
        if t == "string":
            return v.strip()
        elif t == "int":
            return int(v)
        elif t in ["decimal", "double", "float"]:
            return float(v)
        elif t == "boolean":
            if v:
                return "Y"
            else:
                return "N"
        elif t == "dateTime":
            return f"{timestring.Date(v).date:%Y-%m-%d %H:%M:%S}"
        elif t == "timeStamp":
            return datetime.fromtimestamp(v).strftime("%Y-%m-%d %H:%M:%S")


def get_info_from_a_id(a_id):
    """Get the filename and schema from the process id given
    Get the argument from
    from factory_utilities import get_info_from_a_id
    a_id = sys.argv[1]
    filename, database =  get_info_from_a_id(a_id)
    """
    import thefactory.config as config

    db = config.DBaseLive()
    sql = f"""SELECT a.file_name, c.schema_name
FROM workshop.assembly_line a,
     workshop.file_list f,
     workshop.customers c
WHERE a.process_no = f.file_no
  AND f.client = c.cust_string
  AND assembly_id = %(ass_id)s"""
    db.curs.execute(sql, {"ass_id": a_id})
    (filename, database) = db.curs.fetchone()
    db.conn.commit()
    return filename, database
