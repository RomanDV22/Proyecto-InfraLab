from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def root():

    print("\n")

    return {
        "mensaje": "InfraLab funcionando",
        "estado": "online"
    }
