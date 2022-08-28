from pkgutil import get_data
import pandas
import json

class SHEET:
    def __init__(self, state):
        self.state = state
        self.get_data()
    
    # Get data from google sheet
    def get_data(self):
        if self.state == True:
            sheet_id = ""
            sheet_name = ""
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
            excel_data_df = pandas.read_csv(url)
            thisisjson = excel_data_df.to_json(orient='records')
            print('Excel Sheet to JSON: Success')
            thisisjson_dict = json.loads(thisisjson)
            with open('data.json', 'w') as json_file:
                json.dump(thisisjson_dict, json_file)