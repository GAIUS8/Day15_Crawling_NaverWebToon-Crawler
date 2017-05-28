import os
import requests
from bs4 import BeautifulSoup


class NaverWebtoonCrawler:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self.url_in_list = 'http://comic.naver.com/webtoon/list.nhn?' \
                           'titleId={webtoon_id}&' \
                           'page={list_page_num}'
        self.url_in_episode = 'http://comic.naver.com/webtoon/detail.nhn?' \
                              'titleId={webtoon_id}&' \
                              'no={episode_num}&'

    def get_episode_list(self):
        '''
        해당 웹툰의 에피소드 리스트 전체를 반환합니다. 반환되는 형태에 주의하십시오.(2중 리스트 형태로 반환됩니다.)
        :return: list of episode_list like [[episode_title, episode_no, thumnail_src], ......]
        '''
        last_page = 1
        episode_list = []

        '''리스트 페이지가 몇개나 있는지 확인'''

        def get_first_title_of_page(page):
            url_detail = self.url_in_list.format(webtoon_id=self.webtoon_id, list_page_num=str(page))
            header = {'Referer': url_detail}
            response = requests.get(url_detail, headers=header)
            soup = BeautifulSoup(response.text, 'lxml')
            table = soup.find('table', class_="viewList")
            tr_list = table.select_one('td.title').get_text().strip()
            return tr_list

        while get_first_title_of_page(last_page) != get_first_title_of_page(last_page+1):
            last_page += 1
            print('총 리스트 페이지가 몇 페이지인지 확인합니다. 확인된 페이지 :{}'.format(last_page))

        """Get episode_list"""
        for i in range(1, last_page+1):
            url_detail = self.url_in_list.format(webtoon_id=self.webtoon_id, list_page_num=str(i))
            header = {'Referer': url_detail}
            response = requests.get(url_detail, headers=header)
            soup = BeautifulSoup(response.text, 'lxml')
            subject_name = soup.select_one('div.detail').find_all('h2')[0].contents[0].strip()
            table = soup.find('table', class_="viewList")
            tr_list = table.find_all('tr')
            for tr in tr_list:
                if not tr.find('td', class_="title"):
                    continue
                title = tr.find('td', class_="title").find('a').text
                link_no = tr.find('td', class_="title").find('a')['href'].split("no=")[1].split("&")[0]
                thumnail = tr.find('img', title=title)['src']
                episode_list.append([title, link_no, thumnail])
        print("에피소드 리스트가 반환되었습니다.")
        return subject_name, episode_list  #epsode_list = [episode_title, epsode_no, thumnail_src]

    def crawl_episode(self, webtoon_name=None, episode_name=None, episode_num=None):
        """
        WebtoonId에 해당하는 웹툰의 한개 에피소드 이미지를 긁어와 저장 (html 페이지를 만들어줍니다)
        :param episode_num:
        :return:
        """
        if not episode_num:
            url_detail = self.url_in_episode.format(
                self.webtoon_id,
            )
        else:
            url_detail = self.url_in_episode.format(
                webtoon_id=self.webtoon_id,
                episode_num=episode_num
            )
        os.makedirs('{}/{}'.format(self.webtoon_id, episode_num), exist_ok=True)

        dir_path = '{}/{}'.format(self.webtoon_id, episode_num)

        header = {'Referer': url_detail}
        response = requests.get(url_detail, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        div_wt_viewer = soup.select_one('div.wt_viewer')
        img_list = div_wt_viewer.find_all('img')

        with open('{}/{}({})_{}.html'.format(self.webtoon_id, webtoon_name, self.webtoon_id, episode_name), 'wt') as ht:
            ht.write('<!DOCTYPE html>'
                     '<html lang="en">'
                     '<head><meta charset="UTF-8">'
                     '<title>{}</title>'.format(webtoon_name+episode_name))
            ht.close()
        with open('{}/{}({})_{}.html'.format(self.webtoon_id, webtoon_name, self.webtoon_id, episode_name), 'at') as ht:
            ht.write('<style>'
                     'img{'
                     'display: block;'
                     'margin: 0 auto;'
                     '}'
                     '</style>'
                     '</head>'
                     '<body>')
            ht.close()

        for index, img in enumerate(img_list):
            response = requests.get(img['src'], headers=header)
            img_path = '{}/{:2}.jpg'.format(
                dir_path,
                index
            )
            with open(img_path, 'wb') as f:
                f.write(response.content)
                f.close()
            with open('{}/{}({})_{}.html'.format(self.webtoon_id, webtoon_name, self.webtoon_id, episode_name),
                      'at') as ht:
                ht.write('<img src="../{}/{:2}.jpg">\n'.format(
                    dir_path,
                    index
                ))
                ht.close()

        with open('{}/{}({})_{}.html'.format(self.webtoon_id, webtoon_name, self.webtoon_id, episode_name), 'at') as ht:
            ht.write('</body></html>')
            ht.close()
