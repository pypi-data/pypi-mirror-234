from qvin import *


if __name__ == '__main__':

    credentials={
        "server_hostname": "dbc-739ac055-e48a.cloud.databricks.com",
        "http_path": "/sql/1.0/warehouses/774f9262a5ab96e3",
        "access_token": "dapid1616aec4a0cd34fcd055e0f30199e5b"
    }
    vd = QVin(credentials)
    print(vd.lookup_vin(vin='VF1LM1B0H36666155', feature=True))