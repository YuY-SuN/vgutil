#!/usr/bin/env python3
"""
Vectordb Generationai UTILity
"""

import openai
import chromadb
import os
import json
import sys
import uuid

VGUTIL_MODE = os.getenv("VGUTIL_MODE",None)
VGUTIL_LOG  = os.getenv("VGUTIL_LOG",None)

def _isdebug():
    if VGUTIL_MODE is not None and VGUTIL_MODE == "debug":
        return True
    else:
        return False

def _getlogstream():
    if VGUTIL_LOG is not None :
        return open(VGUTIL_LOG, "a")
    else:
        return sys.stdout

def _debuglog(*args, **kwargs):
    if _isdebug() :
        print("[DBG]", *args, **kwargs, file=_getlogstream())

def _warnlog(*args, **kwargs):
    print("[WARN]", *args, **kwargs, file=_getlogstream())

def openai_init():
    creds = json.load(open(os.getenv("MY_OPENAI_CREDS",f"""{os.environ["HOME"]}/.creds.openai.json""")))
    openai.org = creds["org"]
    openai.api_key = creds["api_key"]

def openai_embedding( text ):
    result = openai.Embedding().create(
        model="text-embedding-ada-002"
    ,   input=text
    )
    if len(result["data"]) > 1:
        _warnlog("resultが複数ある", len(result["data"]))
    return result["data"][0]["embedding"]

## https://docs.trychroma.com/embeddings
## 埋め込みできるんかい、、
def chromadb_add_with_emb( db, text ):
    v = openai_embedding(text)
    db.add(
        embeddings=[v]
    ,   documents=[text]
    ,   ids=[str(uuid.uuid4())]
    )

def chromadb_search_with_emb( db, text, n_results ):
    v = openai_embedding(text)
    result = db.query(
        query_embeddings=v
    ,   n_results=n_results
    )
    return result

def chromadb_tmpcollection():
    return chromadb.Client().create_collection(str(uuid.uuid4())) 

if __name__ == "__main__":
    VGUTIL_MODE = "debug"
    VGUTIL_LOG = None
    _debuglog("this is debug.")
