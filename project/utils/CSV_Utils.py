import csv

class CSVUtils:

    @staticmethod
    def read_data(file_path):
        data = []
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
