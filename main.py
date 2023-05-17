from playwright.sync_api import Playwright, sync_playwright
from test import get_url_list
import random

url_list = get_url_list()
username = input("请输入用户名：")
password = input("请输入密码：")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # 完成登录
    page.goto("https://www.yuque.com/login")
    page.get_by_test_id("changeLoginWay").click()
    page.get_by_test_id("email-login-input").click()
    page.get_by_test_id("email-login-input").fill(username)
    page.get_by_test_id("loginPasswordInput").click()
    page.get_by_test_id("loginPasswordInput").fill(password)
    page.get_by_test_id("protocolCheckBox").check()
    page.wait_for_timeout(1000)
    page.get_by_test_id("btnLogin").click()
    page.wait_for_timeout(2000)
    page.click("xpath=//div/a[@class='index-module_link_tdBiE']")
    page.wait_for_timeout(2000)

    title_list1 = page.query_selector_all(
        '//div/div[@class="catalogTreeItem-module_content_fLFbS"]'
    )

    page.wait_for_timeout(2000)
    for i in title_list1:
        name = i.text_content()

        # print(name)
        try:
            page.get_by_role("button", name=name, exact=True).click()
            page.wait_for_timeout(1000)
        except Exception as e:
            page.get_by_role("button", name=name).click()
            page.wait_for_timeout(1000)

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)
    title_list2 = page.query_selector_all(
        "//a[@class='catalogTreeItem-module_content_fLFbS']"
    )
    # a = page.query_selector_all(
    #     "//div[@class='catalogTreeItem-module_CatalogItem_xkX7p']/a"
    # )

    print("文章标题数", len(title_list2))
    url_current = page.url
    with open("url_current.txt", "w", encoding="utf-8") as f:
        f.write(url_current)
    print(url_current)
    with open("url_list.txt", "w", encoding="utf-8") as f:
        pass
    name_list = []
    for i in title_list2:
        name = i.text_content()
        print(name)
        name_list.append(name)
        # page.get_by_test_id("aside").get_by_role("link", name=name).click()
        page.wait_for_timeout(1000)
        url_relative = i.get_attribute("href")

        with open("url_list.txt", "a", encoding="utf-8") as f:
            f.write(url_relative + "\n")

    for i, j in zip(name_list, url_list):
        page.goto(j)
        # print(j)
        page.wait_for_timeout(2000)
        page_content = page.content()

        with open(f"{i}.md", "w", encoding="utf-8") as f:
            f.write(page_content)
    page.close()
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
