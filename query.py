from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np


def connection():
    conn = MongoClient('localhost', 27017)
    conn.server_info()
    my_db = conn['us_co19'] # get database
    set1 = my_db['us'] # get collection(table)
    set2 = my_db['states']  # get collection(table)
    return set1, set2

def draw1(cases, deaths):
    plt.figure(figsize=(10, 8))
    plt.plot(cases)
    plt.plot(deaths)
    plt.xlabel('days')
    plt.ylabel('number of people')
    plt.legend(['cases', 'deaths'], loc='best')
    plt.show()

def draw2(cases, deaths, cases_day, deaths_day):
    plt.figure(figsize=(10, 10))
    plt.figure(1)
    ax1 = plt.subplot(221)
    ax1.plot(cases, color="b")
    ax1.set_title('cases over a month')

    ax2 = plt.subplot(222)
    ax2.plot(deaths, color="y")
    ax2.set_title('deaths over a month')

    X = np.arange(len(cases_day))
    ax3 = plt.subplot(223)
    ax3.bar(X, cases_day, color="b")
    ax3.set_title('cases incremented by day')

    ax4 = plt.subplot(224)
    ax4.bar(X, deaths_day, color="y")
    ax4.set_title('deaths incremented by day')
    plt.show()

def main():
    set1, set2 = connection()

    # Query1: Get the information and graphs about a given state
    target_state = "New York"
    cursor = set2.find({"state": target_state}, {"_id": 0})
    state_cases_list = []
    state_deaths_list = []
    day_increment_cases = []
    day_increment_deaths = []
    for doc in cursor:
        state_cases_list.append(doc['cases'])
        state_deaths_list.append(doc['deaths'])
        print(doc)
    # draw1(state_cases_list,state_deaths_list)
    for i in range(0, len(state_cases_list)):
        if i > 0:
            day_increment_cases.append(state_cases_list[i]-state_cases_list[i-1])
            day_increment_deaths.append(state_deaths_list[i] - state_deaths_list[i - 1])
    draw2(state_cases_list, state_deaths_list, day_increment_cases, day_increment_deaths)

    # Query2: The max cases on one day
    target_date = '2020-11-07'
    cursor = set2.aggregate([
        {'$match': {'date': target_date}},
        {
            '$group': {
                '_id': '$date', 'cases': {'$max': '$cases'}
            }
        }
    ]) # pipeline as parameter
    print("Max cases on "+target_date+" is")
    for doc in cursor:
        print(doc)

    # Query3: States of "deaths > 5000"
    deaths_target = 5000
    cursor = set2.find({"$and": [
        {
            "date": target_date,
            "deaths": {"$gt": deaths_target} # >
        }
    ]}, {"_id": 0, "date": 0, "cases": 0})
    print("States of deaths > 5000 :")
    for doc in cursor:
        print(doc)

    # Query4: Average of each state over a month
    cursor = set2.aggregate([
        {
            '$group': {
                '_id': '$state',
                'cases_avg': {'$avg': '$cases'},
                'deaths_avg': {'$avg': '$deaths'}
            }
        },
        {'$project': {
            '_id': 1,
            'cases_avg': {'$trunc': '$cases_avg'},
            'deaths_avg': {'$trunc': '$deaths_avg'}}}
    ])
    print("Average(cases & deaths) of each state :")
    for doc in cursor:
        print(doc)

if __name__=='__main__':
    main()