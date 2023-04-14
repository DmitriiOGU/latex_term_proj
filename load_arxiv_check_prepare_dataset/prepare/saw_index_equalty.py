

a = './first_part/math_0001154_raw.txt'
import itertools as it


def paragraphs(fileobj, separator='\n'):
    """Iterate a fileobject by paragraph"""
    ## Makes no assumptions about the encoding used in the file
    lines = []
    for line in fileobj:
        if line == separator and lines:
            yield ''.join(lines)
            lines = []
        else:
            lines.append(line)
    yield ''.join(lines)

paragraph_lists = [[], [], []]
with open(a) as f:
    paras = paragraphs(f)
    for para, group in zip(paras, it.cycle(paragraph_lists)):
        group.append(para)