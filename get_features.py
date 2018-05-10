"""
A script that reads the raw data (html files), cleans it, extracts the desired features and saves these features in feature.csv 

author:-Shradha Nayak,Ankita Sawant,Vandna Yadav

"""

import urllib2,os,sys,time
def makeDirec(loc):
    if not os.path.exists(loc):os.mkdir(loc)


#extract all the reviewers
import re
reviewerList=[]
reviewAddList=[]
reviewCombine=[]
fconn1=open('data/user_list.html')
html1=fconn1.read()
fconn1.close()
reviewers=re.finditer('<a title=".*?" href="/user/show/(.*?)-(.*?)">',html1)
#print reviewers
for r in reviewers:
    #print r.group(1)
    reviewAddList.append(r.group(1))
    reviewerList.append(r.group(2))
    reviewCombine.append(r.group(1)+'-'+r.group(2))


#extract all reviews
import re
import urllib2,os,sys,time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys


#Lists
GenreList=[]
totalcommentList=[]
reviewerList=[]
bookList=[]
authorName=[]
isbnList=[]
ratingList=[]
likeList=[]
bookDatePubList=[]
reviewerRating=[]
reviewsList=[]
dateAddedReadList=[]
dateReadList=[]

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def encodeFunc(a):
    a=a.encode('ascii','ignore')
    if a is None:
        a='None'
    return a
def removeChar(char,text):
    a=text.encode('ascii','ignore')
    a=re.sub(char,'',a)
    return a
#retrieve genre of the book
def calldriverforGenre(url):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    html=driver.page_source
    time.sleep(2)
    genre=re.search('<a class="actionLinkLite bookPageGenreLink" href=".*?">(.*?)</a>',html)
    if genre is not None:
        gen=genre.group(1)
    else:
        gen='-'
    return gen

def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None

def calldriverforComments(url):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    html=driver.page_source
    tree=BeautifulSoup(html, 'lxml')
    com1=tree.findAll('div',{'class':'h2Container gradientHeaderContainer'})
    for f in com1:
        value=f.text
        value=encodeFunc(value)# remove non-utf 8 characters
        #print value
        if 'Comments' in value:
            com2=f.find('h2',{'class':'brownBackground'})
            com3=com2
            #.find('span',{'class':'smallText'})
            #print com3
            #comment=re.search('Comments.*?<span class="smallText">(showing.*?of (.*?))</span>',html)
            if com3 is not None:
                com=com3.text
                #print com
                com4=com.strip()
                com5=re.sub('\n',' ',com4)
                com6=re.sub('\)','',com5)
                com7=re.sub('\(','',com6)
                com8=com7.split(' ')
                com9=com8[int(len(com8)-2)]
                #print value
                #value1=re.sub('\)','',value)

        else:
            com9='-'
    print 'comment '+com9
    return com9  
    
    
def parse(html1,reviewer_name):
    
    name=re.search('<a href="/user/show/(.*?)">.*?</a>',html1)
    if name is not None:
        nametext=name.group(1)
        nametext1 = ''.join([i for i in nametext if not i.isdigit()])
        nametext2=re.sub('-','',nametext1)
        #print 'name'+reviewer_name
        tree=BeautifulSoup(html1, 'lxml')
        bookalike=tree.findAll('tr',{'class':'bookalike review'})

        for b in bookalike:
            #reviewer
            reviewerList.append(reviewer_name)

            #book name
            books=b.find('td',{'class':'field title'})
            book=books.text
            book1=re.sub('title','',book)
            book2=re.sub('\n','',book1)
            book3=re.sub('  +','',book2)
            book3=encodeFunc(book3)
            #print 'book name:'+book3
            bookList.append(book3)
            glist=[]
            #genre
            for a in b.find_all('a', href=True):
                glist.append(a['href'])
                #print "Found the URL:", a['href']
                m = re.match('/review/show.*?', a['href'])
                if m:
                    extraCommentAdd=a['href']
            genreAdd=glist[1]
            genreURL='https://www.goodreads.com'+genreAdd
            gen=calldriverforGenre(genreURL)
            #print gen
            GenreList.append(gen)
            extraCommentAddURL='https://www.goodreads.com'+extraCommentAdd
            comment=calldriverforComments(extraCommentAddURL)
            totalcommentList.append(comment)
            
            #author name
            author=b.find('td',{'class':'field author'})
            a=author.text
            a1=re.sub('author ','',a)
            a2=re.sub('\n','',a1)
            a3=re.sub(r'[\*]','',a2)
            a3=encodeFunc(a3)
            #print 'author:'+a3
            authorName.append(a3)

            #isbn
            isbn=b.find('td',{'class':'field isbn'})
            isbn1=isbn.find('div',{'class':'value'})
            i=isbn1.text
            i1=removeChar('\n',i)
            i=encodeFunc(i1)
            #print 'isbn:'+i
            i=removeChar(' ',i)
            if i == 'isbn':
                i1='-'
            elif i=='None':
                i1='-'
            elif i=='':
                i1='-'
            else:
                i1=i

            isbnList.append(i1)

            #rating
            rating=b.find('td',{'class':'field avg_rating'})
            ratingVal=rating.find('div',{'class':'value'})
            r=ratingVal.text
            r1=re.sub('\n','',r)
            r=encodeFunc(r1)
            ratingList.append(r)
            #print 'rating :'+r
            if r >2:
                likeList.append('Good')
                #print 'Good'
            elif r< 3:
                likeList.append('Bad')
                #print 'Bad'


            #date published
            bookDate=b.find('td',{'class':'field date_pub'})
            bookDateVal=bookDate.find('div',{'class':'value'})
            bookDatePub=bookDateVal.text
            bookDatePub=removeChar('\n',bookDatePub)
            bookDatePub=removeChar(' ',bookDatePub)
            if bookDatePub =='unknown':
                bookDate1=b.find('td',{'class':'field date_pub_edition'})
                bookDateVal1=bookDate1.find('div',{'class':'value'})
                bookDatePub1=bookDateVal1.text
                bookDatePub1=removeChar('\n',bookDatePub1)
                bookDatePub1=removeChar(' ',bookDatePub1)
                if bookDatePub1 is not 'unknown':
                    bookDatePubList.append(bookDatePub1)
                else:
                    bookDatePubList.append('-')
            else:
                bookDatePubList.append(bookDatePub)

            #reviewRating
            reviewrating=b.find('td',{'class':'field rating'})
            rw1=reviewrating.find('div',{'class':'value'})
            rw2=rw1.find('span',{'class':' staticStars'})
            rw3=rw2.text
            if rw3 == 'None':
                reviewerRating.append('-')
            elif rw3=='':
                reviewerRating.append('-')
            else:
                reviewerRating.append(rw3)


            #field review"
            review=b.find('td',{'class':'field review'})
            review1=review.find('div',{'class','value'})
            rw2=review1.find('span',id=re.compile(r'freeTextContainerreview.*'))
            rw=str(rw2)
            if rw is not 'None':
                rw3=remove_tags(rw)
                if rw3=='None':
                    reviewsList.append('-')
                else:
                    reviewsList.append(rw3)
            else:
                reviewsList.append('-')


            #date added
            dateAddRead=b.find('td',{'class':'field date_added'})
            dAR=dateAddRead.find('div',{'class':'value'})
            dAR1=removeChar('\n',dAR.text)
            dAR2=removeChar(' ',dAR1)
            #print dAR1
            dateAddedReadList.append(dAR2)
            dar=datetime.datetime.strptime(dAR2, '%b%d,%Y').date()


            #date read
            dateRead=b.find('td',{'class':'field date_read'})
            dR=dateRead.find('div',{'class':'value'})
            dR1=removeChar('\n',dR.text)

            #print dR1
            if dR1 == 'not set':
                end_date = dar + datetime.timedelta(days=2)
                end_date1=end_date.strftime('%b %d,%Y')
                dateReadList.append(end_date1)
            else:
                dR2=removeChar(' ',dR1)
                dateReadList.append(dR2)
        
        
        
def callReviewFunc(r):
    #pageNo=1
    
    url='https://www.goodreads.com/review/list/'+r+'?order=d&sort=review&view=reviews'
    
    print 'URL:'+url

    #open the browser and visit the url
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    html=driver.page_source
    
    
    #################################################################################################
    
    #print 'page '+str(pageNo)+' done'
    page=2
    cssPath='a.siteHeader__topLevelLink'
    try:
        button=driver.find_element_by_css_selector(cssPath)
    except:
        error_type, error_obj, error_info = sys.exc_info()
        print 'STOPPING - COULD NOT FIND THE LINK TO PAGE: ', page
        print error_type, 'Line:', error_info.tb_lineno
        
    #click the button to go the next page, then sleep    
    
    time.sleep(2)
    button.click()
    
    html1=driver.page_source
    
    
    #############################################
       
    wait = ui.WebDriverWait(driver, 3)
    wait.until(page_is_loaded)
    email_field = driver.find_element_by_id("userSignInFormEmail")
    email_field.send_keys("anki.sawant@gmail.com")
    password_field = driver.find_element_by_id("user_password")
    password_field.send_keys("shardavijay")
    password_field.submit()
    time.sleep(2)
       
    ##########################################################
    time.sleep(2)
    driver.get(url)
    html=driver.page_source
    
    parse(driver.page_source,r)
    
    
    ###########################################################################################################

    
i=1
for r  in reviewCombine:
    callReviewFunc(r)
    print 'PAGE:'+str(i)+' done'
    i=i+1


#Creating a dataframe to store the data

from pandas import DataFrame
df = DataFrame({'Book':bookList,'Author':authorName,'ISBN':isbnList,'Average book Rating':ratingList,'Reviewer Name':reviewerList,'Book published date':bookDatePubList,'Reviewer Rating':reviewerRating,'Review':reviewsList,'Book added date':dateAddedReadList,'Book read date':dateReadList,'Genre':GenreList,'Count of people interaction':totalcommentList})



#For converting the dataframe to csv
df.to_csv('intermediate1.csv', sheet_name='sheet1', index=False)



import pandas as pd

#Reading the csv created above
csvData=pd.read_csv("intermediate1.csv")

########For converting the Genre values to 0/1

csvData["Action"] = csvData['Genre'].str.count("Action")
csvData["Adult"] = csvData['Genre'].str.count("Adult")
csvData["Adult Fiction"] = csvData['Genre'].str.count("Adult Fiction")
csvData["Adventure"] = csvData['Genre'].str.count("Adventure")
csvData["Autobiography"] = csvData['Genre'].str.count("Autobiography")
csvData["Biography"] = csvData['Genre'].str.count("Biography")
csvData["Childrens"] = csvData['Genre'].str.count("Childrens")
csvData["Classics"] = csvData['Genre'].str.count("Classics")
csvData["Comics"] = csvData['Genre'].str.count("Comics")
csvData["Contemporary"] = csvData['Genre'].str.count("Contemporary")
csvData["Cultural"] = csvData['Genre'].str.count("Cultural")
csvData["Dark"] = csvData['Genre'].str.count("Dark")
csvData["Disability"] = csvData['Genre'].str.count("Disability")
csvData["Economics"] = csvData['Genre'].str.count("Economics")
csvData["Erotica"] = csvData['Genre'].str.count("Erotica")
csvData["Fantasy"] = csvData['Genre'].str.count("Fantasy")
csvData["Fiction"] = csvData['Genre'].str.count('Fiction')
csvData["Glbt"] = csvData['Genre'].str.count("Glbt")
csvData["Historical"] = csvData['Genre'].str.count("Historical")
csvData["Historical Fiction"] = csvData['Genre'].str.count("Historical Fiction")
csvData["History"] = csvData['Genre'].str.count("History")
csvData["Horror"] = csvData['Genre'].str.count("Horror")
csvData["Humor"] = csvData['Genre'].str.count("Humor")
csvData["Literature"] = csvData['Genre'].str.count("Literature")
csvData["Magical Realism"] = csvData['Genre'].str.count("Magical Realism")
csvData["Media Tie In"] = csvData['Genre'].str.count("Media Tie In")
csvData["Military History"] = csvData['Genre'].str.count("Military History")
csvData["Music"] = csvData['Genre'].str.count("Music")
csvData["Mystery"] = csvData['Genre'].str.count("Mystery")
csvData["New Adult"] = csvData['Genre'].str.count("New Adult")
csvData["Nonfiction"] = csvData['Genre'].str.count('Nonfiction')
csvData["Paranormal"] = csvData['Genre'].str.count("Paranormal")
csvData["Philosophy"] = csvData['Genre'].str.count("Philosophy")
csvData["Plays"] = csvData['Genre'].str.count("Plays")
csvData["Poetry"] = csvData['Genre'].str.count("Poetry")
csvData["Politics"] = csvData['Genre'].str.count("Politics")
csvData["Race"] = csvData['Genre'].str.count("Race")
csvData["Realistic Fiction"] = csvData['Genre'].str.count("Realistic Fiction")
csvData["Romance"] = csvData['Genre'].str.count("Romance")
csvData["Science"] = csvData['Genre'].str.count("Science")
csvData["Science Fiction"] = csvData['Genre'].str.count("Science Fiction")
csvData["Sequential Art"] = csvData['Genre'].str.count("Sequential Art")
csvData["Short Stories"] = csvData['Genre'].str.count("Short Stories")
csvData["Social Issues"] = csvData['Genre'].str.count("Social Issues")
csvData["Sports and Games"] = csvData['Genre'].str.count("Sports and Games")
csvData["Suspense"] = csvData['Genre'].str.count("Suspense")
csvData["Thriller"] = csvData['Genre'].str.count("Thriller")
csvData["War"] = csvData['Genre'].str.count("War")
csvData["Western"] = csvData['Genre'].str.count("Western")
csvData["Young Adult"] = csvData['Genre'].str.count("Young Adult")



####Assigning numbers to different genres for the purpose of plotting

genreValueList=[]
i=0
genreValue=0
while i < len(csvData):
    if str(csvData['Genre'][i]) == 'Action':
        genreValue=1
    elif str(csvData['Genre'][i]) == 'Adult':
        genreValue=2
    elif str(csvData['Genre'][i]) == 'Adult Fiction':
        genreValue=3
    elif str(csvData['Genre'][i]) == 'Adventure':
        genreValue=4   
    elif str(csvData['Genre'][i]) == 'Autobiography':
        genreValue=5
    elif str(csvData['Genre'][i]) == 'Biography':
        genreValue=6
    elif str(csvData['Genre'][i]) == 'Childrens':
        genreValue=7
    elif str(csvData['Genre'][i]) == 'Classics':
        genreValue=8
    elif str(csvData['Genre'][i]) == 'Comics':
        genreValue=9
    elif str(csvData['Genre'][i]) == 'Contemporary':
        genreValue=10
    elif str(csvData['Genre'][i]) == 'Cultural':
        genreValue=11
    elif str(csvData['Genre'][i]) == 'Dark':
        genreValue=12
    elif str(csvData['Genre'][i]) == 'Disability':
        genreValue=13
    elif str(csvData['Genre'][i]) == 'Economics':
        genreValue=14
    elif str(csvData['Genre'][i]) == 'Erotica':
        genreValue=15
    elif str(csvData['Genre'][i]) == 'Fantasy':
        genreValue=16
    elif str(csvData['Genre'][i]) == 'Fiction':
        genreValue=17
    elif str(csvData['Genre'][i]) == 'Glbt':
        genreValue=18
    elif str(csvData['Genre'][i]) == 'Historical':
        genreValue=19
    elif str(csvData['Genre'][i]) == 'Historical Fiction':
        genreValue=20
    elif str(csvData['Genre'][i]) == 'History':
        genreValue=21
    elif str(csvData['Genre'][i]) == 'Horror':
        genreValue=22
    elif str(csvData['Genre'][i]) == 'Humor':
        genreValue=23
    elif str(csvData['Genre'][i]) == 'Literature':
        genreValue=24
    elif str(csvData['Genre'][i]) == 'Magical Realism':
        genreValue=25
    elif str(csvData['Genre'][i]) == 'Media Tie In':
        genreValue=26
    elif str(csvData['Genre'][i]) == 'Military History':
        genreValue=27
    elif str(csvData['Genre'][i]) == 'Music':
        genreValue=28
    elif str(csvData['Genre'][i]) == 'Mystery':
        genreValue=29
    elif str(csvData['Genre'][i]) == 'New Adult':
        genreValue=30
    elif str(csvData['Genre'][i]) == 'Nonfiction':
        genreValue=31
    elif str(csvData['Genre'][i]) == 'Paranormal':
        genreValue=31
    elif str(csvData['Genre'][i]) == 'Philosophy':
        genreValue=33
    elif str(csvData['Genre'][i]) == 'Plays':
        genreValue=34
    elif str(csvData['Genre'][i]) == 'Poetry':
        genreValue=35
    elif str(csvData['Genre'][i]) == 'Politics':
        genreValue=36
    elif str(csvData['Genre'][i]) == 'Race':
        genreValue=37
    elif str(csvData['Genre'][i]) == 'Realistic Fiction':
        genreValue=38
    elif str(csvData['Genre'][i]) == 'Romance':
        genreValue=39
    elif str(csvData['Genre'][i]) == 'Science':
        genreValue=40
    elif str(csvData['Genre'][i]) == 'Science Fiction':
        genreValue=41
    elif str(csvData['Genre'][i]) == 'Sequential Art':
        genreValue=42
    elif str(csvData['Genre'][i]) == 'Short Stories':
        genreValue=43
    elif str(csvData['Genre'][i]) == 'Social Issues':
        genreValue=44
    elif str(csvData['Genre'][i]) == 'Sports and Games':
        genreValue=45
    elif str(csvData['Genre'][i]) == 'Suspense':
        genreValue=46
    elif str(csvData['Genre'][i]) == 'Thriller':
        genreValue=47
    elif str(csvData['Genre'][i]) == 'War':
        genreValue=48
    elif str(csvData['Genre'][i]) == 'Western':
        genreValue=49
    elif str(csvData['Genre'][i]) == 'Young Adult':
        genreValue=50
    elif str(csvData['Genre'][i]) == '-':
        genreValue=0
    genreValueList.append(genreValue) 
    i+=1


#For adding the new  Genre value column to the csv    
csvData["Genre_Value"] = genreValueList

########For finding the length of the reviews
ReviewList=[] 
i=0
for r in csvData['Review']:
    ReviewList.append(len(str(r)))
csvData["Length_Of_Review"] = ReviewList

#For converting the dataframe to csv
csvData.to_csv('intermediate2.csv', sheet_name='sheet1', index=False)

#For making the date format uniform
import re
import csv
f1 = file('intermediate2.csv', 'r')
c1 = csv.reader(f1)
masterlist = list(c1)
datetime1=[]
for c in masterlist:    
    if ',' not in c[5]:      
        c2=c[5]
        c3=re.sub('20','01,20',c2)
        c4=re.sub('19','01,19',c3)
    else:
        c4=c[5].strip()
    c5=re.sub(' +','',c4)
    datetime1.append(c5)
    
#For removing the first row which was the heading
datetime1.pop(0)

csvData1=pd.read_csv("intermediate2.csv")

#For adding the new  book read date column to the csv
csvData1["Book_Read_Date"] = datetime1

#For converting the dataframe to csv
csvData1.to_csv('intermediate3.csv', sheet_name='sheet1', index=False)


########################sort according to genre and date read.#################
df=pd.read_csv('intermediate3.csv')
df['Book_Read_Date'] = pd.to_datetime(df['Book_Read_Date'],format="%b%d,%Y") 
df = df.sort_values(['Genre','Book_Read_Date'], ascending=True)

df.to_csv('intermediate4.csv', index=False)


###########For converting Reviewer Rating from string to number
reviewerRatingList=[]

csvData2=pd.read_csv("intermediate4.csv")

i=0
value=0
while i < len(csvData2):
    if str(csvData2['Reviewer Rating'][i]) == 'it was amazing':
        value=3
    elif str(csvData2['Reviewer Rating'][i]) == 'really liked it':
        value=3
    elif str(csvData2['Reviewer Rating'][i]) == 'liked it':
        value=2
    elif str(csvData2['Reviewer Rating'][i]) == 'it was ok':
        value=1
    elif str(csvData2['Reviewer Rating'][i]) == 'did not like it':
        value=1
    elif str(csvData2['Reviewer Rating'][i]) == '-':
        value=0
    reviewerRatingList.append(value) 
    i+=1
len(reviewerRatingList)
    
#For adding the new  Reviewer Ratings column to the csv    
csvData2["Reviewer_Ratings"] = reviewerRatingList

#For converting the dataframe to csv
csvData2.to_csv('intermediate5.csv', sheet_name='sheet1', index=False)    


###########For Finding past ratings of the reviewers for that genre

csvData3=pd.read_csv("intermediate5.csv")

#Finding the past count of that genre as per the date
csvData3["Past_Count_Genre"]=" "
csvData3['Past_Count_Genre'][0]=0
li=list(csvData3['Genre'].unique())
#print li

for i in range(0,len(li)):
    count=-1
    for j in range(0,len(csvData3)):
        if li[i]==csvData3.Genre[j]:
                csvData3.Past_Count_Genre[j]=count=count+1

#For converting the dataframe to csv   
csvData3.to_csv('intermediate6.csv', sheet_name='sheet1', index=False) 


#Finding the past rating for that genre
csvData4=pd.read_csv("intermediate6.csv")

pastRatingList=[]

l=0

while l < len(csvData4):
    if int(csvData4['Past_Count_Genre'][l]) == 0:
        pastRating=0
        #print pastRating
    else:
        pastCount = csvData4['Past_Count_Genre'][l]
        #print 'Past Count'
        #print pastCount
        currentGenre = csvData4['Genre'][l]
        #print 'current Genre'
        #print currentGenre
        pastRatingSum=0
        m=0
        while m < len(csvData4):
            if csvData4['Past_Count_Genre'][m] < pastCount and currentGenre == csvData4['Genre'][m]:
                pastRatingSum = int(pastRatingSum) + int(csvData4['Reviewer_Ratings'][m])
                #print 'pastRatingSum'
                #print pastRatingSum
            m+=1
        pastRating1 = int(pastRatingSum) / float(pastCount)
        pastRating = round(pastRating1,2)
        #print 'pastRating'
        #print pastRating
    pastRatingList.append(pastRating)
    l+=1

csvData4["Past_Rating_Genre"] = pastRatingList
      
#For converting the dataframe to csv 
csvData4.to_csv('intermediate7.csv', sheet_name='sheet1', index=False)



###########For Finding book title length of the books

csvData5=pd.read_csv("intermediate7.csv")

bookCountList=[] 
i=0
for b in csvData5['Book']:
    bookCountList.append(len(b))
csvData5["Book_Length"] = bookCountList

#For converting the dataframe to csv
csvData5.to_csv('intermediate8.csv', sheet_name='sheet1', index=False)



##########For finding the average rating of the reviewers for the past books of an author

csvData6=pd.read_csv("intermediate8.csv")

#Finding the past count of the books reviewed for that author as per the date
csvData6["Past_Author_Book_Count"]=" "
csvData6['Past_Author_Book_Count'][0]=0
li=list(csvData6['Author'].unique())
#print li

for i in range(0,len(li)):
    count=-1
    for j in range(0,len(csvData6)):
        if li[i]==csvData6.Author[j]:
                csvData6.Past_Author_Book_Count[j]=count=count+1

#For converting the dataframe to csv   
csvData6.to_csv('intermediate9.csv', sheet_name='sheet1', index=False) 


#Finding the past rating for that author's books

csvData7=pd.read_csv("intermediate9.csv")

pastAuthorBookRatingList=[]

l=0

while l < len(csvData7):
    if int(csvData7['Past_Author_Book_Count'][l]) == 0:
        pastRating=0
        #print pastRating
    else:
        pastCount = csvData7['Past_Author_Book_Count'][l]
        #print 'Past Count'
        #print pastCount
        currentAuthor = csvData7['Author'][l]
        #print 'current Genre'
        #print currentGenre
        pastRatingSum=0
        m=0
        while m < len(csvData7):
            if csvData7['Past_Author_Book_Count'][m] < pastCount and currentAuthor == csvData7['Author'][m]:
                pastRatingSum = int(pastRatingSum) + int(csvData7['Reviewer_Ratings'][m])
                #print 'pastRatingSum'
                #print pastRatingSum
            m+=1
        pastRating1 = int(pastRatingSum) / float(pastCount)
        pastRating = round(pastRating1,2)
        #print 'pastRating'
        #print pastRating
    pastAuthorBookRatingList.append(pastRating)
    l+=1

len(pastAuthorBookRatingList)
csvData7["Past_Author_Book_Rating"] = pastAuthorBookRatingList
      
#For converting the dataframe to csv 
csvData7.to_csv('intermediate10.csv', sheet_name='sheet1', index=False)


#Filtering out reviews that have Reviewer Rating = 0

csvData8=pd.read_csv("intermediate10.csv")
    
csvData9 = csvData8[(csvData8['Reviewer_Ratings'] != 0) ]

#For converting the dataframe to csv
csvData9.to_csv('intermediate11.csv', sheet_name='sheet1', index=False)


csvData10=pd.read_csv("intermediate11.csv")

#Dropping the columns that are not going to be used for the prediction

#For removing the old book read date column from the csv
csvData10.drop('Book read date', axis=1, inplace=True)

#Removing the newly created Book_Read_Date column as it was an intermediate feature that was required to obtain other features
csvData10.drop('Book_Read_Date', axis=1, inplace=True)

#Removing the columns that will not be used in our prediction
csvData10.drop('Count of people interaction', axis=1, inplace=True)
csvData10.drop('Author', axis=1, inplace=True)
csvData10.drop('Average book Rating', axis=1, inplace=True)
csvData10.drop('Book', axis=1, inplace=True)
csvData10.drop('Book published date', axis=1, inplace=True)
csvData10.drop('Book added date', axis=1, inplace=True)
csvData10.drop('ISBN', axis=1, inplace=True)
csvData10.drop('Reviewer Name', axis=1, inplace=True)
csvData10.drop('Review', axis=1, inplace=True)
csvData10.drop('Length_Of_Review', axis=1, inplace=True)

#Removing the old Reviewer Rating column from the csv as we will be using the new numeric column for our prediction
csvData10.drop('Reviewer Rating', axis=1, inplace=True)

#Removing the Genre column as it was required only to create new genre columns having 1/0 values
csvData10.drop('Genre', axis=1, inplace=True)

#Removing the Genre_Value column as it was created only for the purpose of plotting and not for making a prediction
csvData10.drop('Genre_Value', axis=1, inplace=True)

#For converting the dataframe to csv. This is the final csv that will be used for making the prediction
csvData10.to_csv('feature.csv', sheet_name='sheet1', index=False)




