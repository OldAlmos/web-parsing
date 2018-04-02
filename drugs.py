import string
import requests
import csv
from bs4 import BeautifulSoup

def  delete_char(str1, str2):
    """Delete in str1 all chars from str2


    """
    return "".join((s for s in str1 if not(s in str2)))

def get_url(url):
    """
    Получает ответ сервера в виде HTML текста

    :param url: имя сайта
    :return: возвращает html код страницы с адресом url
    """
    r=requests.get(url)
    return r.text



def make_url(part_url):
    start_url="https://www.drugs.com/condition/"
    end_url = ".html"
    return f"{start_url}{part_url}{end_url}"

def get_condition_alfa(html):
    return html.find("ul", class_="column-list-2").find_all("li")

def csv_writer(items, fname):
    """
    Сохраняет список фирм в csv файле

    :param items: Список адресов
    :param fname: Файл для сохранения
    :return: ничего не возвращает
    """
    with open(fname, 'w', encoding='utf-8', newline='') as csv_file:#открыть файл csv для записи,
        # если файл есть он будет перезаписан
        #если файла нет, он будет создан
        writer = csv.writer(csv_file, delimiter=';')#создаем писателя в файд с разделителем ;
        for item in items:#для всех фирм в каталоге
            writer.writerow(item)#записать в файл название ссыдку адрес и телефон


def main():
    list_condition_all = []
    for c in string.ascii_lowercase:
        #if c=="c":
        #    break
        url = make_url(c)
        soup = BeautifulSoup(get_url(url), "lxml")
        list_condition_alfa = get_condition_alfa(soup)
        for item in list_condition_alfa:
            print(item.text)
            list_condition_all.append([item.text.strip(), item.a["href"]])
        print(len(list_condition_all))
    csv_writer(list_condition_all, "condition.csv")






if __name__ == "__main__":
    main()