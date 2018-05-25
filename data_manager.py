import csv


def import_data_from_file(filename):
    '''
    Opens file defined in filename
    Returns list of dicts
    '''
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        return None


def import_header(filename):
    ''' 
    Opens file and import header for csv dictwriter
    '''
    with open(filename) as datafile:
        lines = []
        for data in datafile:
            lines.append(data)
    return lines[0].strip("\n").split(",")


def export_data_to_file(filename, data):
    '''
    Opens file to write, and writes data as csv file
    Args:
    filename - patch and filename
    data - list of dicts
    '''
    fieldnames = import_header(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in data:
            writer.writerow(line)
