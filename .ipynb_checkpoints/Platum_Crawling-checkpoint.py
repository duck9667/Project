{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import time\n",
    "import requests\n",
    "import datetime\n",
    "import json\n",
    "from bs4 import BeautifulSoup"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 헬스케어 관련 뉴스 크롤링"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 합치기\n",
    "def getNews(keyword_list, days, n) : \n",
    "    keyword_list =  keyword_list # 키워드 설정\n",
    "    n = n # 키워드당 n개\n",
    "    days = days # 최근 n일\n",
    "\n",
    "    # 크롤링\n",
    "    title = []\n",
    "    url = []\n",
    "    date = []\n",
    "    for i in range(len(keyword_list)) :\n",
    "        keyword = keyword_list[i]\n",
    "        url_keyword = \"https://platum.kr//?s=\" + keyword\n",
    "\n",
    "        soup = requests.get(url_keyword).text\n",
    "        html = BeautifulSoup(soup, 'html.parser')\n",
    "    \n",
    "    # 키워드당 n개 기사\n",
    "        for j in range(n) : \n",
    "            title.append(html.find_all('h5')[j].find('a')['title'])\n",
    "            url.append(html.find_all('h5')[j].find('a')['href'])\n",
    "            date.append(html.find_all('span', {\"class\" : \"post_info_date\"})[j].find('a').text)\n",
    "\n",
    "    # 연결 상태 확인\n",
    "    data = {'payload': '{\"text\": title }'}\n",
    "    response = requests.post('https://hooks.slack.com/services/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', data=data)\n",
    "\n",
    "    content = []\n",
    "    for i in range(len(title)) : \n",
    "        content.append({\"title\": title[i], \"url\":url[i], \"date\": date[i]})\n",
    "\n",
    "    # 중복제거\n",
    "    re_content = list(map(dict, set(tuple(sorted(d.items())) for d in content))) \n",
    "\n",
    "    # 최근 N일 기준\n",
    "    for i in range(len(re_content)) :\n",
    "        re_content[i][\"re_date\"] = re_content[i][\"date\"][10:]\n",
    "        re_content[i][\"re_date\"] = datetime.datetime.strptime(re_content[i][\"re_date\"],'%Y/%m/%d')\n",
    "\n",
    "    content = re_content\n",
    "    now = datetime.datetime.now()\n",
    "    period = now - datetime.timedelta(days=days)\n",
    "\n",
    "    num = []\n",
    "    for i in range(len(content)) : \n",
    "        if period < content[i][\"re_date\"] :\n",
    "            num.append(i)\n",
    "\n",
    "    # html 마크다운 설정\n",
    "    temp = []\n",
    "    for i in num : \n",
    "        if i == num[-1] : \n",
    "            temp.append(\"> \" + content[i]['title'] + \"\\n> \" + content[i]['url'] + \" \\n> \" + content[i]['date'])\n",
    "        else : \n",
    "            temp.append(\"> \" + content[i]['title'] + \"\\n> \" + content[i]['url'] + \" \\n> \" + content[i]['date'] + \"\\n\\n\")\n",
    "    temp\n",
    "    content = \"\".join(temp)\n",
    "\n",
    "    # 슬랙 전송\n",
    "    webhook_url= \"https://hooks.slack.com/services/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\"\n",
    "    payload= {\"text\": content }\n",
    "    requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type':'application/json'})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "keyword_list = [\"헬스\",\"웨어러블\",\"워치\", \"갤럭시 워치\"]\n",
    "getNews(keyword_list, 60, 3)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
