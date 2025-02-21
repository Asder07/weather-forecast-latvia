import json

with open('current.city.list.json', encoding='utf-8') as f:
    cities = json.load(f)

latvia_cities = [city for city in cities if city.get('country') == 'LV']

with open('latvia_cities.json', 'w', encoding='utf-8') as f:
    json.dump(latvia_cities, f, ensure_ascii=False, indent=4)

print(f"Найдено {len(latvia_cities)} городов Латвии")
