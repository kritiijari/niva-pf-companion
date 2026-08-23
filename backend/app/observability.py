import json, logging, uuid
logger=logging.getLogger("niva")
def request_id(): return str(uuid.uuid4())
def log(event:str,request_id:str,**fields): logger.info(json.dumps({"event":event,"request_id":request_id,**fields},default=str))
