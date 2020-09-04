"""
Generate a csv table from a text list of IEEE style reference.

Input text file should be like:
    [1]	M. DeMaria, R. T. DeMaria, J. A. Knaff, and D. Molenar, “Tropical Cyclone Lightning and Rapid Intensity Change,” Mon. Wea. Rev., vol. 140, no. 6, pp. 1828–1842, Feb. 2012, doi: 10.1175/MWR-D-11-00236.1.
    [2]	J. A. Knaff, M. DeMaria, D. A. Molenar, C. R. Sampson, and M. G. Seybold, “An automated, objective, multiple-satellite-platform tropical cyclone surface wind analysis,” Journal of applied meteorology and climatology, vol. 50, no. 10, pp. 2149–2166, 2011.
    [3]	M. D. Powell and T. A. Reinhold, “Tropical Cyclone Destructive Potential by Integrated Kinetic Energy,” Bull. Amer. Meteor. Soc., vol. 88, no. 4, pp. 513–526, Apr. 2007, doi: 10.1175/BAMS-88-4-513.
    ......

Output csv file should be like:
    1\tM. DeMaria, R. T. DeMaria, J. A. Knaff, and D. Molenar, “Tropical Cyclone Lightning and Rapid Intensity Change,” Mon. Wea. Rev., vol. 140, no. 6, pp. 1828–1842, Feb. 2012, doi: 10.1175/MWR-D-11-00236.1.
    2\tJ. A. Knaff, M. DeMaria, D. A. Molenar, C. R. Sampson, and M. G. Seybold, “An automated, objective, multiple-satellite-platform tropical cyclone surface wind analysis,” Journal of applied meteorology and climatology, vol. 50, no. 10, pp. 2149–2166, 2011.
    3\tM. D. Powell and T. A. Reinhold, “Tropical Cyclone Destructive Potential by Integrated Kinetic Energy,” Bull. Amer. Meteor. Soc., vol. 88, no. 4, pp. 513–526, Apr. 2007, doi: 10.1175/BAMS-88-4-513.
    ......
"""

import csv
import re


def main():
    try:
        txt_path = input('Path of the text file recording bibliography: ')
        out_path = input('Path of csv file: ')
        if not out_path.endswith('.csv'):
            print('Out path must ends with ".csv"')
            exit(1)

        with open(txt_path, 'r') as f:
            txt_lines = f.readlines()

        csv_rows = []
        for idx, line in enumerate(txt_lines):
            num_re = re.search(r"\[([0-9_]+)\]", line)
            num = num_re[0].replace('[', '').replace(']', '')

            ref = line.split(num_re[0])[1].lstrip()
            one_csv_row = f'{num}\t{ref}'

            csv_rows.append(one_csv_row)

        with open(out_path, 'w') as f:
            writer = csv.writer(f)
            for row in csv_rows:
                writer.writerow(row.split('\t'))

    except Exception as msg:
        breakpoint()
        exit(msg)


if __name__ == '__main__':
    main()
