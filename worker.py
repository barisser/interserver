import db
import bitsource

def add_message_to_db(message, block, txhash):
  dbstring="INSERT INTO MESSAGES (message, block, txhash) VALUES ('"+str(message)+"','"+str(block)+"','"+str(txhash)+"');"
  response=db.dbexecute(dbstring, False)
  return response

def block_opreturns_to_db(blockn):
  data=bitsource.opreturns_in_block_blockchain(blockn)

  for x in data:
    txhash=str(x[0])
    message=str(x[1])
    k=add_message_to_db(message, str(blockn), txhash)
    print k
  db.dbexecute("UPDATE META SET lastblockdone='" + str(blockn)+"';",False)
