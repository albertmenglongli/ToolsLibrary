import csv


def open_csv(filepath):
    with open(filepath) as f:
        csv_f = csv.reader(f)
        columns_idx_key = []
        row_idx_key = []
        data_table = []
        for idx, row in enumerate(csv_f):
            if idx == 0:
                columns_idx_key += row
            row_idx_key.append(row[0])
            data_table.append(row)

    def get_value_by_coordinate(row_key, column_key):
        try:
            if isinstance(row_key, str):
                row_index = row_idx_key.index(row_key)
            elif isinstance(row_key, int):
                row_index = row_key
            else:
                raise Exception("Not supported Key")

            if isinstance(column_key, str):
                column_index = columns_idx_key.index(column_key)
            elif isinstance(column_key, int):
                column_index = column_key

            value = data_table[row_index][column_index]
        except ValueError as value_error:
            key = value_error.message.split('is not in list', 1)[0]
            raise KeyError('key {} does not exist'.format(key))

        except IndexError as index_error:
            if row_index >= len(data_table) or column_index >= len(data_table[0]):
                raise StopIteration()
            if row_index < - len(data_table) or column_index < -len(data_table[0]):
                raise IndexError(
                    "negative index supported, but not that much!")
        return data_table[row_index][column_index]

    return get_value_by_coordinate

if __name__ == "__main__":
    currency_get_value = open_csv('currency.csv')

    print currency_get_value("Exchange rate", 'CNY')
    # 1 CNY = 0.1543550000 USD
    print currency_get_value("Locale", 'CNY')
    # China
    print currency_get_value("Locale", "USD")
    # USA
    print currency_get_value("Locale", -1)
    # USA
