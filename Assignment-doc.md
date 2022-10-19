**Data Visualisation 4 Assignment 1 2022-2023**

This counts for 20% 

**Submission Date:** Wednesday, 16th of November 

**Sumission Format:** PDF and Python Source code 

**Assignment Description**

Scrape Car Information from "www.carzone.ie/search" using Python3 with Beautifulsoup. 

**Simple Information Retrival** (20%)

* Syntheses URLs to download the first 50 pages
* Retrieve the webpages based on these URLs and convert each into a beautifulsoup object
*  Retrieve Car Manufacturing Year, Engine, Price, Dealer information (if it is available), and the URL (href) to access the detailed car information.
* Save the information into a csv file

**Further Information Retrival** (20%)

* Retrive the webpages for each car using the URL (href) from the simple retrival
* Retrive the Price, Engine Type, Body Type, Manual/Auto, Mileage, Colour, Door Number, Manufacturing Year, Phone Number, Car Brand and Model (hint: have a look at the car's URL). 
* Save the information into a csv file

**Load, Analyse and Visualise Data using Pandas** (30%)

* Load the csv file into a dataframe using Pandas
* Create a new dataframe that only contains Year and Price Columns
* Draw a Scatter Chart for Year verses Price
* Use `df.groupby` function to group new dataframe according to year information
* Calculate the average car price per year
* Draw a Bar Chart to show the relationship between Year and Average Price
* (Extra 2%) Draw a box chart for for Year verses Price

**Scatter Facet** (25%)

* Create a new dataframe that contains Manufacturing Year, Car Price, Engine Type, Manufacturer, Door Numbers, Mileage Columns.
* Create a Scatter Facet (a matrix of scatter subplots, using plotly.px or plotly.go) to show the relationship between Year verse Average Price for different auto/manual gearbox (the Horizontal Direction of Matrix), different Manufacturers (the Vertical Direction of Matrix), different Door Numbers (Colour) and use mileage to change the scatter marker size .
* Use `df.pivot_table` function to aggregate the average price for the cars of different Engine Types, different Manufacturers, different Door Numbers, and different Year info. Then calculate the average price for each group and then draw a Line Facet plot (using plotly.px). It should include Door Number (the Horizontal Direction of Matrix), Manufacturer (the Vertical Direction of Matrix),  Engine Type (Colour) to show the trend of the average prices over different years.
* (Extra 1%) Compare the difference between `groupby` and `pivot_table`, and demonstrate you understand it. 
* (Extra 5%) Draw a Pie Facet using plotly.go. NOTE: plotly.ex will not work. To show the number of cars of different years (different colours/proportions in the pie chart), different Engine Types (the Horizontal Direction of Matrix), different Manufacturers (the Vertical Direction of Matrix). 

**Geo-location Visualisation** (5%)

* Change the scraping code to add the county information to your csv file 
* Using plotly.px.choropleth to create a geolocation chart to show the average car price in different counties, versus different years. 
* (Extra 2%) Be creative.

