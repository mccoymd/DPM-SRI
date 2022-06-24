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
    Strategy,
    DrugCategorizations,
)
from app.utils.enums import DrugCategories, TrialOutcome
from sqlalchemy import or_


def flatten_csv(fileName, new_line_value):
    data = []
    with open(fileName, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            row = line[0]
            cells = row.split(",")

            rowData = []

            tValue = 0
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


def process_file(f, filename, file_id=None):
    if "param" in filename:
        process_param_file(f, file_id)
    elif "stopt" in filename:
        process_stopt_file(f)
    elif "dosage" in filename:
        process_dosage_file(f)
    elif "pop" in filename:
        process_pop_file(f)
    else:
        print("Unable to process file")


def process_param_file(f, file_id=None):
    has_header = file_has_header(f)

    with open(f, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        if has_header:
            next(reader)

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

            params = Parameters(
                growth_rate,
                population_obj.id,
                transition_obj.id,
                sensitivities_obj.id,
                parameter_id,
                file_id,
            )
            db_commit(params)


def process_stopt_file(f):
    has_header = file_has_header(f)

    with open(f, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        if has_header:
            next(reader)

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
        row[0] = int(row[0]) + 1  # increment paramater id to start at 1 rather than 0

        dosage = DrugDosages(*row)
        db_commit(dosage)


def process_pop_file(f):
    data = flatten_csv(f, 4)

    for row in data:
        row[0] = int(row[0]) + 1  # increment paramater id to start at 1 rather than 0

        populations = Populations(*row)
        db_commit(populations)


def process_strategies_file(f):
    has_header = file_has_header(f)

    with open(f, "r") as f:
        reader = csv.reader(f, delimiter=",")
        if has_header:
            next(reader)

        for line in reader:
            cells = line[1:]
            db_commit(Strategy(*cells))


def process_drug_categorizations():
    # These values are pulled from the DB and may need to be modified
    STANDARD_STRATEGY_ID = 1
    DPM_STRATEGY_ID = 2

    # TODO: This query needs to be refined so it only runs for dosages that haven't already been used
    dosages = (
        db.session.query(DrugDosages)
        .filter(
            or_(
                DrugDosages.strategy_id == STANDARD_STRATEGY_ID,
                DrugDosages.strategy_id == DPM_STRATEGY_ID,
            )
        )
        .filter(or_(DrugDosages.t == 0, DrugDosages.t == 45))
        .all()
    )

    time_dict = {}
    for dosage in dosages:
        if dosage.t == 0:
            time_dict.setdefault((0, dosage.parameter_id), []).append(dosage)
        elif dosage.t == 45:
            time_dict.setdefault((45, dosage.parameter_id), []).append(dosage)

    results_dict = {}
    for key, dosages in time_dict.items():
        parameter_id = key[1]

        if parameter_id not in results_dict:
            results_dict[parameter_id] = {
                DrugCategories.STANDARD_T0: None,
                DrugCategories.DPM_T0: None,
                DrugCategories.STANDARD_T45: None,
                DrugCategories.DPM_T45: None,
            }

        inner_dict = results_dict[parameter_id]

        if key[0] == 0:
            for dosage in dosages:
                if dosage.strategy_id == STANDARD_STRATEGY_ID:
                    inner_dict[DrugCategories.STANDARD_T0] = dosage
                elif dosage.strategy_id == DPM_STRATEGY_ID:
                    inner_dict[DrugCategories.DPM_T0] = dosage

        elif key[0] == 45:
            for dosage in dosages:
                if dosage.strategy_id == STANDARD_STRATEGY_ID:
                    inner_dict[DrugCategories.STANDARD_T45] = dosage
                elif dosage.strategy_id == DPM_STRATEGY_ID:
                    inner_dict[DrugCategories.DPM_T45] = dosage

    for parameter_id, dosages in results_dict.items():
        standard_t0 = dosages[DrugCategories.STANDARD_T0]
        dpm_t0 = dosages[DrugCategories.DPM_T0]
        standard_t45 = dosages[DrugCategories.STANDARD_T45]
        dpm_t45 = dosages[DrugCategories.DPM_T45]

        if (standard_t0.drug_1 == dpm_t0.drug_1) and (
            standard_t0.drug_2 == dpm_t0.drug_2
        ):
            if (standard_t45.drug_1 == dpm_t45.drug_1) and (
                standard_t45.drug_2 == dpm_t45.drug_2
            ):
                create_drug_categorization(
                    standard_t0.id,
                    dpm_t0.id,
                    standard_t45.id,
                    dpm_t45.id,
                    TrialOutcome.BOTH_SAME,
                )
            else:
                create_drug_categorization(
                    standard_t0.id,
                    dpm_t0.id,
                    standard_t45.id,
                    dpm_t45.id,
                    TrialOutcome.FIRST_SAME,
                )
        else:
            if (standard_t45.drug_1 == dpm_t45.drug_1) and (
                standard_t45.drug_2 == dpm_t45.drug_2
            ):
                create_drug_categorization(
                    standard_t0.id,
                    dpm_t0.id,
                    standard_t45.id,
                    dpm_t45.id,
                    TrialOutcome.SECOND_SAME,
                )
            else:
                create_drug_categorization(
                    standard_t0.id,
                    dpm_t0.id,
                    standard_t45.id,
                    dpm_t45.id,
                    TrialOutcome.NONE_SAME,
                )


def create_drug_categorization(
    standard_t0_id, dpm_t0_id, standard_t45_id, dpm_t45_id, category
):
    category = DrugCategorizations(
        standard_t0_id, dpm_t0_id, standard_t45_id, dpm_t45_id, category
    )
    db_commit(category)


def db_commit(*data):
    try:
        for item in data:
            db.session.add(item)
        db.session.commit()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        db.session.rollback()


def file_has_header(f):
    with open(f, "r") as f:
        reader = csv.reader(f)
        row1 = next(reader)
        return not any(cell.isdigit() for cell in row1)
