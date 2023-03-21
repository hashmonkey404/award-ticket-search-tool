import pandas as pd
from datetime import datetime
from styleframe import StyleFrame, Styler



def results_to_excel(results, max_stops: int):
    if len(results) == 0:
        print('No results! Finished.')
    else:
        df = pd.DataFrame(results)
        df.reset_index()

        width_dict = {}
        for col in df.columns.values.tolist():
            series = df[col]
            series_cell_top = series.map(lambda x: x.split('\n')[0]) # get first line of every cell
            max_len = max(
                series_cell_top.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header  # len(col)
            ) * 1.5 + 2
            width_dict[col] = max_len
            # print(f'{series.name} {max_len} {col}')

        sf = StyleFrame(df, styler_obj=Styler(horizontal_alignment = 'center'))
        sf.set_column_width_dict(width_dict)

        file_name = datetime.now().strftime("%Y%m%dT%H%M")
        writer = sf.to_excel(excel_writer = f'output{file_name}.xlsx', row_to_add_filters = 0)
        # writer.save()
        writer.close()
        print(f'Success! Please check the output excel file: {file_name} !')
