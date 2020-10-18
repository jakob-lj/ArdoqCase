# ArdoqCase

In my case, I wanted to stand out, using more information about the trips than what was available from Oslo bysykkel.

Having that starting point, I was quickly motivated to use Google's Directions api. That would allow me to calculate the shortest path between two bicicle stations. 

Being quite expensive, I didn't want to use all my money on Google API's this weekend, I had to be creative to find a usage for my data. 

Therefor, I had to find a usage where I could compare relative speeds. If I were to compare national health, I could simply have used the avarage duration.

Having that said, I found out I could compare Oslo east vs Oslo west, using relative speeds.

Here's how I did it:

## Fetch data:
Used in order to download the json file with historical data from april 2019.

## getData:
Used to filter trips and add avarage speed to unique trips

## handle data
Making charts

# Reults

![alt trips](https://github.com/jakob-lj/ardoqcase/blob/main/task3/result/trips.png?raw=true)

Having a total of 2193 unique trips started from centrum going out of centrum, started between 16.00(-) to 17.00(-), 975 trips were going in the west direction, while 1218 was eastgoing. 
I do find this enogugh in order to be able to see some differences. 

![alt west](https://github.com/jakob-lj/ardoqcase/blob/main/task3/result/westTrips.png?raw=true)

![alt east](https://github.com/jakob-lj/ardoqcase/blob/main/task3/result/eastTrips.png?raw=true)


However, After removing the fasts and slowest riders, the avarage speed is 3.14 in west and 2.93 in east. Witch is not a significant difference. 

