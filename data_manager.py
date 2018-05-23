import csv


def import_data_from_file(filename):
    '''
    Opens file defined in filename
    Returns list of dicts
    '''
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row)
    return data
