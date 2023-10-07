import pytest


@pytest.mark.asyncio
async def test_intelligent_captcha(page):
    await page.goto("https://www.geetest.com/en/demo")

    result = await page.solve_geetest()
    print(result)
    assert result


@pytest.mark.asyncio
async def test_slider_captcha(page):
    await page.goto("https://www.geetest.com/en/demo")

    checkbox = page.locator('[class="tab-item tab-item-1"]')
    await checkbox.click()

    await page.wait_for_timeout(2000)

    result = await page.solve_geetest()
    print(result)
    assert result


@pytest.mark.asyncio
async def test_icon_captcha(page):
    await page.goto("https://www.geetest.com/en/demo")

    checkbox = page.locator('[class="tab-item tab-item-2"]')
    await checkbox.click()

    await page.wait_for_timeout(2000)

    result = await page.solve_geetest(mode="canny")
    print(result)
    assert result
