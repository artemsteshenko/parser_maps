def into_json(org_id, name, address, website, opening_hours, ypage, goods, rating, reviews, phone, social):
    """ Шаблон файла OUTPUT.json"""

    opening_hours_new = []
    days = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']

    # Проверка opening_hours на отсутствие одного их рабочих дней
    # Создается отдельный список (opening_hours_new) с полученными значениями
    # Далее он проверяется на отсутствие того или иного рабочего дня
    # На индекс отсутствующего элемента вставляется значение  "   выходной"
    for day in opening_hours:
        opening_hours_new.append(day[:2].lower())
    for i in days:
        if i not in opening_hours_new:
            opening_hours.insert(days.index(i), '   выходной')

    data_grabbed = {
        "ID": org_id,
        "name": name,
        "address": address,
        "website": website,

        "opening_hours":
            {
                "mon": opening_hours[0][3:],
                "tue": opening_hours[1][3:],
                "wed": opening_hours[2][3:],
                "thu": opening_hours[3][3:],
                "fri": opening_hours[4][3:],
                "sat": opening_hours[5][3:],
                "sun": opening_hours[6][3:]
            },
        "ypage": ypage,
        "goods": goods,
        "rating": rating,
        "reviews": reviews,
        "phone": phone,
        "social": social,

    }
    return data_grabbed