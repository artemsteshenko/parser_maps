# parser_maps
![plot](img.png)
## Parsing Yandex Maps 'https://yandex.ru/maps'
### Simple start
1. change ```type_org_mapping``` from [constants.py](https://github.com/artemsteshenko/parser_maps/blob/master/utils/constants.py), (```type_org_mapping = 'folder name': 'query'``` For example, ```type_org_mapping = 'showroom': 'Шоу-рум'```)


```
pip3 install -r requirements.txt
python3 link_parser.py showroom
python3 info_parser.py showroom
```


### 1. [link_parser.py](https://github.com/artemsteshenko/parser_maps/blob/master/link_parser.py)
- creating selenium webdriver. 
- creating ```LinksCollector``` object. 
- run collecting links with params of city, district, organization type and folder name for saving results. 
```
driver = webdriver.Safari()
grabber = LinksCollector(driver)
grabber.run(city='Москва', district='район Арбат', type_org_ru='Кафе', type_org='cafe')
```

### 2. [info_parser.py](https://github.com/artemsteshenko/parser_maps/blob/master/info_parser.py)
- creating selenium webdriver. 
- creating ```Parser``` object. 
- parse data with params of hrefs list, folder name of links from prev step
```
driver = webdriver.Safari()
parser = Parser(driver)
parser.parse_data(all_hrefs, type_org)
```
