
import playwright.sync_api as pw_sync_api
from playwright.sync_api import sync_playwright
from ParseTypes import ParseRequestData, Cookie, ParseResponseData, createScript
from Database import Database
from typing import List

def parse_script(topic: str, request: ParseRequestData):
    cors_domains = ['.yandex.ru', 'wiki.yandex.ru']
    url = request.params.url
    if not [i for i in cors_domains if url.find(i) != -1]:
        print("CORS policy error. Unable to parse.")
        return

    cookies = [
        # обновить Session_id и sessionid2 после повторной авторизации Yandex ID
        Cookie('Session_id', '3:1786132887.5.0.1786132887766:bKhHUA:6ff2.1.2:1|1656228854.-1.20002.3:1786132887|3:12097102.961343.rvsdp2uCgisXhca-ve8KKnXRbKU', cors_domains[0]),
        Cookie('sessionid2', '3:1786132887.5.0.1786132887766:bKhHUA:6ff2.1.2:1|1656228854.-1.20002.3:1786132887|3:12097102.961343.fakesign0000000000000000000', cors_domains[0]),
    ]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        cookies_gen = [dict(name=c.name, value=c.value, domain=c.domain, path=c.path) for c in cookies]
        print("initializing cookies...")
        print(cookies_gen)
        ctx.add_cookies(cookies_gen) # type: ignore
        page = ctx.new_page()

        response = page.goto(url)
        wiki_layout_selector = ".WikiPage-Content"
        page.wait_for_selector(wiki_layout_selector)

        if not response:
            print("Response is None. Check the URL and try again.")
            return
        raw_bytes = response.body()
        html_content = raw_bytes.decode('utf-8', errors='ignore')
        with open('home.html', 'w', encoding='utf-8') as document:
            document.write(html_content)
        
        page_cookies: List[pw_sync_api.Cookie] = ctx.cookies()
        csrf_token = next((cookie.get('value') for cookie in page_cookies if cookie.get('name') == 'CSRF-TOKEN'), None)
        
        if csrf_token:
            print(f"\n[УСПЕХ] Защита пройдена!")
            print(f"Ваш актуальный CSRF-TOKEN: {csrf_token}")
            
            # Получаем чистый контент статьи Wiki
            html_content = page.content()
            print("HTML-код статьи успешно получен и готов к парсингу контента.")
        else:
            print("\n[ОШИБКА] Токен все еще не найден. Возможно, Яндекс выдал капчу (картинку), которую нужно решить глазами.")
            # На всякий случай сохраним скриншот, чтобы увидеть, что сейчас на экране
            page.screenshot(path="yandex_result.png")
            print("Скриншот экрана сохранен в файл yandex_result.png")

        page.evaluate("""
            () => {
                document.querySelectorAll('details:not([open])').forEach(el => el.setAttribute('open', ''));
            }
        """)

        all_text = page.locator(wiki_layout_selector).inner_text()
        response = ParseResponseData(
            request.params, 
            all_text
        )
        # Save parse results to Database
        with Database() as db:
            db.insertScriptData(createScript(response.params.url, topic, response.content, response.date_parsed))
        browser.close()