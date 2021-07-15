from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import os
from tqdm import tqdm

# 현재 폴더에 result 없으면 생성하고 있으면 넘어감
try:
    os.mkdir("./result")
    print("result 폴더 생성")
except:
    print("result 폴더 이미 존재")

# path_dir 에 있는 모든 .txt 파일을 탐색해서 file_list_txt 에 저장
path_dir = './'  # 경로를 현재 경로로 바꿀 예정
file_list = os.listdir(path_dir)
file_list_txt = [file for file in file_list if file.endswith(".txt")]
print("현재 폴더의 .txt 파일 목록", end=' ')
print(file_list_txt)

print("출발 언어 : 자동 감지")

# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")

# selenium 을 통한 웹 자동화
driver = webdriver.Chrome(options=options)
driver.get("https://google.com")
# 구글을 통해 번역기 검색
elem = driver.find_element_by_class_name("gLFyf.gsfi")
elem.send_keys("구글 번역기")
elem.send_keys(Keys.ENTER)
driver.find_element_by_xpath('//*[@id="tw-sl"]').click()
driver.find_element_by_xpath('//*[@id="tw-container"]/g-expandable-container/div/div/div['
                             '6]/g-expandable-container/div/g-expandable-content/span/div/div[3]/div[1]/div/div['
                             '1]').click()  # 언어 감지 클릭


print("\n[도착 가능 언어]")
driver.find_element_by_xpath('//*[@id="tw-tl"]').click()
soup = BeautifulSoup(driver.page_source, 'html.parser')
ArriveLenge = []
ArriveLenge2 = []
jump = 0
for i in soup.select("div.tw-lliw"):

    if jump < 10:
        ArriveLenge2.append(i.text)
        jump += 1
    else:
        if i.text == "힌디어":
            ArriveLenge2.append(i.text)
            ArriveLenge.append(ArriveLenge2)
            # print(i.text)
            break
        ArriveLenge.append(ArriveLenge2)
        ArriveLenge2 = []
        jump = 0

for row in ArriveLenge:
    print(row)


text = input("\n도착 언어를 선택하세요 : ")

driver.find_element_by_xpath('//*[@id="tw-container"]/g-expandable-container/div/div/div['
                             '6]/g-expandable-container/div/g-expandable-content/span/div/div[2]/div[1]/div/div['
                             '2]/div[107]/div[contains(text(), "' + text + '")]').click()

print("번역 시작")

# file_list_txt 에서 .txt 파일을 하나씩 가져와 번역 시행
for txt in file_list_txt:
    fp = open("./" + txt, 'r', encoding="utf-8")  #경로 수정하기
    text = fp.read()
    fp.close()

    # 하나의 .txt 파일에서 500글자씩 잘라서 ready_list 에 저장
    ready_list = []
    while len(text) > 400:
        temp_str = text[:400]
        last_space = temp_str.rfind('.')
        if '。' in text:  # 일본어 일때만...
            last_space = temp_str.rfind('。')
        temp_str = text[0:last_space]
        ready_list.append(temp_str)
        text = text[last_space:]

    ready_list.append(text)

    elem = driver.find_element_by_class_name("tw-ta.tw-text-large.XcVN5d.goog-textarea")

    new_str = ''

    pbar = tqdm(total=len(ready_list), desc=txt)  # tqdm 을 사용한 progress bar

    # 500자씩 나눠 담아둔 ready_list 에서 리스트 하나씩 꺼내 번역
    for ready in ready_list:
        elem.send_keys(Keys.CONTROL, "a")
        elem.send_keys(ready)

        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        st = soup.select("pre.tw-data-text.tw-text-large.XcVN5d.tw-ta")[0].text
        new_str += st

        pbar.update(1)  # progress bar 인 pabar 을 1증가
    pbar.close()

    # 결과를 result 폴더에 .txt 파일로 저장
    fp = open("./result/" + txt, 'w', encoding='utf-8')  # 경로 수정하기
    fp.write(new_str)
    fp.close()
    
print("번역 완료 및 종료")
driver.quit()
