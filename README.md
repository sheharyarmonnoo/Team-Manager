# team_manager

## Overview

This code aims to provide a platform for tracking the performance of members in the house on proposed legislations. 
It does this by scraping data from the website 'https://clerk.house.gov/members/ViewRecentVotes'. 

The code has several functionalities that make it possible to track the performance of members, these functionalities include:

- Member tracking: The code allows the user to input the names of members that they want to track, the names are then used to scrape data from the website.

- Performance tracking: The code tracks the performance of members on proposed legislations, this is achieved by scraping data from the website and then analyzing it to determine the performance of members.

- Meetings tracking: The code also has a form input that takes members inputs on meetings, this is useful for keeping track of when and where the members have held meetings.

- Analytics view: The code has an analytics view that displays graphs showing the monthly activity of members. This view provides the user with an insight into the performance of members over time.


## Implementation
The code uses several libraries to implement its functionalities, some important libraries include:

Streamlit: This library is used for building the web application, it provides the necessary tools for building a user-friendly interface and fast web deployment.

Plotly: This library is used for creating interactive visualizations, it provides several visualizations that can be used to display the data scraped from the website.

Aggrid: This library is used for displaying the data in a grid format, it provides a grid component that can be used to display data in an organized and easy-to-read manner.
