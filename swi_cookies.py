import requests
import urllib.parse
import pandas as pd
import json

headers = {
    '__fetch_req__': 'true',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'addressId=s%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s; deviceId=s%3Acbdd2fbb-cea3-4204-81f2-5f9a69cc963f.a4tUTME4YWm9%2Bek6I7PpOAZFmTCOFqN%2F0dMzHg4N9mU; versionCode=1200; platform=web; subplatform=dweb; statusBarHeight=0; bottomOffset=0; genieTrackOn=false; isNative=false; openIMHP=false; webBottomBarHeight=0; _gcl_au=1.1.726130143.1723454654; _fbp=fb.1.1723454654598.494516705775600464; tid=s%3A67bc1480-fd2c-4242-b0a7-37666618130d.VHX76CZjVDdDbwxyd6gvWk%2B%2F74YPc8RMrNvy9%2FAwtQo; sid=s%3Afiac8232-5c6b-4710-b3b1-52b4b6885967.%2BylWUQpq7PZM5GrA%2FLqLl0yqOhZe1YCboU%2BdJpljNAw; ally-on=false; strId=; LocSrc=s%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y; __SW=jd0GDTYSN2WHgdGk5jMuDG13oqk5ZIBS; _device_id=6018dd4c-31a9-f0b0-7e4c-accdd61b1570; fontsLoaded=1; _gid=GA1.2.1807016463.1723527996; accessibility-enabled=false; dadl=true; _ga_4BQKMMC7Y9=GS1.2.1723528994.1.1.1723529067.60.0.0; lat=s%3A28.5388479.7Qft0y8nQ29XMDLYEOdfQk96d3LrxSpNtZw9KdSSlbo; lng=s%3A77.2753728.6kk5Vmco3Y%2Bq%2BFh2xqojtBjRZxXpHIiK2GIsruyzYGo; address=s%3ANew%20Delhi%2C%20Delhi%20110020%2C%20India.9uEW3ESfMkLEGeQWIWt1B6sLNMPn8k4AK0Wdy1Eir1E; _ga_8N8XRG907L=GS1.1.1723533516.6.1.1723534157.0.0.0; _guest_tid=ef458182-79f7-4b4d-8a29-0fa765b9914f; _sid=fid99c4a-0aad-4e1a-b95c-63692fcba0de; userLocation={%22lat%22:28.5388479%2C%22lng%22:77.2753728%2C%22address%22:%22New%20Delhi%2C%20Delhi%20110020%2C%20India%22%2C%22area%22:%22%22%2C%22showUserDefaultAddressHint%22:false}; _gat_0=1; _ga_34JYJ0BCRN=GS1.1.1723534563.3.0.1723534563.0.0.0; _ga=GA1.1.731672155.1723454655',
    'priority': 'u=1, i',
    'referer': 'https://www.swiggy.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

pincodes = pd.read_excel(r"C:\Users\Admin\PycharmProjects\get_cookies\qc_pincode.xlsx")

collected_data = {}

for pincode in pincodes['pincode']:

    res1 = requests.get(f'https://www.swiggy.com/dapi/misc/place-autocomplete?input={pincode}&types=', headers=headers)
    json_data = res1.json()

    if 'data' in json_data and len(json_data['data']) > 0:
        place_id = json_data['data'][0]['place_id']

        res2 = requests.get(f'https://www.swiggy.com/dapi/misc/address-recommend?place_id={place_id}', headers=headers)
        data = res2.json()

        if 'data' in data and len(data['data']) > 0:
            address = data['data'][0]['formatted_address']
            lat = data['data'][0]['geometry']['location']['lat']
            lng = data['data'][0]['geometry']['location']['lng']

            address_part = f"%7B%22address%22%3A%22{urllib.parse.quote(address)}%22%2C%22"
            userLocation = f'{address_part}lat%22%3A{lat}%2C%22lng%22%3A{lng}%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D'
            lat_ = f's%3A{lat}.7Qft0y8nQ29XMDLYEOdfQk96d3LrxSpNtZw9KdSSlbo'
            lng_ = f's%3A{lng}.6kk5Vmco3Y%2Bq%2BFh2xqojtBjRZxXpHIiK2GIsruyzYGo'

            collected_data[pincode] = {
                "userLocation": userLocation,
                "lat": lat_,
                "lng": lng_
            }
            print("DONE: ", pincode)

output_file = r"swi_cookies.json"
with open(output_file, 'w') as json_file:
    json.dump(collected_data, json_file, indent=4)

print(f"Data collected and saved to {output_file}")
