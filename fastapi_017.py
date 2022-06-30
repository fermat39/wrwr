# uvicorn fastapi_001:app --reload
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
# pip install pydantic
from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel
from Movie import Movie

pgdb = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = pgdb.cursor()

app = FastAPI()

# movies = [{"title":"Batman", "year":2021}]
movies = [
    {"title":"", "year":0}, 
    {"title":"Batman", "year":2021}, 
    {"title":"Joker", "year":2022},
    {"title":"Lion King", "year":1999},
    {"title":"Snow white", "year":1998}, 
    {"title":"Ice age", "year":2012}, 
]

@app.get("/")
async def root():
    return {"message": "환영합니다"}

@app.get("/movies")
def get_movies():
    sql = "SELECT * FROM movies"
    cur.execute(sql)
    movies = cur.fetchall()
    return movies

@app.get("/movie/{movie_id}")
def get_movie(movie_id:int):
    sql = "SELECT * FROM movies WHERE id = %s"
    val = (movie_id, )
    cur.execute(sql, val)
    movies = cur.fetchall()
    return movies[0]

@app.get("/movie_by_title/{movie_title}")
def get_mvoie_by_title(movie_title:str):
    sql = "SELECT * FROM movies WHERE title = %s"
    val = (movie_title, )
    cur.execute(sql, val)
    movie = cur.fetchall()
    if len(movie) == 0:
        raise HTTPException(status_code=500, detail="영화가 존재하지 않습니다")
    return movie[0]

@app.delete("/movie/{movie_id}")
def delete_movie(movie_id:int):
    sql = "DELETE FROM movies WHERE id = %s"
    val = (movie_id, )
    cur.execute(sql, val)
    pgdb.commit()
    return {"message":"영화가 성공적으로 삭제되었습니다."}

@app.post("/create_movie")
def create_movie(movie:Movie):
    sql = "INSERT INTO movies (title, year, sstoryline) VALUES (%s, %s, %s)"
    val = (movie.title, movie.year, movie.storyline)
    cur.execute(sql, val)
    pgdb.commit()
    return movie

@app.post("/update_movie")
def update_movie(movie:Movie, movie_id: int):
    sql = "UPDATE movies SET title = %s, year = %s, storyline = %s WHERE id = %s"
    val = (movie.title, movie.year, movie.storyline, movie_id)
    cur.execute(sql, val)
    pgdb.commit()
    return movie