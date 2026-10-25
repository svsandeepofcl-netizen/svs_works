#

from fastapi import FastAPI, Query
from typing import List, Dict

app=FastAPI()

EMPLOYEES = [
    {"id":  1, "name": "Alice Johnson",   "department": "Engineering", "salary": 51500},
    {"id":  2, "name": "Bob Smith",        "department": "Sales",       "salary": 53000},
    {"id":  3, "name": "Carol White",      "department": "HR",          "salary": 54500},
    {"id":  4, "name": "David Brown",      "department": "Finance",     "salary": 56000},
    {"id":  5, "name": "Eva Martinez",     "department": "Marketing",   "salary": 57500},
    {"id":  6, "name": "Frank Lee",        "department": "Legal",       "salary": 59000},
    {"id":  7, "name": "Grace Kim",        "department": "Engineering", "salary": 60500},
    {"id":  8, "name": "Henry Wilson",     "department": "Sales",       "salary": 62000},
    {"id":  9, "name": "Isla Thompson",    "department": "HR",          "salary": 63500},
    {"id": 10, "name": "Jack Davis",       "department": "Finance",     "salary": 65000},
    {"id": 11, "name": "Karen Moore",      "department": "Marketing",   "salary": 66500},
    {"id": 12, "name": "Liam Taylor",      "department": "Legal",       "salary": 68000},
    {"id": 13, "name": "Mia Anderson",     "department": "Engineering", "salary": 69500},
    {"id": 14, "name": "Noah Jackson",     "department": "Sales",       "salary": 71000},
    {"id": 15, "name": "Olivia Harris",    "department": "HR",          "salary": 72500},
    {"id": 16, "name": "Paul Martin",      "department": "Finance",     "salary": 74000},
    {"id": 17, "name": "Quinn Garcia",     "department": "Marketing",   "salary": 75500},
    {"id": 18, "name": "Rachel Clark",     "department": "Legal",       "salary": 77000},
    {"id": 19, "name": "Sam Lewis",        "department": "Engineering", "salary": 78500},
    {"id": 20, "name": "Tina Walker",      "department": "Sales",       "salary": 80000},
    {"id": 21, "name": "Uma Hall",         "department": "HR",          "salary": 81500},
    {"id": 22, "name": "Victor Allen",     "department": "Finance",     "salary": 83000},
    {"id": 23, "name": "Wendy Young",      "department": "Marketing",   "salary": 84500},
    {"id": 24, "name": "Xander King",      "department": "Legal",       "salary": 86000},
    {"id": 25, "name": "Yara Scott",       "department": "Engineering", "salary": 87500},
    {"id": 26, "name": "Zoe Adams",        "department": "Sales",       "salary": 89000},
    {"id": 27, "name": "Aaron Baker",      "department": "HR",          "salary": 90500},
    {"id": 28, "name": "Beth Carter",      "department": "Finance",     "salary": 92000},
    {"id": 29, "name": "Chris Evans",      "department": "Marketing",   "salary": 93500},
    {"id": 30, "name": "Diana Foster",     "department": "Legal",       "salary": 95000},
    {"id": 31, "name": "Ethan Green",      "department": "Engineering", "salary": 96500},
    {"id": 32, "name": "Fiona Hill",       "department": "Sales",       "salary": 98000},
    {"id": 33, "name": "George Irwin",     "department": "HR",          "salary": 99500},
    {"id": 34, "name": "Hannah Jones",     "department": "Finance",     "salary": 101000},
    {"id": 35, "name": "Ivan Knight",      "department": "Marketing",   "salary": 102500},
    {"id": 36, "name": "Julia Lane",       "department": "Legal",       "salary": 104000},
    {"id": 37, "name": "Kevin Morgan",     "department": "Engineering", "salary": 105500},
    {"id": 38, "name": "Laura Nash",       "department": "Sales",       "salary": 107000},
    {"id": 39, "name": "Mike Owen",        "department": "HR",          "salary": 108500},
    {"id": 40, "name": "Nina Price",       "department": "Finance",     "salary": 110000},
    {"id": 41, "name": "Oscar Quinn",      "department": "Marketing",   "salary": 111500},
    {"id": 42, "name": "Paula Reed",       "department": "Legal",       "salary": 113000},
    {"id": 43, "name": "Ryan Stone",       "department": "Engineering", "salary": 114500},
    {"id": 44, "name": "Sara Turner",      "department": "Sales",       "salary": 116000},
    {"id": 45, "name": "Tom Underwood",    "department": "HR",          "salary": 117500},
    {"id": 46, "name": "Uma Vance",        "department": "Finance",     "salary": 119000},
    {"id": 47, "name": "Vera Wright",      "department": "Marketing",   "salary": 120500},
    {"id": 48, "name": "Will Xavier",      "department": "Legal",       "salary": 122000},
    {"id": 49, "name": "Xena Young",       "department": "Engineering", "salary": 123500},
    {"id": 50, "name": "Yusuf Zhang",      "department": "Sales",       "salary": 125000},
]

@app.get("/")
def welcome():
    return "Welcome to Fast API"

@app.get("/getemployees", response_model=List[Dict])
def get_employees(page: int = Query(1, ge=1),                 
                  page_size: int = Query(10, ge=1, le=50)
                  ):
    # page_size = 10
    start = (page - 1) * page_size
    end = start + page_size
    return EMPLOYEES[start:end]



