import csv
import os


DEFAULT_DICT_PATH = os.path.dirname(os.path.realpath(__file__))


class Dictionary:
    def __init__(self, filename='data.csv'):
        filename = os.path.join(DEFAULT_DICT_PATH, filename)
        self.TO_UNCOOL, self.TO_COOL = load_dictionary(filename)


def load_dictionary(filename):
    short_to_long = {}
    long_to_short = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, skipinitialspace=True)
        for row in spamreader:
            left = row[0]
            right = row[1].split(',')
            if len(right) > 1:
                for v in right:
                    v = tuple(v.lower().split())
                    long_to_short[v] = left
            else:
                v = tuple(row[1].lower().split())
                if len(v) > 1:
                    for i in range(len(v)):
                        long_to_short[(*v[:i], True)] = True
                #  print(v)
                long_to_short[v] = left

            short_to_long[row[0]] = row[1]

    return short_to_long, long_to_short


if __name__ == '__main__':
    d = Dictionary()
    import pprint
    #  pprint.pprint(d.TO_UNCOOL)
    pprint.pprint(d.TO_COOL)
