from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()


hotels = [
    {"id": 1, "title": "Moscow", "name": "moscow"},
    {"id": 2, "title": "Sochi", "name": "sochi"},
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


@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def change_hotel(hotel_id: int,
                 title: str = Body(),
                 name: str = Body()):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            break
    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}")
def changes_hotel(hotel_id: int,
                  title: str | None = Body(None),
                  name: str | None = Body(None)):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            break
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)