import requests
import sys
import re
import os


def create_dir(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print(name, "already exists")


def regex_engine(compiled_regex, text):
    results = re.findall(compiled_regex, text)
    return results


def img_downloader(img_name, url):
    print("Downloading from", url)
    res = requests.get(url)
    with open(img_name, "wb") as f:
        f.write(res.content)


def process():
    main_dir = "dimik_pub"
    create_dir(main_dir)

    url = "http://dimik.pub"
    res = requests.get(url)
    if res.ok is False:
        sys.exit("could not get response from the server")
    text = res.text
    text = re.sub(r'\s+', ' ', text)
    regexp = re.compile(r'<div class="book-cover"> <a href="(.*?)"><img src="(.*?)">.*?<h2 class="sd-title"><.*?>(.*?)</')
    for result in regex_engine(regexp, text):
        url = result[0]
        img_link = result[1]
        title = result[2]
        book_names = re.compile(r'book/(\d+)/(\w+)-(\w+)')
        book_names = regex_engine(book_names, url)
        for book_name in book_names:
            book_name = "_".join(book_name)
            create_dir(main_dir + "/" + book_name)
            file_name = main_dir + "/" + book_name + "/" + "info.txt"
            with open(file_name, "w") as f:
                f.write(title + "\n")
                f.write(url)

            img_name = main_dir + "/" + book_name + "/" + "image.png"
            img_downloader(img_name, img_link)


if __name__ == "__main__":
    process()
