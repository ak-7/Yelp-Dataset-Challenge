# -*- coding:utf-8 -*-
import json
import sqlite3
import requests
import csv

def clean_merge_data(JSON_FILE2, JSON_FILE, DB_FILE, year):
   '''
   Input:
      JSON_FILE2: the Yelp review data
      JSON_FILE: the Yelp business data
      DB_FILE: the name of the database to store the data
      year: the year for which you want all the reviews

   The review dataset, business dataset, obesity dataset,
      demographics dataset, and Census county dataset are all merged
      in sql 

  Output:
      YelpObesityData.csv, the merged final dataset, is outputted
      This dataset is at the review level.
   '''
   
   ##Import reviews before "year"
   reviews = []
   business_ids = dict()      #HashMap so I don't go through the business dataset unnecessarily
   with open(JSON_FILE2, 'r') as f:  
       for line in f:
          line = json.loads(line)
          b_id = line['business_id']
          if(line['date'][:4] <= year):
             reviews.append((b_id, line['date'], line['text'], line['review_id']))
             business_ids[b_id] = 0


   #Import obesity Data-2013
   obesity= []
   with open('obesity_prev_2013.csv', 'r') as f:
       temp = csv.reader(f)
       for line in temp:
          obesity.append(tuple(line))          
   print("finished obesity & review")


   ##Import business dataset
   ## json.loads can only parse 1 line of text/String at a time
   contents = []
   with open(JSON_FILE, 'r') as f:
       for line in f:
          line = json.loads(line)
          b_id = line['business_id']
          if(business_ids.get(b_id, 1) == 0 and "Restaurants" in line['categories']):
             contents.append(line)
             business_ids[b_id] = 1
   print("finished business", len(contents))


   #Get County Name- https://www.fcc.gov/general/census-block-conversions-api    
   business = []
   fipsCode = set()
   for line in contents:
      coordinates = {'format': 'json', 'latitude': line['latitude'], 'longitude': line['longitude'], 'showall': 'false'}                      
      url = 'http://data.fcc.gov/api/block/find'
      try:
          censusData = requests.get(url, params = coordinates)
          censusData = json.loads(censusData.text)
          countyName = censusData['County']['name']
          stateName = censusData['State']['name']
          fips = censusData['County']['FIPS']
          business.append((line['business_id'], countyName, stateName, line['stars'], fips,))
          fipsCode.add(fips)
      except:
          print("can't get FIPS")
   print("finished getting county names %d", len(fipsCode))


   with open('Business.csv', 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(("business_id", "county", "state", "stars", "FIPS"))
       for row in business:
           try:
               writer.writerows(row)
           except:
               print("couldn't write b row")


   #Demographics Data- 2013
   demographics = []
   for line in fipsCode:
      try:
          state = line[:2]
          county = line[2:]
          url = 'http://api.census.gov/data/2013/acs5/profile?get=DP05_0017E,DP05_0024E,DP05_0023E,DP03_0092E,DP05_0032E,DP05_0039E,DP05_0033E,DP05_0066E,DP03_0095E,DP02_0122E,DP05_0034E,DP05_0047E&for=county:%s&in=state:%s&key=74a71d32eb158f947d02a7665f94f4876960c2bc' % (county, state)
          censusData = requests.get(url)
          censusData = json.loads(censusData.text)
          medianAge = censusData[1][0]
          female18Over = censusData[1][1]
          male18Over = censusData[1][2]
          medianIncome = censusData[1][3]
          white = censusData[1][4]
          asian = censusData[1][5]
          black = censusData[1][6]
          hispanic = censusData[1][7]
          pctHealthInsurance = censusData[1][8]
          totalPop = censusData[1][9]
          indianOrAlaskan = censusData[1][10]
          hawaiianPacificIslander = censusData[1][11]   
          demographics.append((line, medianAge, female18Over, male18Over, medianIncome, white, asian, black, hispanic, hawaiianPacificIslander, indianOrAlaskan, pctHealthInsurance, totalPop,))
      except:
         print("cantsaveFIPS");


   with open('Demographics.csv', 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(("FIPS", "medianAge", "female18&Over", "male18&Over", "medianIncome", "Race_White", "Race_Asian", "Race_Black", "Race_Hispanic", "Race_HawaiianPacificIslander", "Race_IndianOrAlaskan", "healthInsurance", "totalPoulation"))
       for row in demographics:
           try:
               writer.writerows(row)
           except:
              print("cantsaveDemographics");
               
      
   #SQLite- Get data joined and in tables
   conn = sqlite3.connect(DB_FILE)
   c = conn.cursor()

   c.execute('CREATE TABLE business (bus_id text, county text, state text, stars real, fips text)')
   c.executemany('INSERT INTO business VALUES (?,?,?,?,?)', business)

   c.execute('CREATE TABLE demographics (fips text, medianAge real, female18Over real, male18Over real, medianIncome real, white real, asian real, black real, hispanic real, hawaiianPacificIslander real, indianOrAlaskan real, pctHealthInsurance real, totalPop real)')
   c.executemany('INSERT INTO demographics VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', demographics)
   c.execute('CREATE TABLE county AS SELECT b.bus_id, b.county, b.state, b.stars, d.* FROM business AS b LEFT OUTER JOIN demographics AS d ON b.fips = d.fips')

   c.execute('CREATE TABLE obesity (state text, fips text, county text, n_obesity real, pct_obesity real, pct_ageadjustedobesity real, n_pa real, pct_pa real, pct_ageadjustedpa real)')
   c.executemany('INSERT INTO obesity VALUES (?,?,?,?,?,?,?,?,?)', obesity)
   c.execute('CREATE TABLE countyobesity AS SELECT b.*, o.n_obesity, o.pct_obesity, o.pct_ageadjustedobesity, o.n_pa, o.pct_pa, o.pct_ageadjustedpa FROM county AS b LEFT OUTER JOIN obesity AS o ON b.fips = o.fips')

   c.execute('CREATE TABLE reviews (bus_id text, date text, review text, review_id text)')
   c.executemany('INSERT INTO reviews VALUES (?,?,?, ?)', reviews)
   c.execute('CREATE TABLE YelpObesityData AS SELECT  countyobesity.*, reviews.date, reviews.review, reviews.review_id FROM reviews INNER JOIN countyobesity ON reviews.bus_id = countyobesity.bus_id')
   conn.commit()
   c.close()


   #EXPORT the data
   conn = sqlite3.connect(DB_FILE)
   c = conn.cursor()
   c.execute('SELECT * FROM YelpObesityData')
   rows = c.fetchall()

   with open('YelpObesityData.csv', 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(("business_id", "county", "state", "stars", "FIPS", "medianAge", "female18&Over", "male18&Over", "medianIncome", "Race_White", "Race_Asian", "Race_Black", "Race_Hispanic", "Race_HawaiianPacificIslander", "Race_IndianOrAlaskan", "healthInsurance", "totalPoulation", "Number_obesity", "Pct_obesity","Pct_ageadjustedobesity", "Num_active", "Pct_active", "Pct_ageadjustedactive", "Date", "Review", "Review_id"))
       writer.writerows(rows)
                         
   conn.commit()
   c.close()
