import csv
from collections import defaultdict
from datetime import datetime
import click
import attr
from calendar import monthrange
from attrs import validators


@attr.s
class Sales:
    sale_amount: float = attr.ib()
    sale_date: datetime = attr.ib()


@attr.s
class AvgSales:
    date: datetime = attr.ib()
    days_in_month: int = attr.ib()
    valid_days: int = attr.ib()
    total_sales: float = attr.ib(validator=validators.instance_of(float))
    avg_sales_per_day: float = attr.ib(validator=validators.instance_of(float))


def csv_reader(input_csv):
    results = []
    reader = csv.DictReader(input_csv)
    for row in reader:
        try:
            # Check if there is a sales value otherwise skip
            if row["sales"]:
                results.append(
                    Sales(
                        sale_amount=float(row["sales"]),
                        sale_date=datetime.strptime(row["date"], "%Y-%m-%d"),
                    )
                )
        except (ValueError, IndexError):
            # Skip over any rows with missing or invalid data
            continue
    return results


def csv_writer(output_csv, output_data):
    output_fields = (
        "date",
        "days_in_month",
        "valid_days",
        "total_sales",
        "avg_sales_per_day",
    )
    output_writer = csv.DictWriter(
        output_csv, fieldnames=output_fields, lineterminator="\n"
    )
    output_writer.writeheader()

    # Write each row of monthly sales data to the output file
    for data in output_data:
        data_dict = attr.asdict(data)
        data_dict = {
            key: value for key, value in data_dict.items() if key in output_fields
        }
        output_writer.writerow(data_dict)


@click.command()
@click.option("--input_sales_csv", type=click.File("r"), default="sales.csv")
@click.option("--output_sales_csv", type=click.File("w"), default="")
def main(input_sales_csv, output_sales_csv):
    input_sales_list = csv_reader(input_csv=input_sales_csv)

    # Initialize a dictionary to store the total sales and number of days for each month
    monthly_sales = defaultdict(
        lambda: {"total_sales": 0, "valid_days": 0, "days_in_month": 0}
    )
    output_data = []
    for data in input_sales_list:
        weekday, total_days = monthrange(data.sale_date.year, data.sale_date.month)
        monthly_sales[data.sale_date.strftime("%Y-%m")][
            "total_sales"
        ] += data.sale_amount
        monthly_sales[data.sale_date.strftime("%Y-%m")]["valid_days"] += 1
        monthly_sales[data.sale_date.strftime("%Y-%m")]["days_in_month"] = total_days

    # Calculate the average sales per day for each month (out of total days in month)
    for month in monthly_sales:
        total_sales = monthly_sales[month]["total_sales"]
        days_in_month = monthly_sales[month]["days_in_month"]
        valid_days = monthly_sales[month]["valid_days"]
        # In case we want to only average by data provided use valid_days instead of days_in_month
        avg_sales_per_day = total_sales / days_in_month
        output_data.append(
            AvgSales(
                date=month,
                days_in_month=days_in_month,
                valid_days=valid_days,
                total_sales=total_sales,
                avg_sales_per_day=avg_sales_per_day,
            )
        )

    csv_writer(output_csv=output_sales_csv, output_data=output_data)
