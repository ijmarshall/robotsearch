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
            if isinstance(v_list, list):
                for v in v_list:
                    out.append('{}  - {}'.format(k, v))
            elif any((isinstance(v_list, typ) for typ in [str, int, bool])):
                out.append('{}  - {}'.format(k, v_list))
        out.append('\n\n\n')

    return '\n'.join(out)

def dump(ris_list, file_obj):
    file_obj.write(dumps(ris_list))

def simplify(article):

    # Note currently the article *must* have at least a title
    # otherwise an exception happens

    # When strict=True, exceptions are raised
    # else empty data returned with a status message field

    try:
        # this should work for both PubMed and the Ovid/Endnote format
        out = {"title": ' '.join(article.get('TI', [])),
               "abstract": ' '.join(article.get('AB', []))}
        if 'PT' in article:
            out['ptyp'] = article['PT']
        # have an explicit use_ptyp variable, which is automatically 
        # detected
        # for PubMed, this will autoset to True for where
        # status = "MEDLINE". (and hence MeSH tagging is complete)
        # for Ovid, this will just check whether the MEDLINE database
        # was used (and if so, we have MeSH for all)
        # for all other options, we will only use title/abstract

        
        if "MEDLINE" in article.get('STAT', []):
            # PubMed + MEDLINE article
            out['use_ptyp'] = True
        elif "Ovid MEDLINE(R)" in article.get('DB', []):
            # Ovid + MEDLINE article
            out['use_ptyp'] = True
        else:
            out['use_ptyp'] = False
    except:
        raise Exception('Data was not recognised as Ovid or PubMed format')
    return out



