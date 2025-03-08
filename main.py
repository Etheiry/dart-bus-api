from fastapi import FastAPI
import psycopg2
import json
import os

app = FastAPI()

# Database connection settings

def get_db_settings():
    with open("db.json") as db_settings:
        data = json.load(db_settings)
        data = data.get("db_settings")
    return data
    
get_db_settings()
def get_db_connection():
    db_settings = get_db_settings()
    return psycopg2.connect(
        dbname=db_settings.get("db_name"), user=db_settings.get("user"), password=db_settings.get("password"), host=db_settings.get("host"), port=db_settings.get("port")
    )

# API endpoint to get all bus routes
@app.get("/routes")
def get_routes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT \"ROUTE\" FROM bus_schedule;")
    routes = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return {"routes": routes}

# API endpoint to get schedule by route
@app.get("/schedule/{route_number}")
def get_schedule(route_number: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT "STOP_SEQUENCE", "TRIPID", "STOP_NAME", "STOP_TIME" FROM bus_schedule WHERE "ROUTE" = %s;',
        (route_number,),
    )
    schedule = [{"stop_sequence": row[0], "trip_id": str(row[1]), "stop_name": row[2], "stop_time": row[3]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return {"route": route_number, "schedule": schedule}



# @app.get("/search/{stop_name}")
# def get_stop(stop_name: str):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         'SELECT "ROUTE", "TRIPID", "STOP_NAME", "STOP_TIME" FROM bus_schedule WHERE "STOP_NAME" LIKE \'%{stop_name}%\';', (stop_name,),
#     )
#     #print(f'SELECT "ROUTE", "TRIPID", "STOP_NAME", "STOP_TIME" FROM bus_schedule WHERE "STOP_NAME" LIKE \'%{stop_name}%\';', stop_name)
#     #stop_details = [{"route": str(row[0]), "trip_id": str(row[1]), "stop_name": str(row[2]), "stop_time": str(row[3])} for row in cursor.fetchall()]
#     cursor.close()
#     conn.close()
#     return {"stop_name": stop_name}
# Run with: uvicorn main:app --port 5434

