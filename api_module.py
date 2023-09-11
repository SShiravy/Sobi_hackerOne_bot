import requests


def get_scopes():
    headers = {
        'Accept': 'application/json'
    }
    final_handle_list = []
    final_asset_identifier_list = []

    # دریافت داده‌ها از API
    for i in range(50):
        r = requests.get(
            'https://api.hackerone.com/v1/hackers/programs/',
            auth=('sobi313sh', 'qWhP7AbTZsrMs87fiYvldbJ15fWEumziAWhJXo1+Qyo='),
            headers=headers,
            params={'page[number]': i, 'page[size]': 6}
        )
        programs_obj = r.json()['data']

        for program in programs_obj:
            handle = program['attributes']['handle']
            structured_scopes = requests.get(
                f'https://api.hackerone.com/v1/hackers/programs/{handle}/structured_scopes',
                auth=('sobi313sh', 'qWhP7AbTZsrMs87fiYvldbJ15fWEumziAWhJXo1+Qyo='),
                headers=headers,
                params={'handle': handle}).json()['data']
            asset_identifier_list = [scop['attributes']['asset_identifier'] for scop in structured_scopes]
            final_handle_list.append(handle)
            final_asset_identifier_list.append(asset_identifier_list)
            print(handle)
            print(asset_identifier_list)

    return final_handle_list, final_asset_identifier_list
