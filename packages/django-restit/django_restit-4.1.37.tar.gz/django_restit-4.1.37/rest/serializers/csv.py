from objict import objict
from io import StringIO
from django.http import StreamingHttpResponse
import csv


def flattenObject(obj, field_names):
    NOT_FOUND = "-!@#$%^&*()-"

    row = []
    for f in field_names:
        d = getattr(obj, f, NOT_FOUND)
        if d != NOT_FOUND:
            if callable(d):
                d = d()
        elif "." in f:
            f1, f2 = f.split('.')
            d1 = getattr(obj, f1, None)
            if d1:
                if not hasattr(d1, f2):
                    if hasattr(d1, "first"):
                        d1 = d1.first()
                d = getattr(d1, f2, "")
                if callable(d):
                    d = d()
            else:
                d = ""
        elif "__" in f:
            f1, f2 = f.split('__')
            d1 = getattr(obj, f1, None)
            if d1:
                if not hasattr(d1, f2):
                    if hasattr(d1, "first"):
                        d1 = d1.first()
                d = getattr(d1, f2, "")
            else:
                d = ""
        else:
            d = "n/a"
        row.append(str(d))
    return row


def extractFieldNames(fields):
    header = []
    field_names = []
    for f in fields:
        if type(f) is tuple:
            r, f = f
            field_names.append(r)
        else:
            field_names.append(f)
        header.append(f)
    return header, field_names


def generateCSV(qset, fields, name, header_cols=None, values_list=False, output=None, stream=False):
    a = objict()
    a.name = name
    a.file = StringIO()
    if output:
        a.file = output
    csvwriter = csv.writer(a.file)
    header, field_names = extractFieldNames(fields)
    if header_cols:
        header = header_cols
    csvwriter.writerow(header)
    if values_list:
        for row in qset.values_list(*field_names):
            row = [str(x) for x in row]
            csvwriter.writerow(row)
    else:
        for obj in qset:
            csvwriter.writerow(flattenObject(obj, field_names))
    if hasattr(a.file, "getvalue"):
        a.data = a.file.getvalue()
    a.mimetype = "text/csv"
    return a


def iterCsvObject(items, writer, header, field_names):
    yield writer.writerow(header)
    for item in items:
        yield writer.writerow(flattenObject(item, field_names))


def generateCSVStream(qset, fields, name):
    import csv
    # check if we support stream mode
    header, field_names = extractFieldNames(fields)
    # rows = qset.values_list(*fields)
    pseudo_buffer = EchoWriter()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        iterCsvObject(qset, writer, header, field_names))


class EchoWriter(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def writeline(self, value):
        return "{}\n".format(value)

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
