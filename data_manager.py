import csv
import connection_handler


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
        csvfile.close()
        return data
    except FileNotFoundError:
        print("File not found")
        return {"message": "File not found"}
    except OSError:
        print("OS Error")
        return {"message": "OS Error"}


@connection_handler.connection_handler
def import_data_from_db(cursor, qa):
    if qa == "q":
        cursor.execute("""
                        SELECT * from question
                        """)
        data = cursor.fetchall()
        return data
    if qa == "a":
        cursor.execute("""
                        SELECT * from answer
                        """)
        data = cursor.fetchall()
        return data


def import_header(filename):
    '''
    Opens file and import header for csv dictwriter
    '''
    try:
        with open(filename) as datafile:
            lines = []
            for data in datafile:
                lines.append(data)
        return lines[0].strip("\n").split(",")
    except FileNotFoundError:
        print("File not found")
        return {"message": "File not found"}
    except OSError:
        print("OS Error")
        return {"message": "OS Error"}


def export_data_to_file(filename, data):
    '''
    Opens file to write, and writes data as csv file
    Args:
    filename - patch and filename
    data - list of dicts
    '''
    fieldnames = import_header(filename)
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for line in data:
                writer.writerow(line)
    except FileNotFoundError:
        print("File not found")
        return {"message": "File not found"}
    except OSError:
        print("OS Error")
        return {"message": "OS Error"}
