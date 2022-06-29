from fastapi import FastAPI, Request, File
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from pprint import pprint
import json
from typing import List
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path


app = FastAPI()

paymentlinks = {
    "Schwarz": "https://buy.stripe.com/00g14d1bl9YGcdG5kl",
    "Dunkelbraun" : "https://buy.stripe.com/dR69AJ7zJ4Em4Le8ww",
    "Weiß" : "https://buy.stripe.com/8wM8wFaLV1safpSbIK",
    "Hellbraun" : "https://buy.stripe.com/aEU14d5rBeeW2D6eUX"

}

# "{\"attribute_rahmenfarbe\": \"Schwarz\", \"userpictures\": {\"filename\": \"piconleaf logo.png\",
#  \"content_type\": \"image/png\", \"file\": {}, \"headers\": {\"content-disposition\": 
# \"form-data; name=\\\"userpictures\\\"; filename=\\\"piconleaf logo.png\\\"\", \"content-type\": \"image/png\"}}, 
# \"quantity\": \"1\", \"add-to-cart\": \"16156\", \"product_id\": \"16156\", \"variation_id\": \"16291\"}"


@app.post("/")
async def wpproductpost(request: Request, userpictures: List[bytes] = File(...)):
    da = await request.form()
    da = jsonable_encoder(da)
    # bytes to file
    # print("file is: ", str(userpicture))
    # get filenames
    filename = da["userpictures"]["filename"]
    rahmenfarbe = da["attribute_rahmenfarbe"]
    link = paymentlinks[rahmenfarbe]
    timestring = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    Path("tmppic/%s" % timestring).mkdir(parents=True, exist_ok=True)
    with open("tmppic/%s/order.txt" % (timestring, ), "w") as f:
        f.write(json.dumps(da, indent=4))
        f.write("\n")
        f.write(link)
    for i,file in enumerate(userpictures):
        with open("tmppic/%s/%d.png" % (timestring, i), "wb") as f:
            f.write(file)
    # da["manualfilenames"] = [f.filename for f in files]

    return RedirectResponse(url = link, status_code = 302)

@app.get("/health")
async def health():
    return {"status": "i'm alive boy"}