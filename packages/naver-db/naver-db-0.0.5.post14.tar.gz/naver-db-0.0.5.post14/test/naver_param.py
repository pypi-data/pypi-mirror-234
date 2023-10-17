from naver_db import NaverDB

ndb = NaverDB()

if __name__ == '__main__': 
    res = ndb.persistence.getParam(['1'])
    print (res)