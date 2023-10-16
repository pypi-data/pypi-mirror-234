
class Prints:

    @staticmethod
    def print_list(list_print: list, end_attribute='\n'):
        if list_print is not None:
            print(f'{end_attribute.join([str(x) for x in list_print])}')
        if end_attribute == '':
            print()

    @staticmethod
    def print_dict_line(dictionary: dict, end_attribute='\n'):
        for x, y in dictionary.items():
            print(f'{x} : {y}', end=end_attribute)
        if end_attribute == '':
            print()

    @staticmethod
    def print_df(df, min_1, max_1, min_2, max_2):
        for lat_f in range(min_1, max_1 + 1):
            for lon_f in range(min_2, max_2 + 1):
                print(df.at[lat_f, lon_f], end=' ')
            print()

    @staticmethod
    def print_separator(separator='-', number=45):
        print(separator*number)
