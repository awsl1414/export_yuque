def get_url_list():
    with open("url_list.txt", "r", encoding="utf-8") as f:
        url_list_origin1 = f.readlines()

    url_list_ = "".join(url_list_origin1).split("\n")

    with open("url_current.txt", "r", encoding="utf-8") as f:
        url_current = f.read()

    url_list_origin2 = url_current.split("/")
    url_ = url_list_origin2[:3]

    url_list = []
    for i in url_list_:
        if i:
            url = "/".join(url_) + i + "/markdown"
            url_list.append(url)

    return url_list
