from flask import Flask, request
import mysql.connector
import json
import os

db = mysql.connector.connect(
    host="35.224.60.87",
    user="root",
    password=os.getenv('DB_PASSWORD'),
    database="vend"
)

questions = []

cursor = db.cursor()
app = Flask(__name__)


@app.route("/items")
def items():
    cursor.callproc("GetAllItems")
    results = next(cursor.stored_results()).fetchall()

    converted_results = []
    for i in results:
        converted_results.append({"id": i[0], "name": i[1]})

    return json.dumps({"items": converted_results})


@app.route("/locations")
def locations():
    cursor.callproc("GetAllLocations")
    results = next(cursor.stored_results()).fetchall()

    convertedResults = []
    for i in results:
        convertedResults.append({"id": i[0], "description": i[1], "lat": i[2], "lon": i[3]})

    return json.dumps({"locations": convertedResults})


@app.route("/locations/<id>/machines")
def machinesAtLocation(id):
    cursor.callproc("GetMachinesAtLocation", [id])
    results = next(cursor.stored_results()).fetchall()

    convertedResults = []
    for i in results:
        convertedResults.append({"id": i[0], "specific-location": i[1]})

    return json.dumps({"machines": convertedResults})


@app.route("/machines/<id>/items")
def itemsInMachine(id):
    cursor.callproc("GetItemsAtMachine", [id])
    results = next(cursor.stored_results()).fetchall()

    convertedResults = []
    for i in results:
        convertedResults.append({"id": i[0], "name": i[1]})

    return json.dumps({"items": convertedResults})


@app.route("/items/<id>")
def getItemInfo(id):
    cursor.callproc("GetDetailsOfItem", [id])
    results = next(cursor.stored_results()).fetchall()

    convertedResults = []
    for i in results:
        convertedResults.append({"name": i[0], "description": i[1]})

    return json.dumps(convertedResults[0])


@app.route("/items/<id>/machines")
def getMachinesWithItem(id):
    cursor.callproc("GetMachinesWithItem", [id])
    results = next(cursor.stored_results()).fetchall()

    convertedResults = []
    for i in results:
        convertedResults.append({"id": i[0], "location-id": i[1], "last-updated": i[2].strftime("%Y-%m-%d %H:%M:%S")})

    return json.dumps({"machines": convertedResults})


@app.route("/machines/<machineid>/question")
def getQuestion(machineid):
    cursor.callproc("GetItemIdOfOldestEntryForMachine", [id])
    results = next(cursor.stored_results()).fetchall()
    itemid = results[0][0]

    questions.append((machineid, itemid))

    response = {"question-id": len(questions), "item-id": itemid}
    return json.dumps(response)


@app.route("/machines/<machineid>/items/<itemid>/question")
def getSpecificQuestion(machineid, itemid):
    questions.append((machineid, itemid))

    response = {"question-id": len(questions)}
    return json.dumps(response)


@app.route("/questions/<id>", methods=['POST'])
def answerQuestion(id):
    answer = request.json["answer"]
    question = questions[id]
    machine = question[0]
    item = question[1]

    if answer:
        cursor.callproc("AddEntryForItem", [machine, item])
        _ = next(cursor.stored_results()).fetchall()
    else:
        cursor.callproc("RemoveEntryForItem", [machine, item])
        _ = next(cursor.stored_results()).fetchall()

    return ""
