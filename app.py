from fastapi import FastAPI

app = FastAPI()

def calculate_area(length: float, width: float) -> float:
    return length * width

@app.get("/area")
async def get_area(length: float, width: float):
    area = calculate_area(length, width)
    return {"length": length, "width": width, "area": area}
