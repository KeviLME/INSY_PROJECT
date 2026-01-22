#need two thing to run fast api
# FASTAPI and UVICORN
#UNVICORN is ASGI server to run FASTAPI application, in simple words it is used to serve the application

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {
        'message': 'Hello World'
    }


@app.get("/adding/{num1}/{num2}")
async def add(num1: int, num2: int):
    return {
        'results': num1 + num2
    }


@app.get("/name/{your_name}")
async def name(your_name: str):
    return {
        'message': f"hello {your_name}"
    }