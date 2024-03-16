from scraping.driver import SmartDriver


def main():
    driver = SmartDriver()
    html = driver.get_html("https://www.aruodas.lt/butai-vilniuje-tarandeje-uzubaliu-g-akcija-net-euru-nuolaida-pilnai-1-3412521/")
    # save the html to a file
    with open("test.html", "w") as file:
        file.write(html)
    


if __name__ == "__main__":
    main()