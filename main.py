import datetime
import pandas
import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_word(age):
    last_number = age % 10
    prelast_number = age // 10 % 10
    if last_number >= 2 and last_number <= 4:
        if prelast_number == 1:
            word = "лет"
        else:
            word = "года"
    elif last_number == 1:
        if prelast_number == 1:
            word = "лет"
        else:
            word = "год"
    else:
        word = "лет"
    return word


def main():

    wines = pandas.read_excel(
        "wine3.xlsx", na_values=["N/A", "NA"], keep_default_na=False
    ).to_dict("records")

    dict_of_lists = collections.defaultdict(list)
    for wine in wines:
        dict_of_lists[wine["Категория"]].append(wine)

    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")
    now = datetime.datetime.now()
    age = now.year - 1920

    rendered_page = template.render(age=age, wines=dict_of_lists, word=get_word(age))

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()

