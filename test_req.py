import os

import requests
import json

# .airbnb.com$ElzxlrV2huQ$xJ5MD3DoXWevk1TL-B_5MsSGlsb3aZMdXw7EOt92KwE= = os.getenv('.airbnb.com$ElzxlrV2huQ$xJ5MD3DoXWevk1TL-B_5MsSGlsb3aZMdXw7EOt92KwE=')

cookies = {
    'bev': '1645828675_ZTc1YWVjMWQ4MzI5',
    '_abck': 'D1D79E50FC84F6B90D9C1F3977CB21F3~-1~YAAQH24cuDPI+heCAQAArEApIwhpiXLslMQaEskWdWjbLawkFA6Gc1Px+ML5LZc26SLzBhDry+nrLHrSpCddU7G5Lfg8EVNvXPIok7s1umT8r97HH6B6ZUZE28jKT5glhOBjD6kP2Vp6LlPdYyMbMR8oX3oVm38j/aX3ibMBQ8lB3IZfxZEK1IxPAhVivxzfb1H68rcKbOyW+VvjnsrVO1bV7a0A1/ja1XQRpQwFLHUVkzV/RuIEMWcQ2NE+lkm3rPFh47D0NxSl4XqkzkdkfZ1L4C7OUpnBWZptzLpbVg2XNCRAqiN3H5ICah8rXv2uFUeTjr2Uk2JJ1b53lpjMSYE4EuqJNk5Gp/bFqYszvfWaA5QhsngHEP14nrJX4opRTX+t36keugzfqi4k86hNDxiYO1o+jXThvg==~-1~-1~-1',
    'everest_cookie': '1667947986.O172i6MAmFaNpROXrb5s.MYF144HIWy3KYuQfTrwbK8Wzlk1Be3gUVUQgRlNQop0',
    'country': 'US',
    'cdn_exp_2ab78baeda6c3fe9c': 'treatment',
    'cdn_exp_e34f8847ee4f0c14f': 'treatment',
    'ak_bmsc': 'F3DD2744DCA522BD2AF0565A6D41B840~000000000000000000000000000000~YAAQxv3aFzwoJDWEAQAAo35yWRFqoeE+k4LIUCpuzMsx0xJxTrLZ9xSNWYksvgOsC7/7VKji5S0rxPeNzufD7U21JKAi6fPjG6rytBngJGAUdPvckLvFp/5I0ML5uB+vTW4kiaCSA0cXD11MXPjyMKwM3f/BTapgUNjkd+0qWij9dy2lwlJoj5DPjAKJV+o16eFFWptSlseGkcBVWB4C5t6vhqUmYEldFNe/9PouauUdwES1Wmz0AzlV8UZhzb1jWtWdqoFNZwk2hXeHEefmiYaAWuomzOS6u1/Hbz+Aj0Vq7xREGNphfjj6ZJDuf6pQuB7q7eohV7q1bDo1q1ChKnEmX3qAuBXiZ5HanAvlKIhFwVD2NAFTzJuJZdB4SrSIUHX7eV64/ky0o0c=',
    '_csrf_token': 'V4%24.airbnb.com%24ElzxlrV2huQ%24xJ5MD3DoXWevk1TL-B_5MsSGlsb3aZMdXw7EOt92KwE%3D',
    'jitney_client_session_id': 'ce6dc5b5-7a24-41e3-a7c5-6f198cd53e03',
    'jitney_client_session_created_at': '1667947986',
    'flags': '0',
    'OptanonAlertBoxClosed': 'NR',
    'tzo': '-300',
    'frmfctr': 'wide',
    '_gcl_au': '1.1.1343832408.1667947987',
    'AMP_TOKEN': '%24NOT_FOUND',
    '_gid': 'GA1.2.522684526.1667947988',
    'cfrmfctr': 'DESKTOP',
    'cbkp': '4',
    'previousTab': '%7B%22id%22%3A%221af32782-8dc5-491f-b960-1ffc472d257f%22%2C%22url%22%3A%22https%3A%2F%2Fwww.airbnb.com%2Frooms%2F134238%3Fadults%3D1%26category_tag%3DTag%253A8536%26children%3D0%26infants%3D0%26search_mode%3Dflex_destinations_search%26check_in%3D2023-01-11%26check_out%3D2023-01-17%26federated_search_id%3D3b667d77-ae15-4f21-930a-ddcdf0a046ee%26source_impression_id%3Dp3_1667948539_QD7zmlrahlewwCFE%22%7D',
    '_gat': '1',
    '_user_attributes': '%7B%22curr%22%3A%22USD%22%2C%22enable_auto_translate%22%3Afalse%2C%22guest_exchange%22%3A1.0%2C%22device_profiling_session_id%22%3A%221645828675--dad67b3d1d514e70d4e4d39a%22%2C%22giftcard_profiling_session_id%22%3A%221667947986--6145be05d2eb368f5164185a%22%2C%22reservation_profiling_session_id%22%3A%221667947986--adc1692e30cd8668c2f67793%22%7D',
    'jitney_client_session_updated_at': '1667950341',
    '_ga_2P6Q8PGG16': 'GS1.1.1667947987.21.1.1667950341.51.0.0',
    '_ga': 'GA1.1.28538937.1645828676',
    '_uetsid': '1c9f4ef05fb811ed90a42d17c31d99e4',
    '_uetvid': '93c35a50968b11ecb2c259648f5ad98d',
    'bm_sv': '96C45E59886438CD6ABF39A6A66920E4~YAAQBP4xFxa6mDWEAQAAqW2WWRFFA7+XMBg9VOtjetVnBufMkBO1btrcNAdTNs0vA543NbQEGSpTtPGftSbc7jy1uh1r5Mr0JWF5PDFpVQ9wuM8Z7nMfY8UwLmZyiidgaWWo8lwz+v8XXasMzN41XupBzDZo2ugLU1aLaD2mIkqwa+W6NPE21hFYWYQMM2H8zvDGDe1C+7QVGQC4kWmjCf5XtDER7h7DrOiWTh2vgFCtxNKBqGP6onln/kGfbh1LGw==~1',
}

headers = {
    'authority': 'www.airbnb.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'bev=1645828675_ZTc1YWVjMWQ4MzI5; _abck=D1D79E50FC84F6B90D9C1F3977CB21F3~-1~YAAQH24cuDPI+heCAQAArEApIwhpiXLslMQaEskWdWjbLawkFA6Gc1Px+ML5LZc26SLzBhDry+nrLHrSpCddU7G5Lfg8EVNvXPIok7s1umT8r97HH6B6ZUZE28jKT5glhOBjD6kP2Vp6LlPdYyMbMR8oX3oVm38j/aX3ibMBQ8lB3IZfxZEK1IxPAhVivxzfb1H68rcKbOyW+VvjnsrVO1bV7a0A1/ja1XQRpQwFLHUVkzV/RuIEMWcQ2NE+lkm3rPFh47D0NxSl4XqkzkdkfZ1L4C7OUpnBWZptzLpbVg2XNCRAqiN3H5ICah8rXv2uFUeTjr2Uk2JJ1b53lpjMSYE4EuqJNk5Gp/bFqYszvfWaA5QhsngHEP14nrJX4opRTX+t36keugzfqi4k86hNDxiYO1o+jXThvg==~-1~-1~-1; everest_cookie=1667947986.O172i6MAmFaNpROXrb5s.MYF144HIWy3KYuQfTrwbK8Wzlk1Be3gUVUQgRlNQop0; country=US; cdn_exp_2ab78baeda6c3fe9c=treatment; cdn_exp_e34f8847ee4f0c14f=treatment; ak_bmsc=F3DD2744DCA522BD2AF0565A6D41B840~000000000000000000000000000000~YAAQxv3aFzwoJDWEAQAAo35yWRFqoeE+k4LIUCpuzMsx0xJxTrLZ9xSNWYksvgOsC7/7VKji5S0rxPeNzufD7U21JKAi6fPjG6rytBngJGAUdPvckLvFp/5I0ML5uB+vTW4kiaCSA0cXD11MXPjyMKwM3f/BTapgUNjkd+0qWij9dy2lwlJoj5DPjAKJV+o16eFFWptSlseGkcBVWB4C5t6vhqUmYEldFNe/9PouauUdwES1Wmz0AzlV8UZhzb1jWtWdqoFNZwk2hXeHEefmiYaAWuomzOS6u1/Hbz+Aj0Vq7xREGNphfjj6ZJDuf6pQuB7q7eohV7q1bDo1q1ChKnEmX3qAuBXiZ5HanAvlKIhFwVD2NAFTzJuJZdB4SrSIUHX7eV64/ky0o0c=; _csrf_token=V4%24.airbnb.com%24ElzxlrV2huQ%24xJ5MD3DoXWevk1TL-B_5MsSGlsb3aZMdXw7EOt92KwE%3D; jitney_client_session_id=ce6dc5b5-7a24-41e3-a7c5-6f198cd53e03; jitney_client_session_created_at=1667947986; flags=0; OptanonAlertBoxClosed=NR; tzo=-300; frmfctr=wide; _gcl_au=1.1.1343832408.1667947987; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.522684526.1667947988; cfrmfctr=DESKTOP; cbkp=4; previousTab=%7B%22id%22%3A%221af32782-8dc5-491f-b960-1ffc472d257f%22%2C%22url%22%3A%22https%3A%2F%2Fwww.airbnb.com%2Frooms%2F134238%3Fadults%3D1%26category_tag%3DTag%253A8536%26children%3D0%26infants%3D0%26search_mode%3Dflex_destinations_search%26check_in%3D2023-01-11%26check_out%3D2023-01-17%26federated_search_id%3D3b667d77-ae15-4f21-930a-ddcdf0a046ee%26source_impression_id%3Dp3_1667948539_QD7zmlrahlewwCFE%22%7D; _gat=1; _user_attributes=%7B%22curr%22%3A%22USD%22%2C%22enable_auto_translate%22%3Afalse%2C%22guest_exchange%22%3A1.0%2C%22device_profiling_session_id%22%3A%221645828675--dad67b3d1d514e70d4e4d39a%22%2C%22giftcard_profiling_session_id%22%3A%221667947986--6145be05d2eb368f5164185a%22%2C%22reservation_profiling_session_id%22%3A%221667947986--adc1692e30cd8668c2f67793%22%7D; jitney_client_session_updated_at=1667950341; _ga_2P6Q8PGG16=GS1.1.1667947987.21.1.1667950341.51.0.0; _ga=GA1.1.28538937.1645828676; _uetsid=1c9f4ef05fb811ed90a42d17c31d99e4; _uetvid=93c35a50968b11ecb2c259648f5ad98d; bm_sv=96C45E59886438CD6ABF39A6A66920E4~YAAQBP4xFxa6mDWEAQAAqW2WWRFFA7+XMBg9VOtjetVnBufMkBO1btrcNAdTNs0vA543NbQEGSpTtPGftSbc7jy1uh1r5Mr0JWF5PDFpVQ9wuM8Z7nMfY8UwLmZyiidgaWWo8lwz+v8XXasMzN41XupBzDZo2ugLU1aLaD2mIkqwa+W6NPE21hFYWYQMM2H8zvDGDe1C+7QVGQC4kWmjCf5XtDER7h7DrOiWTh2vgFCtxNKBqGP6onln/kGfbh1LGw==~1',
    'device-memory': '8',
    'dpr': '0.9',
    'ect': '4g',
    'referer': 'https://www.airbnb.com/rooms/134238?adults=1&category_tag=Tag%3A8536&children=0&infants=0&search_mode=flex_destinations_search&check_in=2023-01-11&check_out=2023-01-17&federated_search_id=3b667d77-ae15-4f21-930a-ddcdf0a046ee&source_impression_id=p3_1667948539_QD7zmlrahlewwCFE',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'viewport-width': '2598',
    'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    'x-airbnb-graphql-platform': 'web',
    'x-airbnb-graphql-platform-client': 'minimalist-niobe',
    'x-airbnb-supports-airlock-v2': 'true',
    'x-client-request-id': '02g3t4q1s9ajma1lgth2x0uyolnf',
    # 'x-csrf-token': f"V4{.airbnb.com$ElzxlrV2huQ$xJ5MD3DoXWevk1TL-B_5MsSGlsb3aZMdXw7EOt92KwE=}",
    'x-csrf-without-token': '1',
    'x-niobe-short-circuited': 'true',
}

params = {
    'operationName': 'StaysPdpSections',
    'locale': 'en',
    'currency': 'USD',
    'variables': '{"id":"U3RheUxpc3Rpbmc6MTM0MjM4","pdpSectionsRequest":{"adults":"1","bypassTargetings":false,"categoryTag":"Tag:8536","causeId":null,"children":"0","disasterId":null,"discountedGuestFeeVersion":null,"displayExtensions":null,"federatedSearchId":"3b667d77-ae15-4f21-930a-ddcdf0a046ee","forceBoostPriorityMessageType":null,"infants":"0","interactionType":null,"layouts":["SIDEBAR","SINGLE_COLUMN"],"pets":0,"pdpTypeOverride":null,"preview":false,"previousStateCheckIn":null,"previousStateCheckOut":null,"priceDropSource":null,"privateBooking":false,"promotionUuid":null,"relaxedAmenityIds":null,"searchId":null,"selectedCancellationPolicyId":null,"selectedRatePlanId":null,"splitStays":null,"staysBookingMigrationEnabled":false,"translateUgc":null,"useNewSectionWrapperApi":false,"sectionIds":["CANCELLATION_POLICY_PICKER_MODAL","BOOK_IT_FLOATING_FOOTER","EDUCATION_FOOTER_BANNER_MODAL","POLICIES_DEFAULT","BOOK_IT_SIDEBAR","URGENCY_COMMITMENT_SIDEBAR","BOOK_IT_NAV","EDUCATION_FOOTER_BANNER","URGENCY_COMMITMENT","BOOK_IT_CALENDAR_SHEET"],"checkIn":"2023-01-11","checkOut":"2023-01-17","p3ImpressionId":"p3_1667950341_LGIPdX+0dHd5w28/"},"isLeanTreatment":false,"isHotel":false,"isPlus":false}',
    'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"36c83ecef0b4acaa151126f98997549c59805599d386a782996335f8e7a91ad8"}}',
}

response = requests.get('https://www.airbnb.com/api/v3/StaysPdpSections', params=params, cookies=cookies, headers=headers)
print(response.text)


print(json.dumps(json.loads(params["variables"]), indent=4))


with open("params.json", "w") as f:
    json.dump(params, f, indent=4)

with open("headers.json", "w") as f:
    json.dump(headers, f, indent=4)

with open("cookies.json", "w") as f:
    json.dump(cookies, f, indent=4)

with open("response.json", "w") as f:
    json.dump(response.json(), f, indent=4)
