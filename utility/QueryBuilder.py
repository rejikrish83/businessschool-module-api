from bson import ObjectId


class QueryBuilder:

    def __init__(self):
        print("")

    def queryForKpiData(self,date_obj, student_id, role, module_id, dataType):
        #subQuery =  self.buildKpiDataSubQuery(role, student_id, module_id)

        pipeline = [

            {
                "$match": {
                    "$and": [
            {
                "$or": [
                    {"students": student_id},
                    {"moduleAdmins": student_id}

                ]
            },
                        {"_id":ObjectId(module_id)}

        ]
                }
            },

            {
                "$unwind": "$assignments"
            },
            {
                "$unwind": "$assignments.kpiData"
            },
            {
                "$match": {
                    "assignments.kpiData.dataType": dataType,
                    "$expr": {
                        "$eq": [
                            {"$dateFromString": {
                                "dateString": {
                                    "$dateToString": {
                                        "format": "%Y-%m-%d",
                                        "date": {
                                            "$dateFromString": {
                                                "dateString": "$assignments.kpiData.timestamp",
                                                "format": "%Y-%m-%dT%H:%M:%S%z"
                                            }
                                        }
                                    }
                                }
                            }},
                            date_obj
                        ]
                    }
                }
            },
            {
                "$lookup": {
                    "from": "teams",
                    "let": {"teamId": "$assignments.kpiData.teamId"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": [
                                        "$_id",
                                        {"$toObjectId": "$$teamId"}
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "teamInfo"
                }
            },
            {
                "$unwind": "$teamInfo"
            },
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "moduleId": "$moduleId",
                    "moduleName": "$moduleName",
                    "assignmentTitle": "$assignments.title",
                    "teamName": "$teamInfo.teamName",
                    "kpiData": "$assignments.kpiData"
                }
            }
        ]

        return pipeline

    def buildKpiDataSubQuery(self,role, student_id, module_id):
        subQuery = ''
        if role == "Student":
            subQuery = {
                "$match": {"students": student_id, "_id": module_id}
            }
        elif role == "Academic" or role == "Support":
            subQuery = {
                "$match": {"moduleAdmins": student_id, "_id": module_id}
            }
        return subQuery

    def buildModuleQuery(self, student_id):

        pipeline = [
                    {
                        "$match": {
                            "$or": [
                                {"students": student_id},
                                {"moduleAdmins": student_id}
                            ]
                        }
                    },
                    {
                        "$unwind": "$assignments"
                    },
                    {
                        "$unwind": "$assignments.kpiData"
                    },
                    {
                        "$lookup": {
                            "from": "course",
                            "let": {"courseId": "$courseId"},
                            "pipeline": [
                                {
                                    "$match": {
                                        "$expr": {
                                            "$eq": ["$_id", {"$toObjectId": "$$courseId"}]
                                        }
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "modules",
                                        "let": {"courseId": {"$toString": "$_id"}},
                                        "pipeline": [
                                            {
                                                "$match": {
                                                    "$expr": {
                                                        "$eq": ["$courseId", "$$courseId"]
                                                    }
                                                }
                                            },{
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "moduleId": 1,
                    "moduleName": 1,
                    "teamCollaboration": 1,
                    "moduleAdmins": 1,
                    "students":1


                }
            }
                                        ],
                                        "as": "modules"
                                    }
                                },
                                {
                                    "$project": {
                                        "_id": 1,
                                        "courseDesc": 1,
                                        "courseName": 1,
                                        "modules": 1
                                    }
                                }
                            ],
                            "as": "courseDetails"
                        }
                    },
                    {
                        "$unwind": "$courseDetails"
                    },
                    {
                        "$group": {
                            "_id": {"$toString": "$courseDetails._id"},

                            "courseDesc": {"$first": "$courseDetails.courseDesc"},
                            "courseName": {"$first": "$courseDetails.courseName"},
                          "modules": {"$first": "$courseDetails.modules"}
                        }
                    }

                ]

        return pipeline


    def buildKpiTypeQuery(self,module_id):

        pipeline = [
            {
                "$match": {
                    "moduleId": module_id
                }
            },
            {
                "$unwind": "$assignments"
            },
            {
                "$unwind": "$assignments.kpiData"
            },
            {
                "$group": {
                    "_id": "$assignments.kpiData.dataType"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "uniqueDataTypes": {"$addToSet": "$_id"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "uniqueDataTypes": 1
                }
            },
            {
                "$unwind": "$uniqueDataTypes"
            },
            {
                "$sort": {
                    "uniqueDataTypes": 1  # 1 for ascending order, -1 for descending
                }
            },
            {
                "$group": {
                    "_id": None,
                    "uniqueDataTypes": {"$push": "$uniqueDataTypes"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "uniqueDataTypes": 1
                }
            }
        ]
        return pipeline