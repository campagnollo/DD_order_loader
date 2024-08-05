import gspread
from google.oauth2.service_account import Credentials
import yaml

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("/Users/eric.moore/PycharmProjects/dd_schedule_pull/pythonProject/DD_order_loader/credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1knd164TF14LWy3Rq2_vV0jL4VSTWsPiDmnPSKPJSkqM"
sheet = client.open_by_key(sheet_id)


def active_order_list(order_list):
    sites = yaml_reader()
    wsheet_id = sheet.get_worksheet_by_id(sites['active_orders']['wsheet_id'])
    final_list = active_order_list_prep(order_list)
    i = sites['active_orders']["placeholder"]
    i = active_orders_end_finder(i, sites, wsheet_id)
    wsheet_id.insert_rows(final_list, i)

def active_order_list_prep(order_list):
    final_list = []
    temp_list = []
    for i in order_list:
        temp_list.append(i[10])
        temp_list.append(i[9])
        temp_list.append(i[0])
        temp_list.append(i[2])
        temp_list.append(i[11])
        temp_list.append(i[1])
        temp_list.append(i[7])
        temp_list.append(i[5])
        final_list.append(temp_list)
        temp_list = []
    return final_list


def yaml_reader():
    with open(r"/Users/eric.moore/PycharmProjects/dd_schedule_pull/pythonProject/DD_order_loader/sites.yml", "r") as file:
        sites = yaml.safe_load(file)
    return sites


def active_orders_end_finder(i, sites, wsheet_id):
    j = i + 50
    old_place = i
    range_start = f"A{i}:C{j}"
    raw = list(map(lambda x: x.value, wsheet_id.range(range_start)))
    temp_list = []
    check_list = []
    while raw:
        for _ in range(3):
            if raw:
                temp_list.append(raw.pop(0))
        check_list.append(temp_list)
        temp_list = []
    final_list = [x for x in check_list if x[0] != x[1] != x[2]]
    return i + len(final_list)


