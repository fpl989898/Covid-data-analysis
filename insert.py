# save data form cvs file into MongoDB

from pymongo import MongoClient
import csv
import matplotlib.pyplot as plt

us_list = []
cases_list = []
deaths_list = []

def connection():
    conn = MongoClient('localhost', 27017)
    # db = conn.admin
    # db.authenticate('admin', '123123')
    conn.server_info()
    my_db = conn['us_co19'] # get database
    set1 = my_db['us'] # get collection(table)
    set2 = my_db['states']  # get collection(table)
    set1.delete_many({})
    set2.delete_many({})
    return set1, set2

def insertIntoMongodb(set1, set2):
    with open('us.csv','r') as csvfile1:
        # get the data from csv file as Dict format
        reader = csv.DictReader(csvfile1)
        count = 0
        each_list = []
        for each in reader:
            each['cases'] = int(each['cases'])
            each['deaths'] = int(each['deaths'])
            each_list.append(each['date'])
            each_list.append(each['cases'])
            each_list.append(each['deaths'])
            us_list.append(each_list)
            cases_list.append(each['cases'])
            deaths_list.append(each['deaths'])
            set1.insert(each)
            count+=1
    with open('us-states.csv','r') as csvfile2:
        # get the data from csv file as Dict format
        reader = csv.DictReader(csvfile2)
        count = 0
        each_list = []
        for each in reader:
            each['fips'] = int(each['fips'])
            each['cases'] = int(each['cases'])
            each['deaths'] = int(each['deaths'])
            set2.insert(each)
            count+=1

def draw():
    plt.figure(figsize=(10, 8))
    plt.plot(cases_list)
    plt.plot(deaths_list)
    plt.xlabel('days')
    plt.ylabel('number of people')
    plt.legend(['cases', 'deaths'], loc='best')
    plt.show()

def main():
    set1, set2 = connection()
    insertIntoMongodb(set1, set2)
    #draw()
    #print (us_list)
    print("insert data into MongoDB successfully")

if __name__=='__main__':
    main()