from naver_db import NaverDB

ndb = NaverDB()

if __name__ == '__main__':
    try:
        stm="""INSERT INTO GAMER VALUES(7777,'gamer9','jose','cuevas','jose@aol.com',123456,1,1,4)"""
        res = ndb.persistence.setWriteLog("UNO") 
        print(res) 
        res["session"].commit()
    except Exception as e:
        print("ERROR")
        print(e)
        pass
