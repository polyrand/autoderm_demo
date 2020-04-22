from fastapi import FastAPI, Form, UploadFile, Request  # , WebSocket
from fastapi.templating import Jinja2Templates
import requests
import os

# import logging

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

templates = Jinja2Templates(directory=".")

headers = {"Api-Key": os.getenv("API_KEY")}

app = FastAPI()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/img/")
async def process(
    *,
    age: int = Form(...),
    sex: str = Form(...),
    image_uploads: UploadFile = Form(...),
    request: Request,
):

    image_contents = await image_uploads.read()
    received_file = {"Image": image_contents}

    response = requests.post(
        os.getenv("API_URL", "https://autoderm-api.firstderm.com/Query"),
        headers=headers,
        files=received_file,
        data={"AgeYears": age, "Sex": sex, "Language": "EN", "Model": "43PLUS_noo_v3"},
    )

    data = response.json()

    # logging.info(str(data))
    predictions = data["predictions"]

    return templates.TemplateResponse(
        "prediction.html", {"request": request, "predictions": predictions}
    )


# import arel

# hotreload = arel.HotReload(".")
# templates.env.globals["DEBUG"] = os.getenv("DEBUG")  # Development flag.
# templates.env.globals["hotreload"] = hotreload


# @app.websocket("/ws")
# arel.HotReload(".")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


@app.get("/imgt/")
async def preds(request: Request):

    predictions = [
        {
            "confidence": 0.5864430665969849,
            "icd": "B02.9",
            "name": "B02.9: Herpes Zoster",
            "classificationId": "3e4f9cbe-d4aa-11e7-a562-0242ac120003",
            "readMoreUrl": "https://www.firstderm.com/herpes-zoster-shingles/",
        },
        {
            "confidence": 0.01193641684949398,
            "icd": "B00.5",
            "name": "B00.5: Herpes Simplex",
            "classificationId": "3e505aed-d4aa-11e7-a562-0242ac120003",
            "readMoreUrl": "https://www.firstderm.com/herpes-simplex/",
        },
        {
            "confidence": 0.011772023513913155,
            "icd": "L01.0",
            "name": "L01.0: Impetigo",
            "classificationId": "3e507f48-d4aa-11e7-a562-0242ac120003",
            "readMoreUrl": "https://www.firstderm.com/impetigo/",
        },
        {
            "confidence": 0.008549939841032028,
            "icd": "L40.9",
            "name": "L40.9: Psoriasis",
            "classificationId": "3e4fc6ff-d4aa-11e7-a562-0242ac120003",
            "readMoreUrl": "https://www.firstderm.com/psoriasis/",
        },
        {
            "confidence": 0.008327976800501347,
            "icd": "L20.8",
            "name": "L20.8: Neurodermatitis (Lichen Simplex Chronicus)",
            "classificationId": "3e50c7c4-d4aa-11e7-a562-0242ac120003",
            "readMoreUrl": "https://www.firstderm.com/neurodermatitis/",
        },
    ]

    return templates.TemplateResponse(
        "prediction.html", {"request": request, "predictions": predictions}
    )
