Team Members:
Shradha Nayak
Ankita Sawant
Vandna Yadav

1) We have scraped the 'Most popular 100 reviewers this week in The United States' page of goodreads and since this list keeps changing every week, the reviewers that you scrape might be different from the reviewers that we have scraped. Also, we have scraped this page, since fetching the data of popular reviewers would mean getting maximum number of reviews.

2) The get_features.py uses web-driver and for fetching the reviews of all the reviewers it takes about a day.

3) Since we have used bucketization and have 3 outcomes possible for our prediction label, we were unable to calculate the R squared and area under the curve which work only for binary outcomes. We had even dropped you a mail regarding the same.

4) There are files intermediate1 to intermediate11.csv that get generated in between while running the get_features.py script. They were generated to ensure that the code is executing correctly. In the end, 'feature.csv' gets created and that file has been included in the final project submission.

5) As per your suggestion, we have dropped the 'Length of review' feature and it will not be used for prediction.