import requests
import csv
from  bs4 import BeautifulSoup

def get_url(url):
    """
    Получает ответ сервера в виде HTML текста

    :param url: имя сайта
    :return: возвращает html код страницы с адресом url
    """
    r=requests.get(url)
    return r.text

def get_company_data(html):
    companies = []
    items = html.find_all("div", class_="blockv")
    for item in items:
        titel=item.h3.text
        link = item.h3.a["href"]
        address = item.div.text.split("тел.: ")[0].strip()
        phone = item.div.text.split("тел.: ")[1].split("Сегодня ")[0].strip()
        company = [titel, link, address, phone]
        companies.append(company)
    return companies

def uniq(lst):
    seen = set()
    result = []
    for x in lst:
        if x[0] in seen:
            continue
        seen.add(x[0])
        result.append(x)
    return result

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

def make_url(num_url):
    start_url="http://list.infox.by/search/page-"
    end_url="/?"
    return f'{start_url}{str(num_url)}{end_url}'

def make_company_full(link):
    print(link[1])
    soup=BeautifulSoup(get_url(link[1]), "lxml")
    address=soup.find('div', class_="concr_adr").text
    phone = soup.find('div', class_="concr_tel").text.split("Телефон: ")[1]
    if soup.find('div', class_="concr_site") is None:
        site = ""
    else:
        site = soup.find('div', class_="concr_site").text.split("Сайт: ")[1]
    if soup.find('div', class_="concr_email") is None:
        email=""
    else:
        email = soup.find('div', class_="concr_email").text.split("E-mail: ")[1]
    print(address)
    print(f"Телефон: {phone}")
    print(f"Caйт: {site}")
    print(f"E-mail: {email}")


def main():
    list_companies = []
    #url = "http://list.infox.by/search/page-350/?"
    file_name="address.csv"
    #url = make_url(340)
    for i in range(356, 357):
        url=make_url(i)
        soup=BeautifulSoup(get_url(url), "lxml")
        for company in get_company_data(soup):
            list_companies.append(company)
        #list_companies= get_company_data(soup)

    last_list = uniq(list_companies)
    #csv_writer(last_list, file_name)
    for item in last_list:#list_companies:
        #print(item)
        make_company_full(item)
    print(f'list len ={len(list_companies)} without duplicate record len = {len(last_list)}')
    #print(make_url(340))
    #print(make_url(500))
    #x = 5
    #y = 10
    #print(f'{x}*{y}/2={x*y/2}')


if __name__ == "__main__":
    main()

