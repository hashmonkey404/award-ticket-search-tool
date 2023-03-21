from datetime import datetime
from typing import List

import requests

import utils
from flight_filter import filter_price
from flight_sorter import sort_segs

def ac_response_parse(response: requests.Response, 
                      seg_sorter: dict = None,
                      price_filter: dict = {}) -> list:
    return convert_nested_jsons_to_flatted_jsons(convert_response_to_nested_jsons(response), seg_sorter, price_filter)

def convert_response_to_nested_jsons(response: requests.Response) -> List: # list of JSON/dict
    """
    Convert response from ac_searcher POST request. 
    Return: List of nested json. Each json means an itinerary with one fare.
    """
    if response.status_code != 200:
        return list()
    else:
        json_data = response.json() # return python dict {data: , dictionaries: }
        air_bounds_group_list = json_data.get('data', {}).get('airBoundGroups', []) if json_data is not None else []
        flights_info_dict = json_data.get('dictionaries', {}).get('flight', {}) if json_data is not None else {}
        
        results = []

        fare_class_dict = {
            'STANDARD': 'Std', # cabin: eco, bookingClass: K X
            'FLEX': 'Flex', # cabin: eco, bookingClass: K X
            'LATITUDE': 'Lat', # cabin: eco, bookingClass: K X

            'PYLOW': 'PY Low', # cabin: ecoPremium, bookingClass: A
            'PYFLEX': 'PY Flex', # cabin: ecoPremium, bookingClass: A

            'EXECLOW': 'J Low', # cabin: business, bookingClass: P
            'EXECFLEX': 'J Flex', # cabin: business, bookingClass: P

            'FIRSTLOW': 'F Low', #cabin: , bookingClass: 
        }
        cabin_class_dict = {'eco': 'Y', 'ecoPremium':'PY', 'business':'J', 'first':'F'}
        partner_saver_class_list = ['X', 'I', 'O']

        for bound_group in air_bounds_group_list:
            bound_group = dict(bound_group) # one itinerary with all fares

            segs_raw = [seg_json for seg_json in bound_group['boundDetails']['segments']] # example - [{'flightId': 'SEG-AC933-CUNYVR-2023-06-10-1710'}, 'connectionTime':]
            air_bounds_raw = [bound_json for bound_json in bound_group['airBounds']] # different fares on same route
            
            segs = [] # list of every segment flight info of each itinerary

            for seg in segs_raw:
                flight_info = flights_info_dict[seg['flightId']]
                temp = {
                    'connection_time': seg.get('connectionTime', 0),
                    'flight_number': flight_info['marketingAirlineCode'] + f"{flight_info['marketingFlightNumber']:>6}",
                    'aircraft': flight_info['aircraftCode'],
                    'departure_location': flight_info['departure']['locationCode'],
                    'departure_time': flight_info['departure']['dateTime'],
                    'arrival_location': flight_info['arrival']['locationCode'],
                    'arrival_time': flight_info['arrival']['dateTime'],
                    'flight_time': flight_info['duration'],
                    'departure_days_diff': seg.get('departureDaysDifference', 0),
                    'arrival_days_diff': seg.get('arrivalDaysDifference', 0)
                }
                segs.append(temp)

            stop_count = len(segs_raw) - 1
            duration = bound_group['boundDetails']['duration']

            prices = []
            for air_bound in air_bounds_raw:
                temp = {
                    'fare_class': fare_class_dict[air_bound['fareFamilyCode']],
                    'cabin_class': [cabin_class_dict[x['cabin']] for x in air_bound['availabilityDetails']],
                    # 'r_space': ,
                    'quotas': [x['quota'] for x in air_bound['availabilityDetails']],
                    'miles': air_bound['airOffer']['milesConversion']['convertedMiles']['base'],
                    'cash': air_bound['airOffer']['milesConversion']['convertedMiles']['totalTaxes'],
                    'is_mix': air_bound.get('isMixedCabin', False),
                    'mix_detail': utils.convert_mix(air_bound['availabilityDetails']) if air_bound.get('isMixedCabin', False) else ""
                }
                prices.append(temp)

            v = {
                'segments': segs,
                'stops': stop_count,
                'duration': duration,
                'prices': prices
            }

            results.append(v)
        return results


def convert_nested_jsons_to_flatted_jsons(origin_results: list,
                                          seg_sorter: dict = None,
                                          price_filter: dict = {}) -> list:

    sorted_results = sort_segs(origin_results, seg_sorter)
    # sorted_results = origin_results

    flatted_results = []

    for result in sorted_results:
        segs = result['segments']
        itinerary_single = {
            'Flight Time': '\n'.join(utils.convert_datetime(x['departure_time'], with_date = True) + 
                                     '-' + utils.convert_datetime(x['arrival_time'], with_date = False) +
                                     ((' +' + str(x['arrival_days_diff'] - x['departure_days_diff']))
                                        if x['arrival_days_diff'] - x['departure_days_diff'] > 0 else '') +
                                     ' ('+ utils.convert_duration(x['flight_time']) +')' for x in segs),

            'Route': '\n'.join([x['departure_location'] + ' - ' + x['arrival_location'] for x in segs]),

            'Flight': '\n'.join([x['flight_number'] for x in segs]),
            # 'Cabin': '\n'.join(),
            'Aircraft': '\n'.join([str(x['aircraft']) for x in segs]),
            # 'departure_time': utils.convert_datetime(segs[0]['departure_time']),
            # 'arrival_time': utils.convert_datetime(segs[-1]['arrival_time']),
            'Stops': str(result['stops']) if result['stops'] != 0 else '',
            
            'Duration': utils.convert_duration(result['duration']),
        }

        prices = result['prices']
        prices_filtered = filter_price(prices, price_filter)

        """If there is no filtered price, ignore current"""
        if len(prices_filtered) == 0:
            continue
        for pf in prices_filtered:
            price_single = {
                'Cabin': '\n'.join(x for x in pf['cabin_class']),
                'Quota': '\n'.join([str(x) if x < 9 else '9+' for x in pf['quotas']]),
                'Fare Class': pf['fare_class'],
                'Miles': utils.convert_miles(pf['miles']),
                # 'Cost': utils.convert_miles(pf['miles']) + '\n' + utils.convert_cash(pf['cash']),
                'Tax/Fee': utils.convert_cash(pf['cash']),
                'Mixed': 'Yes' if pf['is_mix'] == True else '',
                'Mix Detail': pf['mix_detail'],
            }
            flatted_results.append({**itinerary_single, **price_single})

    return flatted_results

