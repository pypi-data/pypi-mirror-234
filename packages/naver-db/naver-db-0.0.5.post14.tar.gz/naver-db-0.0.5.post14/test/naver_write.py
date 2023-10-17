from naver_db import NaverDB

ndb = NaverDB()

if __name__ == '__main__':
    try:
        stm="""INSERT INTO GAMER VALUES(7777,'gamer9','jose','cuevas','jose2@aol.com',123456,1,1,4)"""
        res = ndb.persistence.setWrite(stm,"GAMER", False)
        print(res)
        print("AQUI")
        cursor = res["cursor"]
        session = res["session"]
   
        session.commit()
        print (cursor.lastrowid)
    except Exception as e:
        print(e)
        pass
