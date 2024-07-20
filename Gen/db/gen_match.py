import project.database as db
import random
from uuid import uuid4


def gen_match(like):
    query_user = "SELECT * FROM USER"
    users = db.get_query(query_user)
    query_like = ""
    match_like = ""

    if like.upper() == 'PLYY':
        query_like = "SELECT plyy_uuid FROM PLYY"
    elif like.upper() == 'CURATOR':
        query_like = "SELECT c_uuid FROM CURATOR"
    likes = db.get_query(query_like)
    users = db.get_query("SELECT * FROM USER")

    for i in users:
        for l in likes:
            TF = random.randint(0,1)
            if TF == 1:
                if like.upper() == 'PLYY':
                    query = "INSERT INTO PLYY_LIKE VALUES (?,?,?)"
                elif like.upper() == 'CURATOR':
                    query = "INSERT INTO CURATOR_LIKE VALUES (?,?,?)"
                db.execute_query(query, (str(uuid4()),i[0],l[0]))


gen_match('plyy')
gen_match('curator')