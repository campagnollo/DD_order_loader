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


def order_pull():
    sites = yaml_reader()
    wsheet_id = sheet.get_worksheet_by_id(sites['sweetgreen']["wsheet_id"])
    i = sites['sweetgreen']["placeholder"]
    order_list, new_place = data_presense(i, wsheet_id, sites, 'sweetgreen')
    sites['sweetgreen']["placeholder"] = new_place
    with open(r"/Users/eric.moore/PycharmProjects/dd_schedule_pull/pythonProject/DD_order_loader/sites.yml", "w") as file:
        yaml.dump(sites, file)
    return order_list


def data_presense(i, wsheet_id, sites, store):
    j = i + 30
    old_place = i
    range_start1 = f"A{i}:J{j}"
    raw = list(map(lambda x: x.value, wsheet_id.range(range_start1)))
    p = 0
    while p < len(raw):
        if raw[p] == '':
            del raw[p:p + 10]
        else:
            p += 10
    record_list = []
    final_list = []
    while len(raw) > 0:
        for h in range(0, 10):
            record_list.append(raw.pop(0))
        record_list.append(sites[store]['dri'])
        record_list.append(sites[store]['time_zone'])
        final_list.append(record_list)
        record_list = []
    new_place = len(final_list) + old_place
    return final_list, new_place

def yaml_reader():
    with open(r"/Users/eric.moore/PycharmProjects/dd_schedule_pull/pythonProject/DD_order_loader/sites.yml", "r") as file:
        sites = yaml.safe_load(file)
    return sites