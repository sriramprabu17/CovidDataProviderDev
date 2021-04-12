{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: off\n",
      "2021-02-02\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [10/Apr/2021 12:04:21] \"\u001b[37mGET /api/46217?StartDate=2021-02-02 HTTP/1.1\u001b[0m\" 200 -\n",
      "127.0.0.1 - - [10/Apr/2021 12:15:33] \"\u001b[37mGET / HTTP/1.1\u001b[0m\" 200 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2021-02-02\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [10/Apr/2021 12:26:37] \"\u001b[37mGET /api/46217?StartDate=2021-02-02&EndDate=2021-02-02 HTTP/1.1\u001b[0m\" 200 -\n",
      "127.0.0.1 - - [10/Apr/2021 12:26:37] \"\u001b[33mGET /favicon.ico HTTP/1.1\u001b[0m\" 404 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2021-02-02\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [10/Apr/2021 12:26:45] \"\u001b[37mGET /api/46217?StartDate=2021-02-02&EndDate=2021-02-03 HTTP/1.1\u001b[0m\" 200 -\n",
      "127.0.0.1 - - [10/Apr/2021 12:26:45] \"\u001b[33mGET /favicon.ico HTTP/1.1\u001b[0m\" 404 -\n"
     ]
    }
   ],
   "source": [
    "from werkzeug.wrappers import Request, Response\n",
    "from flask import Flask\n",
    "\n",
    "def dict_factory(cursor, row):\n",
    "    d = {}\n",
    "    for idx, col in enumerate(cursor.description):\n",
    "        d[col[0]] = row[idx]\n",
    "    return d\n",
    "\n",
    "\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "@app.route(\"/\")\n",
    "def hello():\n",
    "    return \"Hello World!\"\n",
    "\n",
    "@app.route('/api/<ZIP>', methods=['GET'])\n",
    "def api_filter(ZIP):\n",
    "    query_parameters = request.args\n",
    "\n",
    "    id = query_parameters.get('ZIP')\n",
    "    StartDate = query_parameters.get('StartDate')\n",
    "    EndDate = query_parameters.get('EndDate')\n",
    "\n",
    "    query = \"SELECT * FROM APIData WHERE\"\n",
    "    to_filter = []\n",
    "\n",
    "    if ZIP:\n",
    "        query += ' ZIP=? AND'\n",
    "        to_filter.append(ZIP)\n",
    "    if StartDate:\n",
    "        query += ' Date>=? AND'\n",
    "        to_filter.append(StartDate)\n",
    "        print(StartDate)\n",
    "    if EndDate:\n",
    "        query += ' Date<=? AND'\n",
    "        to_filter.append(EndDate)\n",
    "#    if not (id or published or author):\n",
    " #       return page_not_found(404)\n",
    "\n",
    "    query = query[:-4] + ';'\n",
    "\n",
    "    conn = sqlite3.connect('CovidAPI.db')\n",
    "    conn.row_factory = dict_factory\n",
    "    cur = conn.cursor()\n",
    "\n",
    "    results = cur.execute(query, to_filter).fetchall()\n",
    "\n",
    "    return jsonify(results)\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'cur' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-10-b85d16318ade>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mresults\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mcur\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mexecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mquery\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mto_filter\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mfetchall\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mreturn\u001b[0m \u001b[0mjsonify\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mresults\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mNameError\u001b[0m: name 'cur' is not defined"
     ]
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
