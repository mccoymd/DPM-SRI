import sys
import csv
import traceback
from app import db, models
from app.models import (
    Parameters,
    Populations,
    DrugDosages,
    StoppingTimes,
    InitialPopulations,
    DrugSensitivities,
    TransitionRates,
)


def flatten_csv(fileName, new_line_value):
    data = []
    with open(fileName, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            row = line[0]
            cells = row.split(",")

            rowData = []

            tValue = 45
            parameterId = int(cells[0]) + 1
            strategyId = int(cells[1]) + 1
            counter = 0

            rowData.append(parameterId)
            rowData.append(strategyId)
            rowData.append(tValue)

            for index, cell in enumerate(cells[2:]):
                rowData.append(cell)
                counter += 1

                if counter == new_line_value:
                    rowCopy = rowData.copy()
                    data.append(rowCopy)
                    rowData.clear()
                    tValue += 45
                    if tValue > 1800:
                        break
                    rowData.append(parameterId)
                    rowData.append(strategyId)
                    rowData.append(tValue)
                    counter = 0

            data.append(rowData)

    results = [x for x in data if x != []]
    return results


def write_csv(writeFileName, data, headers=None):
    with open(writeFileName, "w") as f:
        writer = csv.writer(f)
        if headers is not None:
            writer.writerow(headers)
        writer.writerows(data)


def convert_txt(inputFile, outputFile):
    with open(inputFile, "r") as f:
        stripped = (line.strip() for line in f)
        lines = (line.split(" ") for line in stripped if line)

        with open(outputFile, "w") as out:
            writer = csv.writer(out)
            writer.writerows(lines)


def process_file(f, filename):
    if "param" in filename:
        process_param_file(f)
    elif "stopt" in filename:
        process_stopt_file(f)
    elif "dosage" in filename:
        process_dosage_file(f)
    elif "pop" in filename:
        process_pop_file(f)
    else:
        print("Unable to process file")


def process_param_file(f):
    with open(f, "r") as f:
        #has_header = file_has_header(f)
        #if has_header:
        #    next(f)

        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            row = line[0]
            cells = row.split(",")

            parameter_id = int(cells[0]) + 1
            initial_populations = cells[1:5]
            growth_rate = cells[5]
            drug_sensitivities = cells[6:14]
            transition_rates = cells[14:]

            population_obj = InitialPopulations(*initial_populations)
            transition_obj = TransitionRates(*transition_rates)
            sensitivities_obj = DrugSensitivities(*drug_sensitivities)

            db_commit(population_obj)
            db_commit(transition_obj)
            db_commit(sensitivities_obj)

            params = Parameters(growth_rate, population_obj.id, transition_obj.id, sensitivities_obj.id, parameter_id)
            db_commit(params)

def process_stopt_file(f):
    with open(f, "r") as f:
        has_header = file_has_header(f)
        if has_header:
            next(f)

        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            row = line[0]
            cells = row.split(",")

            cells[0] = (
                int(cells[0]) + 1
            )  # increment paramater id to start at 1 rather than 0

            time = StoppingTimes(*cells)
            db_commit(time)


def process_dosage_file(f):
    data = flatten_csv(f, 2)

    for row in data:
        row[0] = (
            int(row[0]) + 1
        )  # increment paramater id to start at 1 rather than 0

        dosage = DrugDosages(*row)
        db_commit(dosage)


def process_pop_file(f):
    data = flatten_csv(f, 4)

    for row in data:
        row[0] = (
            int(row[0]) + 1
        )  # increment paramater id to start at 1 rather than 0

        populations = Populations(*row)
        db_commit(populations)


def db_commit(*data):
    try:
        for item in data:
            db.session.add(item)
        db.session.commit()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)


def file_has_header(f):
    try:
        return csv.Sniffer().has_header(f.read(1024))
    except:
        return False
