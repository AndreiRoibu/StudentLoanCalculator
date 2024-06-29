#
# Copyright (c) 2024 Andrei Roibu. All rights reserved.
# All rights reserved. Reproduction in whole or part is prohibited without
# the written permission of the copyright owner.
#
# Created by AndreiRoibu on Sat Jun 29 2024
#
# File Description:
#
# This file contains the functions used for the code.


def calculate_monthly_interest(loan_amount, annual_rate):
    """
    Calculate the amount of interest that accrues in a month.
    """
    monthly_interest = loan_amount * (annual_rate / 12)
    return monthly_interest

def update_loan_balance(loan_amount, monthly_payment, interest):
    """
    Update the loan balance for a single month, accounting for payment and interest.
    """
    new_balance = loan_amount + interest - monthly_payment
    if new_balance < 0:
        return 0  # The loan cannot go negative
    return new_balance

def loan_summary(initial_loan_amount, monthly_payment, annual_rate, years=30):
    """
    Generate a monthly breakdown of the loan over a specified period or until the loan is paid off.
    """
    months = years * 12
    total_interest_paid = 0
    current_balance = initial_loan_amount

    for month in range(1, months + 1):
        if current_balance <= 0:
            break  # Stop processing if the loan is fully repaid
        interest = calculate_monthly_interest(current_balance, annual_rate)
        total_interest_paid += interest
        current_balance = update_loan_balance(current_balance, monthly_payment, interest)
        
        # Check if the loan is cleared by forgiveness at the end of the term
        if month == months and current_balance > 0:
            total_interest_paid += current_balance * (annual_rate / 12)  # Add final month's interest if applicable
            current_balance = 0  # Forgive the remaining balance

    months_until_paid = month if current_balance == 0 else months
    return months_until_paid, total_interest_paid

def calculate_investment_growth(initial_amount, monthly_contribution, annual_return_rate, months):
    """
    Calculate the growth of an investment with monthly contributions.
    """
    current_value = initial_amount
    monthly_return_rate = annual_return_rate / 12
    for _ in range(months):
        current_value = current_value * (1 + monthly_return_rate) + monthly_contribution
    return current_value

def loan_and_investment_strategy(initial_loan_amount, annual_loan_rate, monthly_payment,
                                 excess_income, loan_payment_percentage, investment_annual_return, 
                                 starting_investment_value=0, total_years=35):
    """
    Determines the strategy for paying off a student loan and investing in the stock market.
    """
    total_months = total_years * 12
    additional_loan_payment = excess_income * loan_payment_percentage
    monthly_investment = excess_income - additional_loan_payment
    total_interest_paid = 0
    investment_value = starting_investment_value
    total_months_until_paid = 1
    investment_value_at_loan_paid = starting_investment_value

    for month in range(1, total_months + 1):
        if initial_loan_amount > 0:
            # Update loan balance and track interest
            interest = calculate_monthly_interest(initial_loan_amount, annual_loan_rate)
            total_interest_paid += interest
            initial_loan_amount = update_loan_balance(initial_loan_amount, monthly_payment + additional_loan_payment, interest)

            # Check if the loan is cleared by forgiveness at the end of the term
            if month == total_months and initial_loan_amount > 0:
                total_interest_paid += initial_loan_amount * (annual_loan_rate / 12)  # Add final month's interest if applicable
                initial_loan_amount = 0  # Forgive the remaining balance

            total_months_until_paid = month
            investment_value_at_loan_paid = investment_value

        else:
            # Once the loan is paid off, all excess income goes to investment + monthly payment
            monthly_investment = excess_income + monthly_payment

        # Update investment value
        investment_value = calculate_investment_growth(investment_value, monthly_investment, investment_annual_return, 1)

    return {
        "months_until_loan_paid": total_months_until_paid,
        "total_interest_paid": total_interest_paid,
        "investment_value": investment_value,
        "Investment Value at Loan Paid": investment_value_at_loan_paid,
    }

def calculate_annual_return(total_return, years):
    """ Calculate the annual compounded return given total return over a period of years """
    return (1 + total_return) ** (1 / years) - 1

def portfolio_annual_return():
    """ Calculate the annual return of a portfolio given the returns of two funds and their weights """
    # Fund returns over 10 years
    return_fund1 = 0.7852  # 78.52%
    return_fund2 = 0.3836  # 38.36%

    # Portfolio weights
    weight_fund1 = 0.8  # 80%
    weight_fund2 = 0.2  # 20%

    # Number of years over which returns were measured
    years = 10

    # Calculate annual returns for each fund
    annual_return_fund1 = calculate_annual_return(return_fund1, years)
    annual_return_fund2 = calculate_annual_return(return_fund2, years)

    # Calculate the weighted average of these annual returns
    portfolio_return = (annual_return_fund1 * weight_fund1) + (annual_return_fund2 * weight_fund2)

    return portfolio_return

if __name__=='__main__':
    annual_return = portfolio_annual_return()
    print(f"The annual return of the portfolio is: {annual_return * 100:.2f}%")
