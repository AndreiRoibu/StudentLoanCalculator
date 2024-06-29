# StudentLoanCalculator
Small project to calculate the payment of my student loan and how it fits in my longterm wealth management.

# To install

First, create a conda environment with the following command:
```bash
conda create --name studentloan
```

Then, activate the environment with the following command:
```bash
conda activate studentloan
```

Finally, install the required packages with the following command:
```bash
conda install --file requirements.txt
```
# To run

To run the program, simply run the following command:
```bash
python run.py
```

This will give you several prompts. Here is an example:
```
====================================================================
We need some financial information to start off with.
====================================================================


Enter the total amount of the student loan in GBP: 
50000

Enter the interest rate on the student loan (as a percentage - eg 7.9): 
8

Enter the conversion rate between GBP and CHF (default is 1/1.14 = 0.893575 - this is the SLC value): 
  

Enter the minimum loan repayment in CHF: 
400

Enter the date when your course finished (YYYY):
2015

Enter the monthly savings in CHF: 
1000

Enter the total number of years to consider: 
35

Enter the starting investment value in CHF (default is 0): 
10000

Enter the average investment return in percentage (eg 5.43): 
5.5

Enter a unique identifier for this run (optional): 
user_baseline
```

This will run the software, which will create a plot of the predicted wealth after the number of total years based on how much money is paid towards the student loan and how much is saved. The plot will be saved in the `figures` folder. 

In addition to this, a report will be created in the `reports` folder. This report will contain the following information:
- Loan Payment Percentage
- Months Until Loan Paid  
- Total Interest Paid CHF  
- Final Investment Value CHF  
- Investment Value at Loan Paid  
- Change (%) in Final Investment Value CHF  
- Monthly Investment CHF  
- Extra Loan Payment CHF