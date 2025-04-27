from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from paddleocr import PaddleOCR
import base64
import io
from PIL import Image
import numpy as np

app = FastAPI()
# 初始化 PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)

class OCRRequest(BaseModel):
    image: str

@app.post('/ocr')
def ocr_api(body: OCRRequest):
    try:
        # Print the request object
        body_json = body.json()
        print(f"Request object: {body}")
        
       # Decode base64 image
        image_data = base64.b64decode(body.image)
        image = Image.open(io.BytesIO(image_data))

        # Convert image to RGB mode if necessary
        if image.mode not in ("RGB", "L"):  # "L" is grayscale
            image = image.convert("RGB")


        #image.save('temp_image.jpg', format="JPEG")
        image_np = np.array(image)

        # Perform OCR
        result = ocr.ocr(image_np, cls=True)
        text = [line[1][0] for line in result[0]]

        return {"text": text}
    except Exception as e:
        print(f"Exception occurred: {e}")  # Print the exception
        raise HTTPException(status_code=500, detail=str(e))
