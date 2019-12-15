import openpyxl


# Constants:


PRODUCT_MASS = ['30', '25', '20', '18', '14', '10', '7', '5', '2']

PNE = 'Ошибка валидации телефонного номера'

MNE = 'Ошибка валидации имени'

PME = 'Ошибка получения массы продукта, нет соответсвия стандартным значениям'

PCE = 'Отсутсвует код продукта'

PTE = 'Ошибка в значении тоннажа'

PQE = 'Ошибка деления тоннажа на массу продукта, получается не целое число'


# File generators:


def generate_report(work_sheet, bonus_count):
    errors_list = []
    iteration = 1
    new_phone_number = True
    new_manager_name = True
    report = openpyxl.Workbook()
    report_work_sheet = report.active

    while True:
        cell_A = work_sheet[f'A{iteration}'].value
        cell_B = work_sheet[f'B{iteration}'].value
        cell_C = work_sheet[f'C{iteration}'].value

        if new_phone_number:
            if validate_phone_number(cell_A):
                report_work_sheet[f'A{iteration}'] = cell_A
                iteration += 1
                new_phone_number = False
                continue
            else:
                errors_list.append((
                    work_sheet[f'A{iteration}'].row,
                    cell_A,
                    work_sheet[f'A{iteration}'].coordinate,
                    PNE))
                iteration += 1
                continue

        if new_manager_name:  # TODO Свалидировать имя менеджера
            report_work_sheet[f'A{iteration}'] = cell_A
            iteration += 1
            new_manager_name = False
            continue

        if not cell_A:
            if work_sheet[f'A{iteration + 1}'].value:
                new_phone_number = True
                new_manager_name = True
                iteration += 1
                continue
            else:
                break

        product_mass = get_product_mass(cell_A)
        kilograms_from_tons = get_kilograms_from_tons(cell_C)

        if not product_mass:
            errors_list.append((
                work_sheet[f'A{iteration}'].row,
                cell_A,
                work_sheet[f'A{iteration}'].coordinate,
                PME
            ))
            iteration += 1
            continue

        if not cell_B:
            errors_list.append((
                work_sheet[f'B{iteration}'].row,
                cell_B,
                work_sheet[f'B{iteration}'].coordinate,
                PCE
            ))
            iteration += 1
            continue

        if not kilograms_from_tons:
            errors_list.append((
                work_sheet[f'C{iteration}'].row,
                cell_C,
                work_sheet[f'C{iteration}'].coordinate,
                PTE
            ))
            iteration += 1
            continue

        product_count = kilograms_from_tons / product_mass

        if product_count - int(product_count):
            errors_list.append((
                work_sheet[f'C{iteration}'].row,
                cell_C,
                work_sheet[f'C{iteration}'].coordinate,
                PQE
            ))
            iteration += 1
            continue

        report_work_sheet[f'A{iteration}'] = cell_A
        report_work_sheet[f'B{iteration}'] = cell_B
        report_work_sheet[f'C{iteration}'] = cell_C
        report_work_sheet[f'D{iteration}'] = product_count
        report_work_sheet[f'E{iteration}'] = product_mass
        report_work_sheet[f'F{iteration}'] = product_count * bonus_count

        iteration += 1

    return report if not errors_list else errors_list


# Supporting:

def get_kilograms_from_tons(tons):
    try:
        kilograms = float(tons) * 1000
    except ValueError:
        return False
    return kilograms


def get_work_sheet(request):
    try:
        excel_file = request.FILES.get('file')
        work_book = openpyxl.load_workbook(excel_file)
        first_sheet = work_book.get_sheet_names()[0]
        work_sheet = work_book.get_sheet_by_name(first_sheet)
    except Exception:
        return False
    return work_sheet


def get_product_mass(string):
    mass = str()

    for symbol in string:
        if symbol.isdigit():
            mass += symbol
        if mass and not symbol.isdigit():
            if mass not in PRODUCT_MASS:
                mass = ''
            if mass in PRODUCT_MASS:
                return int(mass)
    return False


def validate_phone_number(phone_number):  # TODO
    pass
