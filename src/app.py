from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from pprint import pprint
import json

app = FastAPI()


@app.post("/")
async def wpproductpost(request: Request):
    da = await request.form()
    da = jsonable_encoder(da)
    print("i got data:")
    pprint(da)
    return json.dumps(da)

@app.get("/health")
async def health():
    return {"status": "i'm alive boy"}