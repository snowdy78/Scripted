import datetime
from typing import List
import playwright.sync_api as pw_sync_api
from playwright.async_api import async_playwright
from Scripted.ParseTypes import ParseRequestData, Cookie, ParseResponseData, Script
from Scripted.Database import database

async def findScriptOrParse(topic: str, subtopic: str | None, request: ParseRequestData) -> Script:
    if not topic:
        raise ValueError("Cannot find or push script without topic.")
    topic_id = database.getTopicIdIfNotExists(topic)
    if topic_id is None:
        await parse_script(topic, request)
        return await findScriptOrParse(topic, subtopic, request)
    subtopic_id = database.getSubtopicIdIfNotExists(subtopic, topic_id)
    filters = ["topic_id=%s"]
    if subtopic_id is not None:
        filters.append("subtopic_id=%s")
    scripts = database.getScripts(filters, (topic_id, ) if subtopic_id is None else (topic_id, subtopic_id))
    if  len(scripts) < 1 or datetime.datetime.now() - scripts[0].date_parsed > datetime.timedelta(days=1):
        await parse_script(topic, request)
    scripts = database.getScripts(filters, (topic_id, ) if subtopic_id is None else (topic_id, subtopic_id))
    if len(scripts) < 1:
        raise ValueError("Cannot find script.")
    return scripts[0]

async def parse_script(topic: str, request: ParseRequestData):
    cors_domains = ['.yandex.ru', 'wiki.yandex.ru']
    url = request.params.url
    if not [i for i in cors_domains if url.find(i) != -1]:
        print("CORS policy error. Unable to parse.")
        return

    cookies = [
        # обновить Session_id и sessionid2 после повторной авторизации Yandex ID
        Cookie(
            'Session_id',
            '3:1786132887.5.0.1786132887766:bKhHUA:6ff2.1.2:1|1656228854.-1.20002.3:1786132887|3:12097102.961343.rvsdp2uCgisXhca-ve8KKnXRbKU',
            cors_domains[0]
        ),
        Cookie(
            'sessionid2',
            '3:1786132887.5.0.1786132887766:bKhHUA:6ff2.1.2:1|1656228854.-1.20002.3:1786132887|3:12097102.961343.fakesign0000000000000000000',
            cors_domains[0]
        ),
    ]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        cookies_gen = [dict(
            name=c.name,
            value=c.value,
            domain=c.domain,
            path=c.path
        ) for c in cookies]
        print("initializing cookies...")
        print(cookies_gen)
        await ctx.add_cookies(cookies_gen) # type: ignore
        page = await ctx.new_page()

        response = await page.goto(url)
        wiki_layout_selector = ".WikiPage-Content"
        await page.wait_for_selector(wiki_layout_selector)

        if not response:
            print("Response is None. Check the URL and try again.")
            return
        page_cookies: List[pw_sync_api.Cookie] = await ctx.cookies()
        csrf_token = next(
            (cookie.get('value')
             for cookie in page_cookies if cookie.get('name') == 'CSRF-TOKEN'),
            None
        )

        if csrf_token:
            print("\n[УСПЕХ] Защита пройдена!")
            print(f"Ваш актуальный CSRF-TOKEN: {csrf_token}")

            # Получаем чистый контент статьи Wiki
            print("HTML-код статьи успешно получен и готов к парсингу контента.")
        else:
            print(
                """\n[ОШИБКА] Токен все еще не найден. 
                Возможно, Яндекс выдал капчу (картинку), 
                которую нужно решить глазами."""
            )
            # На всякий случай сохраним скриншот, чтобы увидеть, что сейчас на экране
            await page.screenshot(path="yandex_result.png")
            print("Скриншот экрана сохранен в файл yandex_result.png")

        await page.evaluate("""
            () => {
                document.querySelectorAll('details:not([open])').forEach(el => el.setAttribute('open', ''));
            }
        """)

        all_text = await page.locator(wiki_layout_selector).inner_text()
        response = ParseResponseData(
            request.params,
            all_text
        )
        # Save parse results to Database
        database.insertScriptData(
            response.params.url,
            topic,
            None,
            response.content
        )
        await browser.close()
