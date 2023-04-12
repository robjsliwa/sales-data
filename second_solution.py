import pandas as pd
import click


@click.command()
@click.option("--input_sales_csv", default="sales.csv")
@click.option("--output_sales_csv", default="second_solution_results.csv")
def main(input_sales_csv, output_sales_csv):
    # Use Pandas to read in the CSV file and create a DataFrame
    df = pd.read_csv(input_sales_csv, dtype={"sales": float})

    # convert date column to datetime type instead of parse_dates to help with non-standard `datetime`
    df["date"] = pd.to_datetime(df["date"])

    # drop any rows with missing sales values, so we don't count those dates when calculating the averages
    df.dropna(subset=["sales"], inplace=True)

    # Remove the day from date, so we only output the year-month in the csv
    date = df["date"].dt.strftime("%Y-%m")

    # Group the sales by month and calculate unique days with sale values, total sales and average sales per day
    # Note using pd.Grouper will cause false positives in output if there are only missing values for a month
    monthly_sales = df.groupby(date).agg(
        valid_days=("date", "nunique"),
        total_sales=("sales", "sum"),
        avg_sales_per_day=("sales", "mean"),
    )

    # Output DataFrame results to a new CSV file with comma-separated values
    monthly_sales.to_csv(output_sales_csv)
