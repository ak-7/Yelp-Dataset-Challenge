import pandas as pd
import numpy as np
import csv

def calculate_restaraunt_health_scores(yelpObesityData, ldaWords):
    '''
    Input:
        Yelp review level data,
        the words obtained from LDA (bigram or unigram) with a healthines score for each word

    For each restaurant, this script finds all the LDA words in the restaurant's reviews.
    It then averages the score by the number of restaurants and normalizes the score so its between -5 and 5.
        
    Output:
        mycsvfile.csv, a file that has a healthiness score for each restaurant
    
    '''
    
        df = pd.read_csv(yelpObesityData)
        column = df.Review
        business_ids = df.business_id
        my_Set = set(business_ids)
        unique_business_ids = list(my_Set)
        count = dict((val,0) for val in unique_business_ids)
        num_restaurants = dict((val,0) for val in unique_business_ids)
        i=0
        pos_dict={}

        #read words from the csv file and store then in a dictionary.
        with open(ldaWords) as f:
                reader = csv.reader(f, delimiter=',', quotechar='"')
                for row in reader:
                        pos_dict[row[0]] = row[1]
        dict = pos_dict
        print dict
        i=0
        j=0
        for key in dict.keys():			#iterate through the keys of the dictionary consisting of all words.
                for review in column:		#iterate through all reviews.
                        if '_' not in key:		#check if the word is a unigram or a bigram, if there is an _ in the token then it is a bigram word
                                val = float(dict[key])	#unigram word
                                if key.lower() in review.lower():
                                        count[business_ids[i]] = count[business_ids[i]] + val		#if the word exists in the review add its value to a count array for each restaurant
                                        num_restaurants[business_ids[i]] = num_restaurants[business_ids[i]] + 1  		#keep track of the number of reviews for each restaurant
                        else:						#bigram word
                                val = float(dict[key])
                                k = key.split("_")		
                                if k[0].lower() in review.lower() and k[1].lower() in review.lower():			#if both words in the bigram are in the review, add to the value of that restaurant
                                        count[business_ids[i]] = count[business_ids[i]] + val
                                        num_restaurants[business_ids[i]] = num_restaurants[business_ids[i]] + 1
                        i+=1
                i=0
                
        #divide the score for each restaurant by the number of reviews. 
        for key in count.keys():
                if count[key]!= 0:
                        count[key] = float(count[key])/num_restaurants[key]				
        values = count.values()
        max = np.max(values)
        min = np.min(values)
        j=0

        #normalize the scores so that they are between 0-5
        for key in count.keys():
                count[key] = 0 + 5.0 * (count[key]-min)/(max-min)
        print count
        print max,min
        print "this would" in column[0].lower()
        with open('mycsvfile.csv', 'wb') as f:  
            w = csv.DictWriter(f, count.keys())
            w.writeheader()
            w.writerow(count)
