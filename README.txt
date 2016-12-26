User Manual for CSE6242:Team Obe-City
Last Updated: December 5, 2016
Conctact for questions: ichordia3@gatech.edu

Setup:
The primary python scrip is obesity_pipeline.py. 
To run this script for the Yelp data, please download the reviews and business datasets from https://www.yelp.com/dataset_challenge and save the two datasets in the same folder as the script.
You will also need the file obesity_prev_2013 which is the obesity data for each county.
The remaining data is extracted using APIs.

Our pipeline:
1. Calculate the bag of words for a given file (obesity_pipeline.py)
2. Clean and merge the data and store it in a sql database (obesity_pipeline.py)
3. Use Mallet for LDA (instructions below)
4. Use the LDA-extractaed keywords to build a score for each restaurant. The output of this
step was merged with the output of step #2 using Vlookup in Excel.(obesity_pipeline.py)
5. Visualization was done using the Google API. It involved uploading the output from #4 into the Google Maps pre-built visualization. The link is here: https://www.google.com/maps/d/viewer?mid=1mvZTo5DkRQFaGd7-mz4LykUqxIM&ll=34.06025861536214%2C-111.57872808125&z=8



More on Mallet for LDA:

MALLET is a Java-based package for statistical natural language processing, document classification, clustering, topic modelling, information extraction, and other machine learning applications to text.