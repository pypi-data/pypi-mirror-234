from naver_db import NaverDB

ndb = NaverDB()

if __name__ == '__main__':
    stm="""SELECT * from GAMER"""
    res = ndb.persistence.getQuery(stm,"GAMER")
    print (res)