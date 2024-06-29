#
# Copyright (c) 2024 Andrei Roibu. All rights reserved.
# All rights reserved. Reproduction in whole or part is prohibited without
# the written permission of the copyright owner.
#
# Created by AndreiRoibu on Sat Jun 29 2024
#
# File Description:
#
# This is the run file.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import os
import argparse
os.makedirs("figures", exist_ok=True)
os.makedirs("reports", exist_ok=True)
from utils import loan_and_investment_strategy
from datetime import datetime

if __name__ == "__main__":
    """ This is the main function of the file.
    """

    print("\n====================================================================\nWe need some financial information to start off with.\n====================================================================\n")
    
    # How much is the UK student loan?
    loan_balance = float(input("\nEnter the total amount of the student loan in GBP: \n"))
    
    # What is the interest rate on the student loan?
    loan_interest_rate = float(input("\nEnter the interest rate on the student loan (as a percentage - eg 7.9): \n")) / 100

    # What is the conversion rate between GBP and CHF?
    conversion_rate_chf_to_gbp = float(input("\nEnter the conversion rate between GBP and CHF (default is 1/1.14 = 0.893575 - this is the SLC value): \n") or 1/1.14)

    # How much is the monthly min repayment?
    min_loan_payment = float(input("\nEnter the minimum loan repayment in CHF: \n"))

    # How much is the monthly savings?
    max_monthly_savings = float(input("\nEnter the monthly savings in CHF: \n"))

    # How many years are we looking at?
    total_years = int(input("\nEnter the total number of years to consider: \n"))

    # What is the starting investment value?
    starting_investment_value = float(input("\nEnter the starting investment value in CHF (default is 0): \n") or 0)

    # Average investment return
    investment_return = float(input("\nEnter the average investment return in percentage (eg 5.43): \n")) / 100

    # Unique identifier for the run (optional)
    unique_identifier = input("\nEnter a unique identifier for this run (optional): \n")

    print('\n====================================================================\n')

    loan_balance_chf = loan_balance / conversion_rate_chf_to_gbp

    # Create a range of payment scenarios
    payment_scenarios = {}
    for percentage in range(0, 105, 5):
        loan_payment_percentage = percentage / 100
        results = loan_and_investment_strategy(initial_loan_amount=loan_balance_chf,
                                               annual_loan_rate=loan_interest_rate,
                                               monthly_payment = min_loan_payment,
                                               excess_income= max_monthly_savings,
                                               loan_payment_percentage = loan_payment_percentage,
                                               investment_annual_return = investment_return,
                                               starting_investment_value = starting_investment_value,
                                               total_years = total_years
                    )
        results["Loan Payment Percentage"] = loan_payment_percentage
        payment_scenarios[percentage] = results

    # Create a DataFrame from the results
    df = pd.DataFrame(payment_scenarios).T
    # shift column 'Loan Payment Percentage' to first position 
    first_column = df.pop('Loan Payment Percentage') 
    # insert column using insert(position,column_name, first_column) function 
    df.insert(0, 'Loan Payment Percentage', first_column) 
    # Rename some of the columns
    df = df.rename(columns={
        "months_until_loan_paid": "Months Until Loan Paid",
        "total_interest_paid": "Total Interest Paid CHF",
        "investment_value": "Final Investment Value CHF"
    })
    # Calculate change vs. 0% scenario
    df["Change (%) in Final Investment Value CHF"] = (df["Final Investment Value CHF"] - df.loc[0, "Final Investment Value CHF"])/df.loc[0, "Final Investment Value CHF"]*100
    # Calculate how much goes in stocks per month, and how much extra would be paid in loan
    df["Monthly Investment CHF"] = max_monthly_savings - df["Loan Payment Percentage"] * max_monthly_savings
    df["Extra Loan Payment CHF"] = df["Loan Payment Percentage"] * max_monthly_savings
    
    # print the dataframe
    print(df)
    
    # Plot the results
    plt.figure(figsize=(15, 8))
    plt.plot(df["Loan Payment Percentage"], df["Final Investment Value CHF"], label="Final Investment Value CHF")
    plt.xlabel("Loan Payment Percentage")
    plt.ylabel("Final Investment Value CHF")
    plt.title("Effect of Additional Loan Payment on Investment Value")
    plt.legend()
    # Adjust plot margins
    plt.subplots_adjust(right=0.7)  # Adjust this value based on your needs to make room for the text

    # Print assumptions to the right of the plot
    plt.text(1.1, 0.5, f"Loan Balance: £{loan_balance:.2f} | CHF{loan_balance_chf:.2f}\nLoan Interest Rate: {loan_interest_rate*100:.2f}%\nStarting Investment Value: CHF{starting_investment_value:.2f}\nInvestment Return: {investment_return*100:.2f}%\nMin Loan Payment: CHF{min_loan_payment:.2f}\nMax Monthly Savings: CHF{max_monthly_savings:.2f}\nTotal Years: {total_years}\nConversion Rate: {conversion_rate_chf_to_gbp:.2f}", 
            horizontalalignment='left',
            verticalalignment='center',
            transform=plt.gca().transAxes)

    # Save the plot with datetime it was created + unique identifier
    plt.savefig(f"figures/loan_strategy_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}_{unique_identifier}.png")

    # Format the DataFrame as a string
    df_string = df.to_string()

    # Create a filename with a timestamp and (optionally) a unique identifier
    filename = f"reports/payment_scenarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_identifier}.txt"

    # Write the string to a text file
    with open(filename, 'w') as file:
        file.write(df_string)

    print(f"Data has been saved to {filename}")
