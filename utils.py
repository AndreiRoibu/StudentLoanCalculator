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


def calculate_monthly_interest(loan_amount: float, annual_rate: float) -> float:
    """
    Calculate the amount of interest that accrues in a month.

    Parameters
    ----------
    loan_amount : float
        The initial amount of the loan.
    annual_rate : float
        The annual interest rate as a decimal.

    Returns
    -------
    float
        The amount of interest that accrues in a month.

    """
    monthly_interest = loan_amount * (annual_rate / 12)
    return monthly_interest

def update_loan_balance(loan_amount: float, monthly_payment: float, interest: float) -> float:
    """
    Update the loan balance for a single month, accounting for payment and interest.

    Parameters
    ----------
    loan_amount : float
        The initial amount of the loan.
    monthly_payment : float
        The amount paid toward the loan each month.
    interest : float
        The amount of interest that accrues in a month.

    Returns
    -------
    float
        The remaining balance on the loan after the payment and interest are applied.
    """
    new_balance = loan_amount + interest - monthly_payment
    if new_balance < 0:
        return 0  # The loan cannot go negative
    return new_balance

def loan_summary(initial_loan_amount: float, monthly_payment: float, annual_rate: float, years: int = 30) -> dict:
    """
    Generate a monthly breakdown of the loan over a specified period or until the loan is paid off.

    Parameters
    ----------
    initial_loan_amount : float
        The initial amount of the loan.
    monthly_payment : float
        The amount paid toward the loan each month.
    annual_rate : float
        The annual interest rate as a decimal.
    years : int, optional
        The number of years to generate the summary, by default 30.

    Returns
    -------
    dict
        A dictionary with keys representing months and values representing the remaining balance on the loan.

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

def calculate_investment_growth(initial_amount: float, monthly_contribution: float, annual_return_rate: float, months: int) -> float:
    """
    Calculate the growth of an investment with monthly contributions.

    Parameters
    ----------
    initial_amount : float
        The initial amount of the investment.
    monthly_contribution : float
        The amount contributed to the investment each month.
    annual_return_rate : float
        The annual return rate as a decimal.
    months : int
        The number of months over which the investment grows.

    Returns
    -------
    float
        The value of the investment after the specified number of months.
    """
    current_value = initial_amount
    monthly_return_rate = annual_return_rate / 12
    for _ in range(months):
        current_value = current_value * (1 + monthly_return_rate) + monthly_contribution
    return current_value

def loan_and_investment_strategy(initial_loan_amount: float, annual_loan_rate: float, monthly_payment: float,
                                    excess_income: float, loan_payment_percentage: float, investment_annual_return: float,
                                    starting_investment_value: float = 0, total_years: int = 35, years_until_forgiveness: int =27) -> dict:
    """
    Determines the strategy for paying off a student loan and investing in the stock market.

    Parameters
    ----------
    initial_loan_amount : float
        The initial amount of the loan.
    annual_loan_rate : float
        The annual interest rate on the loan as a decimal.
    monthly_payment : float
        The amount paid toward the loan each month.
    excess_income : float
        The amount of income remaining after paying the loan.
    loan_payment_percentage : float
        The percentage of excess income that goes toward the loan.
    investment_annual_return : float
        The annual return rate on the investment as a decimal.
    starting_investment_value : float, optional
        The initial amount of the investment, by default 0.
    total_years : int, optional
        The total number of years to simulate, by default 35.
    years_until_forgiveness : int, optional
        The number of years until the loan is forgiven, by default 27.
        
    Returns
    -------
    dict
        A dictionary containing the following
        - months_until_loan_paid: The number of months until the loan is paid off.
        - total_interest_paid: The total interest paid on the loan.
        - investment_value: The value of the investment after the loan is paid off.
        - Investment Value at Loan Paid: The value of the investment when the loan is paid off.

    """
    total_months = total_years * 12
    total_months_until_forgiveness = years_until_forgiveness * 12
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
            if month == total_months_until_forgiveness and initial_loan_amount > 0:
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

def calculate_annual_return(total_return: float, years: int) -> float:
    """ Calculate the annual compounded return given total return over a period of years 
    
    Parameters
    ----------
    total_return : float
        The total return over the period.
    years : int
        The number of years over which the return was measured.

    Returns
    -------
    float
        The annual compounded return.
    """
    return (1 + total_return) ** (1 / years) - 1

def portfolio_annual_return():
    """ Calculate the annual return of a portfolio given the returns of two funds and their weights
    
    Parameters
    ----------
    None

    Returns
    -------
    float
        The annual return of the portfolio.
    """

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
