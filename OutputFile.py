import csv

def OutputList(result, filename):
    with open(filename, 'w', encoding = 'utf-8', newline = '') as file:
        writer = csv.writer(file)
        for l in result:
            writer.writerow(l)


# def OutputDicts(result, filename):
#     with open(filename, 'w', encoding = 'utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames = list(result.keys()))
#         writer.writerow(result)


def OutputDict(result, filename):
    with open(filename, 'w', encoding = 'utf-8', newline = '') as file:
        writer = csv.DictWriter(file, fieldnames = list(result[0].keys()))
        writer.writeheader()
        for l in result:
            writer.writerow(l)


def OutputFile(result, filename):
    with open(filename, 'w', encoding = 'utf-8') as file:
        file.write(result)