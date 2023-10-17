from naver_db import NaverDB

ndb = NaverDB()

if __name__ == '__main__':
    try:
        res = ndb.persistence.getNextVal('id_tournament_subject','tournament_subject')
        print(res)
    except Exception as e:
        print("ERROR")
        pass
