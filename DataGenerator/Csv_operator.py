import csv

class CsvOperator:

    def read_csv(self, filename):
        with open(filename, 'r', encoding = 'utf-8') as file:
            csv_reader = csv.reader(file)
            csv_list = [x.strip().strip("'") for y in csv_reader for x in y]
        return csv_list

    def read_dict(self, filename):
        csv_list = []
        with open(filename, 'r', encoding = 'utf-8') as file:
            csv_reader = csv.DictReader(file)
            for l in csv_reader:
                csv_list.append(l)
        return csv_list
    
    def print_csv(self, csv_list, filename):
        with open(filename, 'w', encoding = 'utf-8', newline = '') as file:
            writer = csv.writer(file)
            for l in csv_list:
                writer.writerow(l)

    def print_screen(self, csv_list):
        for l in csv_list:
            print(l)


# CLI 색상 입히기 >> ANSI Color Python