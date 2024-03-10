from scraping.driver import SmartDriver


def main():
    driver = SmartDriver()
    html = driver.get_html("https://www.google.com")
    # save the html to a file
    with open("google.html", "w") as file:
        file.write(html)
    


if __name__ == "__main__":
    main()