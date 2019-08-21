import requests
from lxml import etree as ET
from lxml import html
import json


y_movie_url = 'https://tw.movies.yahoo.com/'
thisWeekUrl ='movie_thisweek.html'
movieInfoUrl = 'movieinfo_main.html/id='
movieTimeUrl ='movietime_result.html?id='


def getMovieID():
    movieIDSource = requests.get(y_movie_url + thisWeekUrl).content
    tree = html.fromstring(movieIDSource)
    IDs = []
    movieIDs = tree.xpath('//*[@id="sbox_mid"]/option/@value')
    IDs = list(filter(lambda x: len(x) != 0 , movieIDs))
    print(IDs)
    return IDs

def getMovieName(IDs):
    name_zh = []
    name_en = []
    for eachID in IDs:
        movieInfoSource = requests.get(y_movie_url + movieInfoUrl + eachID).content
        tree = html.fromstring(movieInfoSource)
        movieZhName = tree.xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/h1/text()')
        movieEnName = tree.xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/h3/text()')
        # print(movieZhName, movieEnName)
        zh = ''.join(movieZhName).encode('utf-8')
        en = ''.join(movieEnName).encode('utf-8')
        print(zh)
        name_zh.append(zh)
        name_en.append(en)
    return (name_zh , name_en)
    
def getMovieTheater():
    allTheaterList = []
    for eachID in IDs:
        #print eachID
        theaterList =[]
        movieInfoSource = requests.get(y_movie_url + movieTimeUrl + eachID).content
        tree = html.fromstring(movieInfoSource)
        movieTheater = tree.xpath('//*[@id="ymvttr"]/div[1]/div/div/div/div/div[1]/a/text()')
        for movieIndex,eachTheater in enumerate(movieTheater):
            eachTheater = eachTheater.encode('utf-8')
            #print eachTheater
            eachTheaterTime = tree.xpath('//*[@id="ymvttr"]/div[1]/div/div[%d]/div/div/div[2]/div/span/text()'%(movieIndex+2))
            #print eachTheaterTime
            myEachTheater = {'theater_name':eachTheater,'time':eachTheaterTime}
            #myEachTheater = json.dumps(myEachTheater,sort_keys = True,ensure_ascii = False)
            #myEachTheater = json.loads(myEachTheater,sort_keys = True,ensure_ascii = False)
            #print myEachTheater
            theaterList.append(myEachTheater)
            #return
        allTheaterList.append(theaterList)
    #print allTheaterList
    return allTheaterList

def myMovieArray():
    name_zh , name_en = getMovieName()
    allTheaterList = getMovieTheater()
    myMovies = []
    for i in range(len(IDs)-1) :
        eachMovieinfo = {'Name_zh':name_zh[i],'Name_en':name_en[i],'Theater':allTheaterList[i]}
        #eachMovieinfo = json.dumps(eachMovieinfo,sort_keys = True)
        myMovies.append(eachMovieinfo)
    #print myMovies
    with open('myMovies.txt', 'w') as outfile:
        json.dump(myMovies, outfile, sort_keys = True,ensure_ascii = False)

def testJson():
    with open('myMovies.txt') as data_file:    
        data = json.load(data_file, object_pairs_hook=OrderedDict)
    #data = data[0]["Theater"][0]["theater_name"]
    data = data[1]
    print(json.dumps(data, indent=2))



if __name__ == '__main__':
    IDs = getMovieID()
    getMovieName(IDs)
    # getMovieTheater()
    # myMovieArray()
    # testJson()