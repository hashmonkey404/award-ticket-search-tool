# award-ticket-search-tool
This tool facilitates award ticket search process, it currently supports Air Canada (Aeroplan) only.

## User Guide
1. install requirements
```
pip install -r requirements.txt
```
2. In main.py set the conditions you want.
```python
    max_stops = 2
    origins = ['PVG','HKG']
    destinations = ['YVR','YYZ']
    start_dt = datetime.strptime('2023-09-29', '%Y-%m-%d')
    end_dt = datetime.strptime('2023-09-29', '%Y-%m-%d')
    dates = date_range(start_dt, end_dt)
    #  means eco, pre, biz and first
    cabin_class = [
        "ECO",
        "PREM",
        "BIZ",
        "FIRST"
    ]
    price_filter = {
        'quota': {
            'operator': '>=',
            'value': 1
        },
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
        'key': 'duration',  # only takes 'duration', 'stops', 'departure_time' and 'arrival_time'.
        'ascending': True
    }
```
3.Run main.py and you will see the output file.

<a href="https://www.buymeacoffee.com/hashmonkey"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a beer&emoji=🍺&slug=hashmonkey&button_colour=5F7FFF&font_colour=ffffff&font_family=Bree&outline_colour=000000&coffee_colour=FFDD00" /></a>
