import os
import json
from flask import Flask, jsonify, request
# from datetime import datetime
import psycopg2

os.environ[
    'DATABASE_URL'] = 'postgres://tdcqtmnigcllnz:9c0c1c18391da12bd9e3e970d6a886e38d1565d7623492eefebc2e0d0116e107@ec2-54-225-76-136.compute-1.amazonaws.com:5432/d9ouc73s3504a6'
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

aplic = Flask(__name__)

# @aplic.route('/')
# def wsReadDB():
#     if request.headers.get('Authorization') == '42':
#         return jsonify({"42": "a resposta para a vida, o universo e tudo mais"})
#     return jsonify({"message": "Não entre em pânico!"})

@aplic.route('/tagsBagsList')
def tagsBagsList():
    pg = request.args.get('page')
    print("Parametro: " + pg)
    offset = 10 * (int(pg) - 1)
    cur.execute('select * from TB_TAG_RECEIVED order by DTH_INSERTIO  desc LIMIT 10' + ' OFFSET ' + str(offset))
    result_set = cur.fetchall()
    # tela = ""
    num_recs = 0

    # username = request.form['username']
    docs = []
    saida = ""
    x = ""
    # lista =db.execute('select count(*) nro from public."TB_TAG_RECEIVED"')
    # cur.execute('select count(*) nro from TB_TAG_RECEIVED')
    # lista = cur.fetchall()
    # print (lista[0][0])
    tot = len(result_set)
    # for r in lista:
    #     print (r[0])
    #     tot = r[0]

    numberOfPages = tot // 10
    if (numberOfPages % 10 != 0):
        numberOfPages = numberOfPages + 1
    if (numberOfPages == 0):
        numberOfPages = 1

    for r in result_set:
        # tela = tela + "<body><p>" + r[2] + "</p></body>"
        data = {}
        dt = r[1]
        id = r[0]
        strg = '{:%Y-%m-%d %H:%M:%S}'.format(dt)
        # print (r.DTH_INSERTION)
        # print (strg)
        data['ID'] = str(id)
        data['data'] = strg
        data['tag'] = r[2]
        x = json.dumps(data)
        # saida.join(x)
        if saida == "":
            saida = x
        else:
            saida = saida + "," + x
        print(x)
        json_data = docs.append(json.dumps(data))
        num_recs = num_recs + 1

    saida = '{"docs":[' + saida + '],"total":' + str(tot) + ',"limit":10,"page":' + pg + ',"pages":' + str(
        numberOfPages) + '}'

    return saida

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    aplic.run(host='0.0.0.0', port=port)
