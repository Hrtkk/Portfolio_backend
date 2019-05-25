import csv
import pandas
DIR = '/home/hritik/Projects/HRKProject/Zettamine/Portfolio_backend/flaskr/CleanedData/'
#
custDb = pandas.read_csv(DIR + 'CustomerDb.csv')
tranDb = pandas.read_csv(DIR + 'HolidayNYSE.csv')
holyDb = pandas.read_csv(DIR + 'StockTransactions.csv')
tickDb = pandas.read_csv(DIR + 'ticker.csv')

print(custDb)

# with open('./CustomerDb.csv', mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column name are {", ".join(row)}')
#             line_count += 1
#         print(f'\t{row["name"]} worlds in the {row["dep"]}')
#         line_count += 1
#     print(f'Processes {line_count} lines.')
#
#
# with open('HolidayNYSE.csv', mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column name are {", ".join(row)}')
#             line_count += 1
#         print(f'\t{row["name"]} worlds in the {row["dep"]}')
#         line_count += 1
#     print(f'Processes {line_count} lines.')
#
#
# with open('StockTransactions.csv', mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column name are {", ".join(row)}')
#             line_count += 1
#         print(f'\t{row["name"]} worlds in the {row["dep"]}')
#         line_count += 1
#     print(f'Processes {line_count} lines.')
#
#
# with open('ticker', mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column name are {", ".join(row)}')
#             line_count += 1
#         print(f'\t{row["name"]} worlds in the {row["dep"]}')
#         line_count += 1
#     print(f'Processes {line_count} lines.')
