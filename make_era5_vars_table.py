"""
Generate a text table in for LaTeX from a text list of variables.

Input text file should be like:
    & 10m u component of neutral wind
    & 10m u component of wind
    & 10m v component of neutral wind
    & 10m v component of wind
    & 2m dewpoint temperature
    ......

Output a text file which has columned by user's
instruction. It will be like this when `cols_num` is 2 and `vars_num` is 57:
    1	& 10m u component of neutral wind	& 30	& mean wave period based on first moment for wind waves\\
    2	& 10m u component of wind	& 31	& mean wave period based on second moment for swell\\
    3	& 10m v component of neutral wind	& 32	& mean wave period based on second moment for wind waves\\
    ......

"""
import copy
import math


def main():
    try:
        txt_path = input('Path of the text file recording ERA5 variables: ')
        cols_num = int(input('Number of columns: '))
        out_path = input('Path of edited text file: ')

        with open(txt_path, 'r') as f:
            txt_lines = f.readlines()

        rows_num = []
        vars_num = len(txt_lines)
        tmp_cols_num = copy.copy(cols_num)
        while vars_num:
            row_num_of_this_col = int(math.ceil(vars_num / tmp_cols_num))
            rows_num.append(row_num_of_this_col)
            vars_num -= row_num_of_this_col
            tmp_cols_num -= 1

        table_cells = []
        for i in range(max(rows_num)):
            row = []
            # Multiple 2 to store number of variable
            for j in range(2 * cols_num):
                row.append('')

            table_cells.append(row)

        vars_num = len(txt_lines)
        # Only refer to column index of variable name
        for txt_line_idx, line in enumerate(txt_lines):
            # Check which column does the variable fall into
            rows_num_sum = 0
            for idx, num in enumerate(rows_num):

                if (txt_line_idx >= rows_num_sum
                        and txt_line_idx < rows_num_sum + num):
                    if txt_line_idx == 29:
                        pass
                    var_cell_col_idx = 2 * idx + 1

                    if var_cell_col_idx > 2 * 1 - 1:
                        tmp_row_idx = copy.copy(txt_line_idx)
                        for row_num_of_col in rows_num[:idx]:
                            tmp_row_idx -= row_num_of_col
                        var_cell_row_idx = tmp_row_idx
                    else:
                        var_cell_row_idx = txt_line_idx

                    break

                rows_num_sum += num

            if not (var_cell_col_idx - 1):
                var_num_cell = f'{txt_line_idx+1}\t'
            else:
                var_num_cell = f'& {txt_line_idx+1}\t'
            table_cells[var_cell_row_idx][
                var_cell_col_idx - 1] = var_num_cell

            if var_cell_col_idx != 2 * cols_num - 1:
                var_cell = line.replace('\n', '\t')
            else:
                var_cell = line.replace('\n', '\\\\') + '\n'

            table_cells[var_cell_row_idx][
                var_cell_col_idx] = var_cell

        table_lines = []
        for row in table_cells:
            table_lines.append(''.join(row))

        with open(out_path, 'w') as f:
            f.writelines(table_lines)
    except Exception as msg:
        breakpoint()
        exit(msg)


if __name__ == '__main__':
    main()
