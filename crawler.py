from lxml import etree as ET
from lxml import html
import requests
import json

y_movie_url = 'https://movies.yahoo.com.tw/'
this_week_url = 'movie_thisweek.html'
movie_info_url = 'movieinfo_main.html/id='
movie_time_url = 'movietime_result.html/id='
'''
TODO
電影院API使用方法
1.找出該電影所有電影院id
2.theater_id找時間id
3.時間id找到時間

url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=10169&date=2019-08-21&area_id=&theater_id=&datetime=&movie_type_id='
rep = requests.get(url).content
src = json.loads(rep).get('view')
# print(src)
tree = html.fromstring(src)
a = tree.xpath('//*[@class="pc-movie-schedule-form"]/*')
# print(a)
for i in a:
    id_list = i.xpath('//@id')
    for x in id_list:
        if 'theater_id' in x:
            print(x)
----
a = tree.xpath('//*[@id="theater_id_241"]/li[3]/div/*/@id/')
a = tree.xpath('//*[@id="71915201"]/@value')
'''


def get_movie_ids():
    ids_src = requests.get(y_movie_url + this_week_url).content
    tree = html.fromstring(ids_src)
    movie_ids = tree.xpath('//*[@id="sbox_mid"]/option/@value')
    ids = list(filter(lambda x: len(x) != 0, movie_ids))
    return ids


def get_movie_name(movie_ids):
    name_zh = []
    name_en = []
    for m_id in movie_ids:
        movie_info_src = requests.get(y_movie_url + movie_info_url + m_id).content
        tree = html.fromstring(movie_info_src)
        m_zh_name = ''.join(tree.xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/h1/text()'))
        m_en_name = ''.join(tree.xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/h3/text()'))
        print(m_zh_name, m_en_name)
        name_zh.append(m_zh_name)
        name_en.append(m_en_name)
        # break
    return name_zh, name_en


def get_movie_theaters(movie_ids):
    all_theaters = []
    for m_id in movie_ids:
        theater = []
        movie_time_src = requests.get(y_movie_url + movie_time_url + m_id).content
        tree = html.fromstring(movie_time_src)
        movie_theaters = tree.xpath('//*[@id="content_l"]/div/div/div[2]/div[1]/div[3]')

        for m_idx, m_th in enumerate(movie_theaters):
            m_th = m_th.encode('utf-8')
            m_th_time = tree.xpath('//*[@id="ymvttr"]/div[1]/div/div[%d]/div/div/div[2]/div/span/text()' % (m_idx + 2))
            #print eachTheaterTime
            m_th_info = {'theater_name': m_th, 'time': m_th_time}
            #myEachTheater = json.dumps(myEachTheater,sort_keys = True,ensure_ascii = False)
            #myEachTheater = json.loads(myEachTheater,sort_keys = True,ensure_ascii = False)
            #print myEachTheater
            theater.append(m_th_info)
            #return
        all_theaters.append(theater)
    #print all_theaters
    return all_theaters


def myMovieArray():
    name_zh, name_en = get_movie_name()
    allTheaterList = getMovieTheater()
    myMovies = []
    for i in range(len(IDs) - 1):
        eachMovieinfo = {'Name_zh': name_zh[i], 'Name_en': name_en[i], 'Theater': allTheaterList[i]}
        #eachMovieinfo = json.dumps(eachMovieinfo,sort_keys = True)
        myMovies.append(eachMovieinfo)
    #print myMovies
    with open('myMovies.txt', 'w') as outfile:
        json.dump(myMovies, outfile, sort_keys=True, ensure_ascii=False)


def testJson():
    with open('myMovies.txt') as data_file:
        data = json.load(data_file, object_pairs_hook=OrderedDict)
    #data = data[0]["Theater"][0]["theater_name"]
    data = data[1]
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    movie_ids = get_movie_ids()
    get_movie_name(movie_ids)
