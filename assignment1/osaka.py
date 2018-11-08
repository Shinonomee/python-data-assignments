
# coding: utf-8

# In[24]:


from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time

def get_by_css(session, css, text=True):
    try:
        MAX_TRY = 3
        t = 0
        while t < MAX_TRY:
            t += 1
            try:
                res = session.find_element_by_css_selector(css)
            except StaleElementReferenceException:
                time.sleep(2)
                continue
            break
        if t == MAX_TRY:
            return None
    except NoSuchElementException:
        return None
    if text:
        return res.text
    return res


# In[25]:


def get_hotels_from_browser(b):

    hotels = []
    for session in b.find_elements_by_css_selector('.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout'):
        hotel = {}
        name = get_by_css(session, 'span.sr-hotel__name')
        score = get_by_css(session, '.bui-review-score__badge')
        comments = get_by_css(session, '.bui-review-score__text')
        address = get_by_css(session, '.jq_tooltip.district_link.visited_link')
        price = get_by_css(session, '.price.availprice.no_rack_rate')
        if not price:
            price = get_by_css(session, '.price.scarcity_color')

        hotel['name'] = name
        hotel['score'] = score
        hotel['comments'] = comments
        hotel['address'] = address
        hotel['price'] = price
        value_list=list(hotel.values())
        hotels.append(value_list)
    return hotels


# In[26]:


url = 'https://www.booking.com/searchresults.zh-cn.html?aid=378266&label=booking-name-IquAp*EbiLS6jPVl_he8yQS267778093594%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp9061634%3Ali%3Adec%3Adm&sid=75a6a10fd83d509dc44f2bc75e94dc31&checkin_month=9&checkin_monthday=12&checkin_year=2019&checkout_month=9&checkout_monthday=13&checkout_year=2019&city=-240905&class_interval=1&dest_id=-240905&dest_type=city&from_sf=1&group_adults=2&group_children=0&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=searchresults&srpvid=342a6023a36e0036&ss=%E5%A4%A7%E9%98%AA&ssb=empty&ssne=%E5%A4%A7%E9%98%AA&ssne_untouched=%E5%A4%A7%E9%98%AA&nflt=di%3D7322%3Bpri%3D2%3B&rsf=pri-2&lsf=pri%7C2%7C136'
browser = webdriver.Chrome()
browser.get(url)
time.sleep(2)


# In[27]:


all_page_hotels = []
for i in range(7):
    time.sleep(2)
    new_hotels= get_hotels_from_browser(browser)
    all_page_hotels.extend(new_hotels)
    time.sleep(0.5)
    no_survey = get_by_css(browser, '.survey_no_button', False)
    if no_survey:
        no_survey.click()
    time.sleep(1)
    next_button = browser.find_element_by_css_selector('.bui-pagination__nav ul.bui-pagination__list li.bui-pagination__item.bui-pagination__next-arrow a') #get the element's location
    next_button.location
    loc = next_button.location
    browser.execute_script("window.scrollTo({x}, {y});".format(**loc))
    time.sleep(2)
    next_button.click()


# In[28]:


import csv
with open('osaka.csv','w',newline='')as f:
    mywriter = csv.writer(f)
    header=['name','score','comments','address','price']
    mywriter.writerow(header)
    mywriter.writerows(all_page_hotels)

