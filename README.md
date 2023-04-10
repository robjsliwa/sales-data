**Problem Statement**: Write a Python program that reads in a CSV file containing data for a company and perform following tasks:
- Calculate the total sales for each month.
- Calculate the average sales per day for each month.
- Output results to a new CSV file.

**Input Data**: (sales.csv)

```
date,sales
2022-01-01,100
2022-01-02,200
2022-01-03,300
2022-02-01,150
2022-02-02,
2022-03-01,200
2022-03-02,300
2022-03-03,400
2022-03-04,
```

Note that the sales value is missing for February 2nd and March 4th. Your program should handle this case and skip over any rows with missing data when calculating the total sales and average sales per day.

Submit solution as PR.
