from bs4 import BeautifulSoup
import requests


def parse_content(URL: str):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_content_by_day(day: str):
    """Get the list of news for a given day.
    """
    URL = f"https://tldr.tech/tech/{day}"
    soup = parse_content(URL)
    title = soup.find("h1")
    summary = soup.find("h2")
    icon_headers = soup.find_all("div", class_="text-3xl")
    text_headers = soup.find_all("h6")
    headers = [icon_header.contents[0] + " " + text_header.contents[0]
               for icon_header, text_header in zip(icon_headers, text_headers)]
    list_contents = soup.find_all("div", class_="mt-3")
    header_index = 0
    output = ""
    output += f"{title.contents[0]} \n\n {summary.contents[0]} \n\n"
    news_index = 1
    for list_content in list_contents[1:]:
        if list_content.find("h3"):
            output += str(news_index) + ". " + \
                list_content.find("h3").contents[0] + "\n" + '-' * 50 + "\n"
            news_index += 1
        elif header_index < len(headers):
            output += headers[header_index] + "\n\n"
            header_index += 1
            news_index = 1
        if list_content.find("div"):
            print(list_content.find("div"))
            output += list_content.find("div").contents[0] + "\n\n"
    return output


def get_days():
    """Get the list of days that have news.
    """
    URL = "https://tldr.tech/tech/archives"
    soup = parse_content(URL)
    link_elements = soup.find_all("a")

    count = 1
    days = []

    for link in link_elements:
        href = link.get("href")
        if not href.startswith("/tech/"):
            continue
        day = href.split("/")[-1]
        days.append(day)
        count += 1
    return days
