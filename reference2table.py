import csv
import re

def main():
    try:
        txt_path = input('Path of the text file recording ERA5 variables: ')
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
