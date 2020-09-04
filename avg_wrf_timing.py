import os


def main():
    try:
        timing_dir = input('Enter the dir of timing logs: ')
        files = [f for f in os.listdir(timing_dir)
                 if f.startswith('timing')]

        max_statistics = dict()
        collect = {
            'User time (seconds)': [],
            'System time (seconds)': [],
            'Percent of CPU this job got': [],
            'Elapsed (wall clock) time (seconds)': [],
        }

        for fname in files:
            fpath = f'{timing_dir}/{fname}'
            with open(fpath, 'r') as f:
                txt_lines = f.readlines()

            for line in txt_lines:
                useful_line = False
                hit_key = None
                for key in collect.keys():
                    if key.split('(')[0] in line:
                        useful_line = True
                        hit_key = key
                        break

                if not useful_line:
                    continue

                if '): ' in line:
                    val_str = line.split('): ')[1]
                    # User, System
                    if ':' not in val_str:
                        val = float(val_str)
                    # Elapsed
                    else:
                        seconds = 0
                        time_parts = val_str.split(':')
                        time_parts.reverse()
                        for idx, part in enumerate(time_parts):
                            seconds += 60 ** idx * float(part)
                        val = seconds
                elif '%' in line:
                    val_str = line.split(': ')[1].replace('%', '')
                    val = float(val_str)
                else:
                    print(('Error occurs when extracting value '
                           'from line'))
                    breakpoint()
                    exit(1)

                collect[hit_key].append(val)

        for key in collect.keys():
            max_statistics[key] = max(collect[key])

        print(max_statistics)
    except Exception as msg:
        breakpoint()
        exit(msg)


if __name__ == '__main__':
    main()
