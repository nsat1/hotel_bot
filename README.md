## Описание:

Бот поможет Вам найти гостиницы в интересующем вас городе. Позволяет искать гостиницы по заданному городу и сортировать их по стоимости и пользовательским параметрам.

### Пример использования [API](https://travelpayouts.github.io/slate/?python#displays-the-cost-of-living-in-hotels):
```python
import requests

url = "http://engine.hotellook.com/api/v2/cache.json"

querystring = {"location":"Saint-Petersburg","checkIn":"2024-04-13","checkOut":"2024-04-18","currency": "rub", "limit": "5", "token":"PasteYourTokenHere"}

response = requests.request("GET", url,params=querystring)

print(response.text)
```
#### Пример ответа:
```json
{
    "location": {
        "country": "Russia",
        "geo": {
            "lon": 37.617508,
            "lat": 55.752041
        },
        "state": null,
        "name": "Moscow"
    },
    "priceAvg": 60897.74,
    "pricePercentile": {
        "3": 28863.56,
        "10": 28863.56,
        "35": 47805.27,
        "50": 59531.09,
        "75": 65435,
        "99": 120128.17
    },
    "hotelName": "Mercure Arbat Moscow",
    "stars": 4,
    "locationId": 12153,
    "hotelId": 333561,
    "priceFrom": 28863.56
}  
```
#### Параметры запроса:
- location - название места (можно использовать код IATA);
- checkIn - дата заселения;
- checkOut - дата выезда;
- locationId - идентификатор места (может использоваться вместо места);
- hotelId - идентификатор отеля;
- hotel - название отеля (при вводе названия обязательно указывайте location или locationId);
- adults - количество взрослых гостей (по умолчанию 2);
- children - количество детей (от 2 до 18 лет);
- infants - количество младенцев (от 0 до 2 лет);
- limit - количество отелей. Если этот параметр используется в запросе без указания точного идентификатора или названия отеля, применяется следующее:
    - limit = 4 (по умолчанию) - будет возвращено по одному отелю каждой категории (Stars);
    - limit = 5 - вернет два 5 отеля и один из других категорий;
    - limit = 6 - два 5 и 4 отеля и один из других категорий;
    - limit = 7 - два 5, 4 и 3-звездочных отеля и один comfortable;
    - limit = 8 - все два. И так далее, причем параметры роста поочередно увеличивают количество отелей в каждой звезде. Если указанных звездных отелей не останется, то выпуск начнет падать и отелей 1 0 звезд по тому же правилу;
- customerIp - параметр для указания IP пользователя, если запрос отправляется не напрямую, а через прокси-сервер;
- currency - валюта цены (rub, usd, eur);
- token - ваш партнерский токен.

#### Параметры ответа:

- stars - количество звезд отеля;
- locationId - идентификатор местоположения данного отеля;
- priceFrom - минимальная цена за проживание в гостиничном номере за период;
- priceAvg - средняя цена за проживание в гостиничном номере за период
- pricePercentile - цена сегментации для пропорций (например, запись типа "50": 59531.09 означает, что 50% цены находится в диапазоне от 59531.09 до руб);
- hotelName - название отеля;
- location - информация о местоположении отеля:
    - geo - координаты отеля;
    - name - название места (города);
    - state - штат, в котором находится город;
    - country - страна, в которой находится отель;
- hotelId - идентификатор отеля.

### Пример использования [API](https://travelpayouts.github.io/slate/?python#the-types-of-hotel-collections) для команды /custom:
```python
import requests

url = "http://yasen.hotellook.com/tp/public/available_selections.json"

querystring = {"id":"12209", "token":"PasteYourTokenHere"}

response = requests.request("GET", url, params=querystring)

print(response.text)
```
#### Пример ответа:
```json
[
    "center",
    "tophotels",
    "highprice",
    "3-stars",
    "4-stars",
    "5-stars",
    "restaurant",
    "pets",
    "pool",
    "cheaphotel_ufa",
    "luxury_ufa",
    "price",
    "rating",
    "distance",
    "popularity",
    "2stars",
    "3stars",
    "4stars",
    "5stars"
]
```
#### Параметры запроса:
- id — идентификатор города;
- token — ваш партнерский токен;

#### Параметры ответа:
- center - отели, расположенные в центре города;
- tophotels - лучшие отели;
- highprice - самые дорогие отели;
- 3-stars, 4-stars, 5-stars - автоматический поиск отелей, имеющих 3, 4 или 5 звезд;
- restaurant - наличие собственного ресторана;
- pets - возможность проживания с домашними животными;
- pool - наличие собственного бассейна;
- cheaphotel - самые дешевые отели;
- luxury - роскошные отели;
- price - вручную сформированные подборки по цене;
- rating - отели с наивысшим рейтингом;
- distance - расстояние от аэропорта;
- popularity - популярность отеля;
- 2stars, 3stars, 4stars, 5stars - сформированные вручную коллекции с соответствующим количеством звезд.

### Пример использования [API](https://travelpayouts.github.io/slate/?python#hotels-selections) для команды /low и /high:
```python
import requests

url = "http://yasen.hotellook.com/tp/public/widget_location_dump.json"

querystring = {"currency":"rub", "language":"ru", "limit":"5", "id":"12209", "type":"popularity", "check_in":"2019-02-02", "check_out":"2019-02-17", "token":"PasteYourTokenHere"}

response = requests.request("GET", url, params=querystring)

print(response.text)
```

#### Пример ответа:
```json
{
    "popularity": [
        {
            "hotel_id": 713859,
            "distance": 6.68,
            "name": "President Hotel",
            "stars": 4,
            "rating": 87,
            "property_type": "hotel",
            "hotel_type": [
                "Solo Hotel"
            ],
            "last_price_info": {
                "price": 39707,
                "old_price": 42761,
                "discount": 7,
                "insertion_time": 1485464441,
                "nights": 15,
                "search_params": {
                    "adults": 2,
                    "children": {},
                    "checkIn": "2019-02-02",
                    "checkOut": "2019-02-17"
                },
                "price_pn": 2647,
                "old_price_pn": 2851
            },
            "has_wifi": true
        }
    ]
}
```
#### Параметры запроса:
***команда /high в параметре type имеет значение по умолчанию [highprice](#пример-использования-api-для-команды-custom)***  
***команда /low в параметре type имеет значение по умолчанию [cheaphotel](#пример-использования-api-для-команды-custom)***

- check_in - дата заселения;
- check_out - дата выезда;
- currency - валюта ответа;
- language - язык ответа (pt, en, fr, de, id, it, pl, es, th, ru);
- limit - ограничение количества выводимых результатов от 1 до 100, по умолчанию - 10;
- [type](#пример-использования-api-для-команды-custom) - тип отелей из запроса;
- [id](#пример-использования-api) - идентификатор города;
- token - ваш партнерский токен;

#### Параметры ответа:
- hotel_id - уникальный идентификатор отелей;
- distance - расстояние от центра города;
- name - название отеля;
- stars - количество звезд;
- rating - рейтинг отеля, присвоенный его посетителями;
- property_type - тип отеля;
- hotel_type - описание типа отеля;
- last_price_info - информация о последней найденной цене отеля (если есть);
    - price - цена проживания за весь период со скидкой;
    - old_price - цена проживания без скидки;
    - discount - размер скидки;
    - insertion_time - время, когда была найдена коллекция;
    - nights - количество ночей;
- search_params - параметры поиска;
- price_pn - цена ночи в гостиничном номере со скидкой;
- old_price_pn - цена ночи в гостиничном номере без скидки;
- has_wifi - наличие Wi-Fi.

## Доступные команды:

- /low - выводит гостиницы с наименьшей стоимостью;
- /high - выводит гостиницы с наибольшей стоимостью;
- /custom - позволяет выбрать диапазон цен для поиска гостиниц;
- /history - выводит историю запросов пользователя.

## Зависимости:

