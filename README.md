In the file - Collecting Job data using API. ipynb
1. To get the no of astrnauts in ISS and names of astronauts in the ISS using API URL
2. To get the numnber of jobs with respect to technology, language and Location using API URL and saved in XLS file

   In the web scraping Review lab.ipynb
1. Download a webpage using requests module
2. Scrape all links from a webpage
3. Scrape all image URLs from a web page
4. Scrape data from html tables
 using Scrape www.ibm.com
 lab v2.ipynb
In the web scraping lab using web scraping.ipynb
data scraped is the name of the programming language and average annual salary from a given url

In the Explore data set
we've completed in this file:

Installed and Imported Libraries: We started by ensuring the pandas library, essential for data manipulation, was installed using !pip install pandas, and then imported it into our environment as pd.

Loaded the Dataset: We loaded a survey dataset from a specified URL (https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/VYPrOu0Vs3I0hKLLjiPGrA/survey-data-with-duplicate.csv) into a pandas DataFrame named df. This is our primary data structure for analysis.

Explored Dataset Head: To get a quick overview and understand the structure of the data, we displayed the first 5 rows of the DataFrame using display(df.head()).

Identified Data Dimensions: We determined the size of our dataset by printing:

The number of rows, which is 65457, indicating the total number of survey responses.
The number of columns, which is 114, representing the various questions or attributes collected in the survey.
Identified Column Data Types: We used df.dtypes to inspect the data type of each of the 114 columns. This step is crucial for understanding how data is stored (e.g., int64 for integers, object for strings, float64 for floating-point numbers) and helps in planning further analysis or necessary data type conversions.

Calculated Mean Age of Participants: This task required a bit more manipulation:

The 'Age' column initially contained categorical string values (e.g., 'Under 18 years old', '25-34 years old', 'Prefer not to say').
To calculate a numerical mean, we created an age_mapping dictionary. This dictionary assigned a representative numerical midpoint to each age range (e.g., '18-24 years old' was mapped to 21, '35-44 years old' to 39.5, etc.).
Entries like 'Prefer not to say' were mapped to None, which pandas automatically treats as NaN (Not a Number), effectively excluding them from the mean calculation.
A new column, Age_numeric, was created in the DataFrame using this mapping.
Finally, we calculated and printed the mean of this Age_numeric column, which came out to be approximately 32.91 years.
Counted Unique Countries: We found out how many distinct countries participated in the survey by using df['Country'].nunique(). The result showed that the survey collected responses from 185 unique countries.

These steps collectively provided a foundational understanding of the dataset's structure, content, and some key demographics.

