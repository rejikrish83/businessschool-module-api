
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, status, Path
from datetime import datetime
from bson.json_util import dumps
from utility.QueryBuilder import QueryBuilder
import json
from database.DatabaseUtility import DatabaseUtility
from bson import ObjectId


# Read configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extract MongoDB connection details
mongo_uri = config["mongo"]["uri"]
database_name = config["mongo"]["database_name"]
DATE_FORMAT = "%Y-%m-%d"
router = APIRouter()
queryBuilder = QueryBuilder()

databaseUtill = DatabaseUtility(mongo_uri,database_name)
db = databaseUtill.dataBaseConnection()
modules_collection = db[config["mongo"]["modulesTableName"]]
team_collection = db[config["mongo"]["teamsTableName"]]
users_collection = db[config["mongo"]["usersTableName"]]
course_collection = db[config["mongo"]["courseTableName"]]


@router.get("/get_kpi_data")
async def get_kpi_data(userId: str, date_str: str, role:str, dataType:str, moduleId:str):
    module_id = ObjectId(moduleId)
    try:
        date_obj = datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    pipeline = queryBuilder.queryForKpiData(date_obj, userId,role,module_id, dataType)

    result = list(modules_collection.aggregate(pipeline))

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given parameters")

    return result


@router.get("/get_modules_and_assignments/{userid}")
async def get_modules_and_assignments(userid: str):
    # MongoDB query
    result = modules_collection.aggregate(queryBuilder.buildModuleQuery(userid))

    # Convert the result from MongoDB cursor to a list
    print(result)
    result_list = list(result)
    print(result_list)
    # Check if any modules were found
    if not result_list:
        raise HTTPException(status_code=404, detail="No modules found for the specified student")



    # Return the first item in the result list
    return result_list



@router.get("/unique_data_types")
async def get_unique_data_types(moduleId:str):
    try:
        pipeline = queryBuilder.buildKpiTypeQuery(moduleId)

        result = modules_collection.aggregate(pipeline)
        result_list = list(result)

        if not result_list:
            raise HTTPException(status_code=404, detail="No data types found")

        return result_list[0]["uniqueDataTypes"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{username}", response_model=dict)
def get_user_by_username(username: str = Path(..., title="The username of the user to find")):
    user_document = find_user_by_username(username)
    if user_document:
        return user_document
    else:
        raise HTTPException(status_code=404, detail=f"User with username {username} not found")

@router.get("/course/{courseId}", response_model=dict)
def get_user_by_username(courseId: str = Path(..., title="The username of the user to find")):
    course_id = ObjectId(courseId)
    user_document = find_course_by_courseId(course_id)
    if user_document:
        return user_document
    else:
        raise HTTPException(status_code=404, detail=f"User with username {courseId} not found")

def find_user_by_username(username: str):
    user_document = users_collection.find_one({"username": username})
    if user_document:
        # Convert ObjectId to string using bson.json_util
        user_document["_id"] = str(user_document["_id"])
        return user_document
    return None

def find_course_by_courseId(courseId: ObjectId):
    course_document = course_collection.find_one({"_id": courseId})
    if course_document:
        # Convert ObjectId to string using bson.json_util
        course_document["_id"] = str(course_document["_id"])
        return course_document
    return None