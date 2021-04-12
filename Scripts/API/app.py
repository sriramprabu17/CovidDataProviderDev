from werkzeug.wrappers import Request, Response
from flask import Flask,request,jsonify
from CovidDataProvider.Config import Config
import sqlite3
import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



app = Flask(__name__)


@app.route('/')
def landing():
    return "/api/ZIPCode?StartDate=YYYY-MM-DD&EndDate=YYYY-MM-DD"

@app.route('/<path:path>')
def catch_all(path):
    return "/api/ZIPCode?StartDate=YYYY-MM-DD&EndDate=YYYY-MM-DD"


@app.route('/api/<ZIP>', methods=['GET'])
def api_filter(ZIP):

    query_parameters = request.args


    StartDate = query_parameters.get('StartDate')
    EndDate = query_parameters.get('EndDate')



    conn = sqlite3.connect(Config.DB)
    conn.row_factory = dict_factory
    cur = conn.cursor()




    query = "select Z.ZIP, F.County, F.Date, F.EstimatedCnt,F.PopulationCnt,Z.RES_RATIO, Round(F.EstimatedCnt/ifnull(PopulationCnt,0)*Z.RES_RATIO,4) Incident_Rate from FactCovidCounts F Left Join LkpZip Z on F.FIPS = Z.FIPS2  WHERE "
    to_filter = []


    if ZIP:

        ValidateZIP = cur.execute("Select count(ZIP) cnt from LkpZip where ZIP = \'"+ ZIP +"\' ;").fetchone()
        if ValidateZIP['cnt'] == 0:

            return "Invalid ZIP Code or ZIP Code Data Not Available"
 
        query += ' ZIP=? AND'
        to_filter.append(ZIP)

    if StartDate:
        try:
            datetime.datetime.strptime(StartDate, '%Y-%m-%d')
        except ValueError:
            return "Data Not Available or Invalid StartDate - Valid Format YYYY-MM-DD"

        query += ' Date>=? AND'
        to_filter.append(StartDate )
        print(StartDate)

    if EndDate:
        try:
            datetime.datetime.strptime(EndDate, '%Y-%m-%d')
        except ValueError:
            return "Data Not Available or Invalid EndDate - Valid Format YYYY-MM-DD"

        query += ' Date<=? AND'
        to_filter.append(EndDate + '23:59:59')
#    if not (id or published or author):
 #       return page_not_found(404)

    query = query[:-4] + ';'
    print(query)

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
