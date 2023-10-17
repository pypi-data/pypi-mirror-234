# Script for comparing actual data from an output file or a SQL-query with expected data in a file.
#
import csv
import datetime
import fnmatch
import os
import re
import time

import dateutil.relativedelta


class DataComparer:
    # Situations:
    # Actual txt file versus expected txt file.
    # Actual csv file versus expected csv file.
    # Array with SQL-output expected csv file.

    def compare_data_2d_array_with_file(self, actual_data, expected_file, delimiter_expected_data=None, quotechar_expected_data=None):
        if 'actual_data' not in locals():
            raise Exception("Input Actual data unknown.")
        #
        if not os.path.exists(expected_file):
            raise Exception("Input file doesn't exists: ", expected_file)
        #
        print("expected_file: ", expected_file)
        #
        if delimiter_expected_data is None:
            delimiter_expected_data = ","
        #
        if quotechar_expected_data is None:
            quotechar_expected_data = '"'
        #
        with open(expected_file, mode='rt', encoding='utf-8') as expected_file:
            time.sleep(1)
            expected_data = list(csv.reader(expected_file, delimiter=delimiter_expected_data, quotechar=quotechar_expected_data))
        #
        if actual_data == [] and expected_data == []:
            raise Exception("Actual and Expected data are not present. Actual data input 2d-array and Expected data input file are empty.")
        #
        if not actual_data:
            raise Exception("Actual data is not present. Input 2d-array is empty.")
        #
        if not expected_data:
            raise Exception("Expected data is not present. Input file is empty.")
        #
        DataComparer.__compare_data(self, actual_data, expected_data)


    def compare_data_file_with_2d_array(self, actual_file, expected_data, delimiter_actual_data=None, quotechar_actual_data=None):
        if not os.path.exists(actual_file):
            raise Exception("Input file doesn't exists: ", actual_file)
        #
        if 'expected_data' not in locals():
            raise Exception("Input Expected data unknown.")
        #
        print("actual_file: ", actual_file)
        #
        if delimiter_actual_data is None:
            delimiter_actual_data = ","
        #
        if quotechar_actual_data is None:
            quotechar_actual_data = '"'
        #
        with open(actual_file, mode='rt', encoding='utf-8') as actual_file:
            time.sleep(1)
            actual_data = list(csv.reader(actual_file, delimiter=delimiter_actual_data, quotechar=quotechar_actual_data))
        #
        if actual_data == [] and expected_data == []:
            raise Exception("Actual and Expected data are not present. Actual data input file and Expected data input 2d-array are empty.")
        #
        if not actual_data:
            raise Exception("Actual data is not present. Input file is empty.")
        #
        if not expected_data:
            raise Exception("Expected data is not present. Input 2d-array is empty.")
        #
        DataComparer.__compare_data(self, actual_data, expected_data)


    def compare_data_2d_arrays(self, actual_data, expected_data):
        if 'actual_data' not in locals():
            raise Exception("Input Actual data unknown.")
        #
        if 'expected_data' not in locals():
            raise Exception("Input Expected data unknown.")
        #
        if actual_data == [] and expected_data == []:
            raise Exception("Actual and Expected data are not present. Actual data input 2d-array and Expected data input 2d-array are empty.")
        #
        if not actual_data:
            raise Exception("Actual data is not present. Input 2d-array is empty.")
        #
        if not expected_data:
            raise Exception("Expected data is not present. Input 2d-array is empty.")
        #
        DataComparer.__compare_data(self, actual_data, expected_data)


    def compare_data_files(self, actual_file, expected_file, delimiter_actual_data=None, delimiter_expected_data=None, quotechar_actual_data=None, quotechar_expected_data=None):
        for file in (actual_file, expected_file):
            if not os.path.exists(file):
                raise Exception("Input file doesn't exists: ", file)
        #
        print("actual_file: ", actual_file)
        print("expected_file: ", expected_file)
        #
        if delimiter_actual_data is None:
            delimiter_actual_data = ","
        #
        if delimiter_expected_data is None:
            delimiter_expected_data = ","
        #
        if quotechar_actual_data is None:
            quotechar_actual_data = '"'
        #
        if quotechar_expected_data is None:
            quotechar_expected_data = '"'
        #
        with open(actual_file, mode='rt', encoding='utf-8') as actual_file, open(expected_file, mode='rt', encoding='utf-8') as expected_file:
            time.sleep(1)
            if len(delimiter_actual_data) == 1:
                actual_data = list(csv.reader(actual_file, delimiter=delimiter_actual_data, quotechar=quotechar_actual_data))
            else:
                actual_data = list(csv.reader((line.replace(delimiter_actual_data, chr(255)) for line in actual_file), delimiter=chr(255), quotechar=quotechar_actual_data))
            #
            if len(delimiter_expected_data) == 1:
                expected_data = list(csv.reader(expected_file, delimiter=delimiter_expected_data, quotechar=quotechar_expected_data))
            else:
                expected_data = list(csv.reader((line.replace(delimiter_expected_data, chr(255)) for line in expected_file), delimiter=chr(255), quotechar=quotechar_expected_data))
        #
        if actual_data == [] and expected_data == []:
            raise Exception("Actual and Expected data are not present. Input files are empty.")
        #
        if not actual_data:
            raise Exception("Actual data is not present. Input file is empty.")
        #
        if not expected_data:
            raise Exception("Expected data is not present. Input file is empty.")
        #
        DataComparer.__compare_data(self, actual_data, expected_data)


    def __compare_data(self, actual_data, expected_data_including_templates):
        difference_found = False
        #
        if actual_data == [] and expected_data_including_templates == []:
            raise Exception("Actual and Expected data are not present.")
        #
        if not actual_data:
            raise Exception("Actual data is not present.")
        #
        if not expected_data_including_templates:
            raise Exception("Expected data is not present.")
        #
        number_of_rows_actual_data   = len(actual_data)
        number_of_rows_expected_data = len(expected_data_including_templates)

        number_of_rows = number_of_rows_actual_data if (number_of_rows_actual_data >= number_of_rows_expected_data) else number_of_rows_expected_data

        DataComparer.__print_2d_array(self, "Actual data", actual_data, 20)
        DataComparer.__print_2d_array(self, "Expected data", expected_data_including_templates, 20)

        print()
        print("=== Overview differences between actual and expected data")
        print()

        for row_nr in range(number_of_rows):
            if row_nr >= number_of_rows_actual_data:
                difference_found = True
                if len(expected_data_including_templates[row_nr]) == 0:
                    DataComparer.__print_comparation_result(self, row_nr, 0, "", "", "Row actual data is not PRESENT. Row expected data is EMPTY.")
                else:
                    DataComparer.__print_comparation_result(self, row_nr, 0, "", expected_data_including_templates[row_nr][0], "Row actual data is not PRESENT.")
                continue
            #
            if row_nr >= number_of_rows_expected_data:
                difference_found = True
                if len(actual_data[row_nr]) == 0:
                    DataComparer.__print_comparation_result(self, row_nr, 0, "", "", "Row actual data is EMPTY. Row expected data is not PRESENT.")
                else:
                    DataComparer.__print_comparation_result(self, row_nr, 0, actual_data[row_nr][0], "", "Row expected data is not PRESENT.")
                continue
            #
            number_of_columns_actual_data   = len(actual_data[row_nr])
            number_of_columns_expected_data = len(expected_data_including_templates[row_nr])

            number_of_columns = number_of_columns_actual_data if (number_of_columns_actual_data >= number_of_columns_expected_data) else number_of_columns_expected_data

            for column_nr in range(number_of_columns):
                expected_data_including_date_template = None
                expected_data_with_wildcard = None
                skip_exception_rule_used = False
                #
                if column_nr >= number_of_columns_actual_data:
                    difference_found = True
                    DataComparer.__print_comparation_result(self, row_nr, column_nr, "", expected_data_including_templates[row_nr][column_nr], "Column actual data is not PRESENT.")
                    continue
                #
                if column_nr >= number_of_columns_expected_data:
                    difference_found = True
                    DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], "", "Column expected data is not PRESENT.")
                    continue
                #
                if actual_data[row_nr][column_nr] != expected_data_including_templates[row_nr][column_nr]:
                    # If data in actual and expected field doesn't match, check if a template has been used in expected data.
                    match expected_data_including_templates[row_nr][column_nr].upper():
                        case "{PRESENT}":
                            if not actual_data[row_nr][column_nr]:
                                # No data is present in actual data field.
                                difference_found = True
                                DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data_including_templates[row_nr][column_nr], "Actual data field is not PRESENT")
                        #
                        case "{EMPTY}":
                            if actual_data[row_nr][column_nr]:
                                # Actual data field is not empty.
                                difference_found = True
                                DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data_including_templates[row_nr][column_nr], "Actual data field is not EMPTY")
                        #
                        case "{INTEGER}":
                            if not actual_data[row_nr][column_nr].isdigit():
                                # Not positive integer field.
                                difference_found = True
                                DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data_including_templates[row_nr][column_nr], "Actual data field is not INTEGER.")
                        #
                        case _:
                            if "{SKIP}" in expected_data_including_templates[row_nr][column_nr].upper():
                                if expected_data_including_templates[row_nr][column_nr].upper() == "{SKIP}":
                                    # Complete actual data field will be skipped for verification.
                                    pass
                                else:
                                    # Part(s) of the actual data field will be skipped for verification.
                                    # Replace {SKIP}, ignoring cases, by wildcard *.
                                    compiled = re.compile(re.escape("{SKIP}"), re.IGNORECASE)
                                    expected_data_with_wildcard = compiled.sub("*", expected_data_including_templates[row_nr][column_nr])
                                    #
                                    if fnmatch.fnmatch(actual_data[row_nr][column_nr], expected_data_with_wildcard):
                                        skip_exception_rule_used = True
                                    else:
                                        # No match despite using of wildcard(s).
                                        if "{NOW()" not in expected_data_including_templates[row_nr][column_nr].upper():
                                            difference_found = True
                                            DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data_including_templates[row_nr][column_nr], "Actual data field has not been SKIPped.")
                            #
                            if expected_data_with_wildcard is None:
                                # Wildcards not used.
                                expected_data_including_date_template = expected_data_including_templates[row_nr][column_nr]
                            else:
                                expected_data_including_date_template = expected_data_with_wildcard
                            #
                            if "{NOW()" in expected_data_including_templates[row_nr][column_nr].upper():
                                matches = ["NOW():", "NOW()+", "{NOW()-"]
                                if all([x not in expected_data_including_templates[row_nr][column_nr].upper() for x in matches]):
                                    difference_found = True
                                    DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data_including_templates[row_nr][column_nr], "NOW() has been found in expected data field, but format is incorrect.")
                                    continue
                                #
                                expected_data = DataComparer.__replace_date_template_in_expected_data(self, expected_data_including_date_template)
                                #
                                if expected_data == -1:
                                    difference_found = True
                                    DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data_including_templates[row_nr][column_nr], "NOW() has been found in expected data field, but format is incorrect.")
                                else:
                                    if not fnmatch.fnmatch(actual_data[row_nr][column_nr], expected_data):
                                        # No match despite using of wildcard(s).
                                        difference_found = True
                                        DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data_including_templates[row_nr][column_nr], "Date template format displayed. See also next message line.")
                                        DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data, "There is a difference between actual and expected data.")
                                #
                            else:
                                if not skip_exception_rule_used:
                                    # No exceptions.
                                    difference_found = True
                                    DataComparer.__print_comparation_result(self, row_nr, column_nr, actual_data[row_nr][column_nr], expected_data_including_templates[row_nr][column_nr], "There is a difference between actual and expected data. No exception rule has been used.")
                            #
        if difference_found:
            print("\n\n\n")
            raise Exception("There is a difference between actual and expected data. See detail information.")
        else:
            print("There are no differences between actual and expected data found.")
            print("\n\n\n")


    def __replace_date_template_in_expected_data(self, expected_data_field_including_date_template):
        # Replace date_template in expected data.
        # For example: This is text {NOW()-5Y2M1D:YYYY-MM-DD} and also text.  =>  This is text 2018-05-03 and also text.
        position_open_brace_today_text  = expected_data_field_including_date_template.find("{NOW()")
        position_close_brace_today_text = expected_data_field_including_date_template.find("}", position_open_brace_today_text)
        #
        if position_close_brace_today_text == -1:
            return -1
        # Close brace of TODAY has been found.
        #
        expected_datetime_template_string = expected_data_field_including_date_template[position_open_brace_today_text:position_close_brace_today_text + 1]
        expected_datetime_string = DataComparer.__convert_datetime_template_to_datetime(self, expected_datetime_template_string)
        #
        if expected_datetime_string == -1:
            return -1
        # Datetime_template_string has been converted to datetime.
        #
        # Replace expected_datetime_template_string by expected_datetime_string in expected_data_field_including_template.
        compiled = re.compile(re.escape(expected_datetime_template_string), re.IGNORECASE)
        expected_data_with_calculated_date = compiled.sub(expected_datetime_string, expected_data_field_including_date_template)
        #
        return expected_data_with_calculated_date


    def __convert_datetime_template_to_datetime(self, expected_datetime_format):
        # Convert expected datetime template into datetime.
        # For example: {NOW():YYYY-MM-DD}         =>  2023-07-04
        #              {NOW():MMDDYY}             =>  070423
        #              {NOW()-5Y3M1D:D-MMMM-YY}   =>  3-April-18
        #              {NOW()-5Y2M1D:YYYY-MMM-DD} =>  2018-Apr-03
        #              {NOW()-5Y2M1D:YYYYMMDD}    =>  20180503
        #              {NOW()-5Y2M1D:YYYY-M-D}    =>  2018-5-3
        #              {NOW()+2D:DDMMYYYY         =>  06072023
        #              {NOW()-5Y2M1D:YYYY-MM-DD}  =>  2018-05-03
        template_datetime_string_splitted = expected_datetime_format.split(":")
        #
        match len(template_datetime_string_splitted):
            case 2:
                if template_datetime_string_splitted[0] == "{NOW()":
                    # Current date time.
                    expected_datetime = datetime.datetime.now()
                else:
                    # Adjust date time based on current date time.
                    relative_datetime_template_string = template_datetime_string_splitted[0].replace('{NOW()', '')
                    relative_datetime = DataComparer.__convert_relative_datetime_template_to_relative_datetime(self, relative_datetime_template_string[1:len(relative_datetime_template_string)])
                    if relative_datetime == -1:
                        return -1
                    else:
                        match relative_datetime_template_string[0]:
                            case "+":
                                expected_datetime = datetime.datetime.now() + relative_datetime
                            case "-":
                                expected_datetime = datetime.datetime.now() - relative_datetime
                            case _:
                                return -1
            case _:
                return -1
        #
        year = expected_datetime.strftime("%Y")
        year_2_digits = expected_datetime.strftime("%y")
        month = expected_datetime.strftime("%m")
        month_abbreviated = expected_datetime.strftime("%b")
        month_full = expected_datetime.strftime("%B")
        day = expected_datetime.strftime("%d")
        #
        expected_date = template_datetime_string_splitted[1][0:len(template_datetime_string_splitted[1]) - 1].replace("YYYY", year).replace("YY", year_2_digits).replace("MMMM", month_full).replace("MMM", month_abbreviated).replace("MM", month).replace("M", month.lstrip("0")).replace("DD", day).replace("D", day.lstrip("0"))
        return expected_date


    def __convert_relative_datetime_template_to_relative_datetime(self, relative_datetime_str):
        # Convert relative datetime template to relative datetime.
        # For example: 2Y5M1D  =>  2 years, 5 months, 1 day   (used to add or subtract from current moment / date)
        # \d+ means 1 of more digits; search on character - for example Y;
        regex = re.compile(r'((?P<years>\d+?)Y)?((?P<months>\d+?)M)?((?P<days>\d+?)D)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
        period = regex.match(relative_datetime_str)

        if not period:
            return -1

        period = period.groupdict()
        kwargs = {}
        period_names = ["years", "months", "days"]
        #
        for name, param in period.items():
            if param:
                period_name = name
                period_count = param
                #
                if period_name in period_names:
                    kwargs[period_name] = int(period_count)
        #
        if kwargs:
            return dateutil.relativedelta.relativedelta(**kwargs)
        else:
            return -1


    def __print_2d_array(self, title, reader_file_list, column_width):
        max_length_title = 30
        title = title[0:(max_length_title - 1)]
        length_title = len(title)
        print("=== ", title, " ", end="")
        print("=" * (max_length_title - length_title))
        print()
        for row in reader_file_list:
            for cell_value in row:
                if isinstance(cell_value, str):
                    print('{val:{fill}{width}}'.format(val=cell_value, fill='', width=column_width), end="  ")
            print()
        print()
        print()


    def __print_comparation_result(self, row_number, column_number, actual_data, expected_data, error_message):
        print("Row: ", row_number + 1, "  Column: ", column_number + 1, "  =>  Actual data: ", actual_data, "    Expected data: ", expected_data, "    Remark / Error message: ", error_message)

