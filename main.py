import time
from datetime import datetime
import utils
from ac_response_parser import convert_response_to_nested_jsons, convert_nested_jsons_to_flatted_jsons
from excel_writer import results_to_excel
from ac_searcher import Searcher



if __name__ == '__main__':
    max_stops = 1
    origins = ['CUN']
    destinations = ['YVR', 'YYJ', 'YLW', 'YCD', 'YXS', 'YXE', 'YQR', 'YWG', 'YEG', 'YYC']
    start_dt = datetime.strptime('2023-06-10', '%Y-%m-%d')
    end_dt = datetime.strptime('2023-06-10', '%Y-%m-%d')
    dates =  utils.date_range(start_dt, end_dt)
    #  means eco, pre, biz and first
    cabin_class = [
        "ECO",
        "PREM",
        "BIZ",
        "FIRST"
    ]
    price_filter = {
        # 'quota': {
        #     'operator': '>=',
        #     'value': 1
        # },
        # 'cabin_class': {
        #     'operator': 'in',
        #     'value': ['J', 'F']
        # },
        # 'is_mix': {
        #     'operator': '==',
        #     'value': False
        # }
    }
    seg_sorter = {
        'key': 'duration',    # Options 'duration', 'stops', 'departure_time' and 'arrival_time'
                                    # only takes 'duration', 'stops', 'departure_time' and 'arrival_time'.
        'ascending': True
    }
    ac_searcher = Searcher()
    results = []
    nested_jsons_list = []
    for date in dates:
        for ori in origins:
            for des in destinations:
                print(f'search for {ori} to {des} on {date} @ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                response = ac_searcher.search_for(ori, des, date, cabin_class)
                v1 = convert_response_to_nested_jsons(response)
                nested_jsons_list.extend(v1)
                # if there are high volume of network requests, add time.sleep
                time.sleep(2)
    v2 = convert_nested_jsons_to_flatted_jsons(nested_jsons_list, seg_sorter=seg_sorter, price_filter=price_filter)
    results.extend(v2)

    results_to_excel(results, max_stops=max_stops)
