import json
from pprint import pprint
import re
import nltk
from nltk import PorterStemmer
import sqlite3
import requests
import csv
from cleanData import clean_merge_data
from calculate_scores import calculate_restaraunt_health_scores

reviews_data = "yelp_academic_dataset_review.json"
restaurant_data = "yelp_academic_dataset_business.json"
db = "yelp.db"

def bag_of_words(json_file, year, dictionary):
    '''
    Input:
        json_file: a json file
        year: string you want word counts for
        dictionary: an empty dictionary with the words you want counts of and values all 0 
    Output:
        returns a list of all the words a dataset for a particular year"
    '''
    data = []
    with open(json_file) as data_file:    
        for line in data_file:
            data.append(json.loads(line))

    numReviews = 0
    reviews = []
    for item in data:
            if(item['date'].find(year) != -1):
                review = item['text'].lower()
                review = re.sub("[^a-zA-Z]", " ", review)
                numReviews = numReviews + 1
                for word in review.split(" "):
                        reviews.append(PorterStemmer().stem_word(word))
    print("NumReviews",numReviews)

    #stem the words in the dictionary so they match
    for item in dictionary.keys():
            item = PorterStemmer().stem_word(item);

    #for word in reviews:
    for word in reviews:
            if(dictionary.get(word) != None):
                    c = dictionary.get(word)
                    c= c+ 1;
                    dictionary[word] = c                   
    return dictionary


if __name__ == '__main__':

    #Find the counts for these words
    counts = {'grease': 0, 'fat': 0, 'sugar':0, 'oil':0,'bacon':0, 'fry':0, 'salt':0,
              'brownie':0, 'cake':0, 'cream':0, 'deep-fried':0, 'fresh':0, 'cheese':0, 'portion':0, 'Mac':0,
              'soda':0, 'coke':0, 'pepsi':0, 'health':0, 'Ishita':0, 'heavy':0, 'buttery':0, 'unhealthy':0,
              'spinach':0, 'shake':0, 'soup':0, 'starch':0, 'carb':0, 'crispy':0, 'salad':0, 'organic':0,
              'broccoli':0,'kale':0, 'quinoa':0, 'gluten':0, 'calorie':0, 'diabetes':0}
    bag_of_words(JSON_FILE2, "2013", counts)

    #Clean & merge all the datasets
    clean_merge_data(reviews_data, restaurant_data, db, "2010")

    #Calculate the healthiness score for each restaurant
    calculate_restaraunt_health_scores("YelpObesityData.csv", "bigram_words.csv") 
