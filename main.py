from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
from flask import make_response
import db
import json
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
import addresses

@app.route('/')
def something():
  response=make_response("Hey there!", 200)
  response.headers['Access-Control-Allow-Origin']= '*'
  return response

# #SEARCH SPECIFIC ADDRESS
# @app.route('/addresses/<address>')
# def address_query(address=None):
#

#SEARCH SPECIFIC TX
@app.route('/txs/<tx>')  #WORKS
def tx_query(tx=None):
  dbstring="SELECT * FROM messages WHERE txhash='"+tx+"';"
  results=db.dbexecute(dbstring,True)
  results=json.dumps(results)
  response=make_response(str(results), 200)
  response.headers['Access-Control-Allow-Origin']= '*'
  return response

#SEARCH SPECIFIC BLOCK
@app.route('/blocks/<block>')  #WORKS
def block_query(block=None):
  dbstring="SELECT * FROM messages where block='"+block+"';"
  results=db.dbexecute(dbstring,True)
  results=json.dumps(results)
  response=make_response(str(results), 200)
  response.headers['Access-Control-Allow-Origin']= '*'
  return response

#LAST N MESSAGES
@app.route('/messages/<lastn>')  #WORKS
def messages_query(lastn=None):
  dbstring="SELECT * FROM messages ORDER BY block DESC;"
  results=db.dbexecute(dbstring,True)
  lastn=int(lastn)
  results=results[0:lastn]
  results=json.dumps(results)
  response=make_response(str(results), 200)
  response.headers['Access-Control-Allow-Origin']= '*'
  return response

@app.route('/messages/queue', methods=['POST']) #WORDS
def message_queue():
  jsoninput=json.loads(request.data)

  r=addresses.generate_secure_pair()
  public=r['public_address']
  private=r['private_key']
  text=jsoninput['text']

  #CALCULATE COST NOW
  cost=0.002

  #DO SOMETHING WITH TEXT IN DB
  dbstring="insert into text_queue (text, public_address, private_key, amount_expected, success) values ('"+str(text)+"','"+public+"','"+private+"','"+str(int(cost*100000000))+"', 'False');"
  db.dbexecute(dbstring,False)


  results={}
  results['public_address']=public
  results['private_key']=private
  results['cost']=cost
  results=json.loads(results)
  response=make_response(str(results), 200)
  response.headers['Access-Control-Allow-Origin']= '*'
  return response



if __name__ == '__main__':
    app.run()
