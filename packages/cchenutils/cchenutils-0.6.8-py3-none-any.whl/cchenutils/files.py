import csv
import os

from .dict import dict


def csvwrite(fp, headers, d):
    writeheader = False if os.path.exists(fp) else True
    with open(fp, 'a', encoding='utf-8') as o:
        csvwriter = csv.DictWriter(o, fieldnames=headers)
        if writeheader:
            csvwriter.writeheader()
        d = dict(d)
        csvwriter.writerow({h: d.path(h) for h in headers})
