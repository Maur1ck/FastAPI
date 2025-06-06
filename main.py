from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()


hotels = [
    {"id": 1, "title": "Moscow"},
    {"id": 2, "title": "Sochi"}
]


@app.get("/hotels")
def get_hotels(id: int | None = Query(None, description="Айди"),
               title: str | None = Query(None, description="Название отеля")):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)