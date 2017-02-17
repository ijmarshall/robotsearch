"""
Simple RIS file parser

Tested and works with the dialects used by PubMed (MEDLINE export format) and Ovid (EndNote export format)

Exercise caution with other RIS formats or it might go wrong :)

"""
import codecs
from collections import OrderedDict
import re

def iter_load_ris(iterable):
    """
    takes either a file or list
    line-by-line
    """

    ris_re = re.compile('^[A-Z0-9]{1,4}\s*\-\s')

    needle_down = False # record player metaphor...
    entry_builder = OrderedDict()

    for line in iterable:
        if needle_down == False and ris_re.match(line):
            needle_down = True
        elif needle_down == True and line.strip()=="":
            new_entry = OrderedDict()
            for k, v in entry_builder.items():
                new_entry[k] = v
            yield(new_entry)
            entry_builder = OrderedDict()
            needle_down = False

        if needle_down:
            key = line[:4].rstrip()
            value = line[6:].rstrip()

            if key == '':
                # for pubmed style newline/tabbed continuation
                # print(last_key)
                # break
                key = last_key

            if key not in entry_builder:
                # since using an ordered dict can't do quicker
                entry_builder[key] = []

            entry_builder[key].append(value)
            last_key = key

    if entry_builder:
        new_entry = OrderedDict()
        for k, v in entry_builder.items():
            new_entry[k] = v
        yield(new_entry)






def load(ris_file_obj):
    return [i for i in iter_load_ris(ris_file_obj)]

def loads(ris_string):
    return [i for i in iter_load_ris(ris_string.splitlines())]


def dumps(ris_list):

    out = []

    for article in ris_list:
        for k, v_list in article.items():
            for v in v_list:
                out.append('{}  - {}'.format(k, v))
        out.append('\n')

    return '\n'.join(out)

def dump(ris_list, file_obj):
    file_obj.write(dumps(ris_list))

def simplify(article, strict=False):

    # Note currently the article *must* have at least a title
    # otherwise an exception happens

    # When strict=True, exceptions are raised
    # else empty data returned with a status message field

    try:
        # this should work for both PubMed and the Ovid/Endnote format
        out = {"title": ' '.join(article['TI']),
               "abstract": ' '.join(article.get('AB', [])),
               "rct_ptyp": "Randomized Controlled Trial" in article.get('PT', []),
               "format": "pubmed"}
    except:
        if not strict:
            out = {"title": "",
                   "abstract": "",
                   "rct_ptyp": None,
                   "format": "unrecognised"}
        else:
            raise Exception('Data was not recognised as either an Ovid or PubMed article')



    return out



