from naver import *
import os


def search_list():
    webtoon_id = ''
    episode_list = []
    menu = 0

    download_intention = ''
    start_point = 0
    end_point = 0

    while True:
        print("====================================================")
        webtoon_id = input('해당 웹툰의 아이디 숫자여섯자리를 입력하여 주십시오.')
        while int(webtoon_id) > 999999 or int(webtoon_id) < 100000:
            webtoon_id = input('웹툰 아이디를 잘못 입력하셨습니다. 정확하게 6자리를 입력해 주세요')

        os.system('clear')
        print("에피소드 리스트를 가져옵니다.")
        webtoon = NaverWebtoonCrawler(webtoon_id=webtoon_id)
        webtoon_name, episode_list = webtoon.get_episode_list()

        os.system('clear')
        print("{}의 에피소드 리스트".format(webtoon_name))
        print("=======================================")
        for i in episode_list:
            print('Episode : {}, Episode_number = {}'.format(i[0], i[1]))

        download_intention = input("위 웹툰을 다운로드 하시겠습니까?(y or yes) 딴소리하시면 나갑니다.")
        if download_intention == 'y' or download_intention == 'yes':
            print("=======================================")
            start_point = input(
                "다운로드를 시작할 에피소드 번호를 입력하여 주십시오.{}~{} : ".format(episode_list[len(episode_list)-1][1], episode_list[0][1]))
            end_point = input(
                "마지막으로 다운로드할 에피소드 번호를 입력하여 주십시오.{}~{} : ".format(str(start_point), episode_list[0][1]))

            for i in range(int(start_point), int(end_point) + 1):
                webtoon.crawl_episode(webtoon_name=webtoon_name, episode_name=episode_list[len(episode_list)-i][0], episode_num=i)
            print("다운로드가 완료되었습니다.")
            exit()
        else:
            exit()

    return


while True:
    print("========NAVER WEBTOON CRWALER==========")
    print("1.웹툰 크롤링")
    print("2.종료")
    print("=======================================")
    menu = input('메뉴를 선택하십시오:')

    if menu == '1':
        search_list()
    elif menu == '2':
        exit()
