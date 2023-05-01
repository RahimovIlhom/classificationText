import csv

# faylga yozish uchun namuna ma'lumotlari
data = [['Hello', 'World'], ['Python', 'Programming'], ['Uzbek', 'Language'], ['Bu mening sevimli kitobim', 'Adabiyot']]
data = [(text[0].lower(), text[1].lower()) for text in data]

# CSV faylini yozish rejimida ochish
with open('classWords.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # sarlavhani yozish
    writer.writerow(['text', 'label'])

    # ma'lumotlarni qatorma-qator yozish
    for row in data:
        writer.writerow(row)
