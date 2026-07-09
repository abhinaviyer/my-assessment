import os

import numpy as np
import pandas as pd

"""
To answer the following questions, make use of datasets: 
    'scheduled_loan_repayments.csv'
    'actual_loan_repayments.csv'
These files are located in the 'data' folder. 

'scheduled_loan_repayments.csv' contains the expected monthly payments for each loan. These values are constant regardless of what is actually paid.
'actual_loan_repayments.csv' contains the actual amount paid to each loan for each month.

All loans have a loan term of 2 years with an annual interest rate of 10%. Repayments are scheduled monthly.
A type 1 default occurs on a loan when any scheduled monthly repayment is not met in full.
A type 2 default occurs on a loan when more than 15% of the expected total payments are unpaid for the year.

Note: Do not round any final answers.

"""


def calculate_df_balances(df_scheduled, df_actual):
    """
    This is a utility function that creates a merged dataframe that will be used in the following questions.
    This function will not be graded, do not make changes to it.

    Args:
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
        df_actual (DataFrame): Dataframe created from the 'actual_loan_repayments.csv' dataset

    Returns:
        DataFrame: A merged Dataframe with additional calculated columns to help with the following questions.

    """

    df_merged = pd.merge(df_actual, df_scheduled)

    def calculate_balance(group):
        r_monthly = 0.1 / 12
        group = group.sort_values("Month")
        balances = []
        interest_payments = []
        loan_start_balances = []
        for index, row in group.iterrows():
            if balances:
                interest_payment = balances[-1] * r_monthly
                balance_with_interest = balances[-1] + interest_payment
            else:
                interest_payment = row["LoanAmount"] * r_monthly
                balance_with_interest = row["LoanAmount"] + interest_payment
                loan_start_balances.append(row["LoanAmount"])

            new_balance = balance_with_interest - row["ActualRepayment"]
            interest_payments.append(interest_payment)

            new_balance = max(0, new_balance)
            balances.append(new_balance)

        loan_start_balances.extend(balances)
        loan_start_balances.pop()
        group["LoanBalanceStart"] = loan_start_balances
        group["LoanBalanceEnd"] = balances
        group["InterestPayment"] = interest_payments
        return group

    df_balances = (
        df_merged.groupby("LoanID", as_index=False)
        .apply(calculate_balance)
        .reset_index(drop=True)
    )

    df_balances["LoanBalanceEnd"] = df_balances["LoanBalanceEnd"].round(2)
    df_balances["InterestPayment"] = df_balances["InterestPayment"].round(2)
    df_balances["LoanBalanceStart"] = df_balances["LoanBalanceStart"].round(2)

    return df_balances


# Do not edit these directories
root = os.getcwd()

if "Task_2" in root:
    df_scheduled = pd.read_csv("data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("data/actual_loan_repayments.csv")
else:
    df_scheduled = pd.read_csv("Task_2/data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("Task_2/data/actual_loan_repayments.csv")

df_balances = calculate_df_balances(df_scheduled, df_actual)



def question_1(df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 1 default definition.

    Args:
        df_balances (DataFrame): Dataframe created from the calculate_df_balances() function

    Returns:
        float: The percentage of type 1 defaulted loans (e.g. 50.0 not 0.5)
    """

    defaulted_loans = 0

    # Loop through each loan
    for loan_id, loan_data in df_balances.groupby("LoanID"):

        # Assume the loan has not been defaulted
        default = False

        # Check every monthly repayment for this loan
        for index, row in loan_data.iterrows():

            # If any repayment is less than the scheduled repayment, the loan is classified as a Type 1 default
            if row["ActualRepayment"] < row["ScheduledRepayment"]:
                default = True
                break

        # Count the loan if it defaulted
        if default:
            defaulted_loans += 1

    # Calculate the percentage of defaulted loans
    total_loans = df_balances["LoanID"].nunique()
    default_rate_percentage = (defaulted_loans / total_loans) * 100

    return default_rate_percentage



def question_2(df_scheduled, df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 2 default definition.

    Type 2 default:
    More than 15% of the expected total payments are unpaid for the year.

    Args:
        df_scheduled (DataFrame): Scheduled loan repayments.
        df_balances (DataFrame): DataFrame created from calculate_df_balances().

    Returns:
        float: Percentage of type 2 defaulted loans.
    """

    # Group all rows by LoanID
    loan_groups = df_balances.groupby("LoanID")

    # Calculate the total scheduled repayment for each loan
    scheduled = loan_groups["ScheduledRepayment"].sum()

    # Calculate the total actual repayment for each loan
    actual = loan_groups["ActualRepayment"].sum()

    # Calculate the percentage of unpaid repayments for each loan
    unpaid = (scheduled - actual) / scheduled

    # Identify loans that have more than 15% unpaid repayments
    defaults = unpaid > 0.15

    # Count the number of defaulted loans
    number_of_defaults = defaults.sum()

    # Count the total number of loans
    total_loans = len(defaults)

    # Calculate the percentage of defaulted loans
    default_rate_percentage = (number_of_defaults / total_loans) * 100

    return default_rate_percentage
    


def question_3(df_balances):
    """
    Calculate the annualized portfolio CPR (as a percentage).

    Args:
        df_balances (DataFrame): DataFrame created from calculate_df_balances().

    Returns:
        float: Annualized CPR of the loan portfolio as a percentage.
    """

    # Calculate the unscheduled principal for each repayment
    df_balances["UnscheduledPrincipal"] = (
        df_balances["ActualRepayment"] - df_balances["ScheduledRepayment"]
    ).clip(lower=0)

    # Group the data by month
    month_groups = df_balances.groupby("Month")

    # Calculate the total unscheduled principal for each month
    total_unscheduled = month_groups["UnscheduledPrincipal"].sum()

    # Calculate the total loan balance at the start of each month
    total_start_balance = month_groups["LoanBalanceStart"].sum()

    # Calculate the Single Monthly Mortality (SMM) for each month
    smm = total_unscheduled / total_start_balance

    # Calculate (1 + SMM) for each month
    factors = 1 + smm

    # Calculate the product of all factors
    product = np.prod(factors)

    # Calculate the geometric mean SMM
    smm_mean = (product ** (1 / len(factors))) - 1

    # Calculate the annual Conditional Prepayment Rate (CPR)
    cpr = 1 - (1 - smm_mean) ** 12

    # Convert to a percentage
    cpr_percent = cpr * 100

    return cpr_percent


def question_4(df_balances):
    """
    Calculate the predicted total loss for the second year in the loan term.

    Uses:
    probability_of_default * total_loan_balance * (1 - recovery_rate)

    The probability of default is taken from Question 2 because
    it identifies loans that have missed more than 15% of their
    total expected repayments, making it a better measure of
    significant credit default.

    Args:
        df_balances (DataFrame): DataFrame created from the
                                 calculate_df_balances() function.

    Returns:
        float: The predicted total loss for the second year.
    """
    # Use the probability of default from Question 2
    probability_of_default = question_2(df_scheduled, df_balances) / 100

    # Find the latest month available in the dataset
    last_month = df_balances["Month"].max()
    # Get the loan balances for that month
    balances = df_balances[df_balances["Month"] == last_month]

    # Calculate the total outstanding loan balance
    total_loan_balance = balances["LoanBalanceStart"].sum()

    # Recovery rate
    recovery_rate = 0.80

    # Calculate predicted loss
    total_loss = probability_of_default * total_loan_balance * (1 - recovery_rate)

    return total_loss