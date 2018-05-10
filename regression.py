"""
A script that reads feature.csv and does the prediction. It also reports the accuracy.

author:-Shradha Nayak,Ankita Sawant,Vandna Yadav

"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
import pandas
import sklearn
import numpy as np
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.grid_search import GridSearchCV

csv=pandas.read_csv('feature.csv')
#Randomizing data
df1=csv.reindex(np.random.permutation(csv.index))

#creating train-70% and test-30% data set
count=len(csv)
trainCount=int((70*count)/100)
testCount=(count-trainCount)
rev_train=df1[0:trainCount]
rev_test=df1[trainCount+1:count]
labels_test=rev_test['Reviewer_Ratings']
labels_train=rev_train['Reviewer_Ratings']
rev_test.drop('Reviewer_Ratings', axis=1, inplace=True)
rev_train.drop('Reviewer_Ratings', axis=1, inplace=True)

#Normalising data
rev_train_Norm = sklearn.preprocessing.normalize(rev_train, norm='l2')
rev_test_Norm=sklearn.preprocessing.normalize(rev_test, norm='l2')


################### KNN #############################################
#build a 3-KNN classifier on the training data
KNN=KNeighborsClassifier(5)
KNN.fit(rev_train_Norm.astype(int),labels_train.astype(int))
predicted=KNN.predict(rev_test_Norm)
print 'Accuracy of KNN: '+ str(accuracy_score(predicted,labels_test))

################### KNN with weights ################################

#build the parameter grid
param_grid = [
  {'n_neighbors': [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31],'weights':['uniform','distance']}
]

#build a grid search to find the best parameters
clf = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)

#run the grid search
clf.fit(rev_train_Norm.astype(int),labels_train.astype(int))

#print the score for each parameter setting
for params, mean_score, scores in clf.grid_scores_:
    print params, mean_score

#print the best parameter setting
print "\nBest parameters",clf.best_params_


KNN=KNeighborsClassifier(n_neighbors=clf.best_params_['n_neighbors'])
KNN.fit(rev_train_Norm.astype(int),labels_train.astype(int))
#use the classifier to predict
predicted=KNN.predict(rev_test_Norm)
#print the accuracy
print 'Accuracy of KNN with weights: ' + str(accuracy_score(predicted,labels_test))


############################# LogisticRegression ########################

#build a Logistic Regression classifier on the training data
LR=LogisticRegression ()
LR.fit(rev_train_Norm,labels_train)
#use the classifier to predict
predicted=LR.predict(rev_test_Norm)
#print the accuracy
print 'Accuracy of Logistic Regression: '+ str(accuracy_score(predicted,labels_test))


################## Naive Bayes ########################

clf3 = MultinomialNB()
clf3.fit(rev_train_Norm,labels_train)
pred=clf3.predict(rev_test_Norm)
print 'Accuracy of Naive Bayes: '+ str(accuracy_score(pred,labels_test))

################# Random Forest ########################

clf3 = RandomForestClassifier(n_estimators=100)
clf3.fit(rev_train_Norm,labels_train)
pred=clf3.predict(rev_test_Norm)
print 'Accuracy of Random Forest: '+ str(accuracy_score(pred,labels_test))


######### Combination of KNN, Random Forest & Logistic Regression #######################

clf1 = LogisticRegression()
clf2 = KNeighborsClassifier(5)
clf3 =RandomForestClassifier(n_estimators=100)
eclf = VotingClassifier(estimators=[('lr', clf1), ('knn', clf2), ('rf',clf3)], voting='hard')
eclf.fit(rev_train_Norm,labels_train)
pred=eclf.predict(rev_test_Norm)
print 'Accuracy of Voting Classifier: '+ str(accuracy_score(pred,labels_test))

