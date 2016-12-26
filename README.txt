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

MALLET is a Java-based package for statistical natural language processing, document classification, clustering, topic modelling, information extraction, and other machine learning applications to text.Topic models are useful for analyzing large collections of unlabeled text. The MALLET topic modeling toolkit contains efficient, sampling-based implementations of Latent Dirichlet AllocationThe MALLET topic model package includes an extremely fast and highly scalable implementation of Gibbs sampling, efficient methods for document-topic hyperparameter optimization, and tools for inferring topics for new documents given trained models.Importing Documentsbin\mallet import-dir --input sample-data/dva --output topic-input.mallet --keep-sequence --remove-stopwordsBuilding Topic Models:bin\mallet train-topics --input topic-input.mallet --num-topics 50 --num-top-words 10 --num-iterations 5000  --optimize-interval 10  --output-state topic-state.gz --output-topic-keys topic-keys.gzOutput: This file contains a "key" consisting of the top k words for each topic (where k is defined by the --num-top-words option). This output can be useful for checking that the model is working as well as displaying results of the model. In addition, this file reports the Dirichlet parameter of each topic. If hyperparamter optimization is turned on, this number will be roughly proportional to the overall portion of the collection assigned to a given topic.
