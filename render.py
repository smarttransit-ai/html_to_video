from selenium import webdriver
import time


def pngify_batch(
        html_file_paths,
        render_wait_max=30,
        post_render_wait=0.2
        ):
    '''
    Render a batch of HTML files to PNGs.
    '''
    options = webdriver.firefox.options.Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    pngs = []
    for fname in html_file_paths:
        try:
            driver.get('file:///{path}'.format(path=fname))
            driver.maximize_window()
            driver.implicitly_wait(render_wait_max)
            time.sleep(post_render_wait)
            pngs.append(driver.get_screenshot_as_png())
        except Exception as e:
            print('Error rendering {fname}: {e}'.format(fname=fname, e=e))
            pngs.append(None)

    driver.quit()
    return pngs
