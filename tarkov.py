import requests


def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def get_item_data(name):

    query = f"""
    {{
        items(name: "{name}") {{
            name
            low24hPrice
            iconLink
            wikiLink
            width
            height
            changeLast48hPercent
            
        }}
    }}
    """

    result = run_query(query)

    items = result['data']['items']

    item_name = items[0]['name']
    item_price = items[0]['low24hPrice']
    item_icon = items[0]['iconLink']
    item_link = items[0]['wikiLink']
    item_width = items[0]['width']
    item_height = items[0]['height']
    item_last48 = items[0]['changeLast48hPercent']
    

    return {
        'name': item_name,
        'low24hPrice': item_price,
        'iconLink': item_icon,
        'wikiLink': item_link,
        'width':item_width,
        'height':item_height,
        'changeLast48hPercent':item_last48
    }