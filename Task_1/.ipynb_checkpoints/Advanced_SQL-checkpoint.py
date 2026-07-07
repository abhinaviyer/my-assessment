"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)

NOTE:
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""


def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    qry = """
    SELECT 
    credit.CustomerClass,
    AVG(customers.Income) AS AverageIncome
    FROM 
    customers
    JOIN 
    credit ON customers.CustomerID = credit.CustomerID
    GROUP BY 
    credit.CustomerClass;
    """

    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

   qry = """  
    SELECT 
        CASE 
            WHEN Region = 'EasternCape' THEN 'EC'
            WHEN Region = 'Gauteng' THEN 'GT'
            WHEN Region = 'WesternCape' THEN 'WC'
            WHEN Region = 'KwaZulu-Natal' THEN 'KZN'
            WHEN Region = 'FreeState' THEN 'FS'
            WHEN Region = 'NorthernCape' THEN 'NC'
            WHEN Region = 'Mpumalanga' THEN 'MP'
            WHEN Region = 'Limpopo' THEN 'LP'
            ELSE Region 
        END AS Province,
        COUNT(*) AS RejectedApplications
    FROM 
        customers c
    JOIN 
        loans l ON c.CustomerID = l.CustomerID
    WHERE 
        l.ApprovalStatus = 'Rejected'
    GROUP BY 
        Province;
"""

    return qry


def question_3():
    """
    Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    qry = """ 
    CREATE TABLE financing AS 
    SELECT 
        c.CustomerID,
        c.Income,
        l.LoanAmount,
        l.LoanTerm,
        l.InterestRate,
        l.ApprovalStatus,
        cr.CreditScore
    FROM 
        customers c
    JOIN 
        loans l ON c.CustomerID = l.CustomerID
    JOIN 
        credit cr ON c.CustomerID = cr.CustomerID;
"""

    return qry


# Question 4 and 5 are linked


def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time.
    Null values to be filled with 0.

    Hint: there should be 12x CustomerID = 1.
    """

    qry = """CREATE TABLE timeline AS
WITH base_timeline AS (
    SELECT DISTINCT c.CustomerID, m.MonthName, m.MonthID
    FROM customers c
    CROSS JOIN months m
)
SELECT 
    b.CustomerID,
    b.MonthName,
    COALESCE(COUNT(r.RepaymentID), 0) AS NumberOfRepayments,
    COALESCE(SUM(r.Amount), 0) AS AmountTotal
FROM 
    base_timeline b
LEFT JOIN 
    repayments r ON b.CustomerID = r.CustomerID 
    AND b.MonthID = EXTRACT(MONTH FROM r.RepaymentDate) -- Adjust column name if different
    AND EXTRACT(HOUR FROM r.RepaymentDate) BETWEEN 6 AND 17 -- 6am to 6pm exclusive of 18:00:01
GROUP BY 
    b.CustomerID, b.MonthName, b.MonthID
ORDER BY 
    b.CustomerID, b.MonthID;
    """

    return qry


def question_5():
    """
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """

    qry = """
    SELECT 
    CustomerID,
    
        SUM(CASE WHEN MonthName = 'January' THEN NumberOfRepayments ELSE 0 END)::INT AS JanuaryRepayments,
        SUM(CASE WHEN MonthName = 'January' THEN AmountTotal ELSE 0 END) AS JanuaryTotal,
        
        SUM(CASE WHEN MonthName = 'February' THEN NumberOfRepayments ELSE 0 END)::INT AS FebruaryRepayments,
        SUM(CASE WHEN MonthName = 'February' THEN AmountTotal ELSE 0 END) AS FebruaryTotal,
        
        SUM(CASE WHEN MonthName = 'March' THEN NumberOfRepayments ELSE 0 END)::INT AS MarchRepayments,
        SUM(CASE WHEN MonthName = 'March' THEN AmountTotal ELSE 0 END) AS MarchTotal,
        
        SUM(CASE WHEN MonthName = 'April' THEN NumberOfRepayments ELSE 0 END)::INT AS AprilRepayments,
        SUM(CASE WHEN MonthName = 'April' THEN AmountTotal ELSE 0 END) AS AprilTotal,
        
        SUM(CASE WHEN MonthName = 'May' THEN NumberOfRepayments ELSE 0 END)::INT AS MayRepayments,
        SUM(CASE WHEN MonthName = 'May' THEN AmountTotal ELSE 0 END) AS MayTotal,
        
        SUM(CASE WHEN MonthName = 'June' THEN NumberOfRepayments ELSE 0 END)::INT AS JuneRepayments,
        SUM(CASE WHEN MonthName = 'June' THEN AmountTotal ELSE 0 END) AS JuneTotal,
        
        SUM(CASE WHEN MonthName = 'July' THEN NumberOfRepayments ELSE 0 END)::INT AS JulyRepayments,
        SUM(CASE WHEN MonthName = 'July' THEN AmountTotal ELSE 0 END) AS JulyTotal,
        
        SUM(CASE WHEN MonthName = 'August' THEN NumberOfRepayments ELSE 0 END)::INT AS AugustRepayments,
        SUM(CASE WHEN MonthName = 'August' THEN AmountTotal ELSE 0 END) AS AugustTotal,
        
        SUM(CASE WHEN MonthName = 'September' THEN NumberOfRepayments ELSE 0 END)::INT AS SeptemberRepayments,
        SUM(CASE WHEN MonthName = 'September' THEN AmountTotal ELSE 0 END) AS SeptemberTotal,
        
        SUM(CASE WHEN MonthName = 'October' THEN NumberOfRepayments ELSE 0 END)::INT AS OctoberRepayments,
        SUM(CASE WHEN MonthName = 'October' THEN AmountTotal ELSE 0 END) AS OctoberTotal,
        
        SUM(CASE WHEN MonthName = 'November' THEN NumberOfRepayments ELSE 0 END)::INT AS NovemberRepayments,
        SUM(CASE WHEN MonthName = 'November' THEN AmountTotal ELSE 0 END) AS NovemberTotal,
        
        SUM(CASE WHEN MonthName = 'December' THEN NumberOfRepayments ELSE 0 END)::INT AS DecemberRepayments,
        SUM(CASE WHEN MonthName = 'December' THEN AmountTotal ELSE 0 END) AS DecemberTotal
    FROM 
        timeline
    GROUP BY 
        CustomerID
    ORDER BY 
        CustomerID;
    """

    return qry


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these questions.


def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """

    qry = """CREATE TABLE corrected_customers AS
WITH counted_fleet AS (
    SELECT 
        CustomerID, Age, Gender,
        COUNT(*) OVER(PARTITION BY Gender) AS GroupSize,
        ROW_NUMBER() OVER(PARTITION BY Gender ORDER BY CustomerID) AS RowNum
    FROM customers
)
SELECT 
    CustomerID,
    Age,
    CASE 
        WHEN RowNum = 1 THEN LEAD(Age, GroupSize - 2) OVER(PARTITION BY Gender ORDER BY CustomerID)
        WHEN RowNum = 2 THEN LEAD(Age, GroupSize - 2) OVER(PARTITION BY Gender ORDER BY CustomerID)
        ELSE LAG(Age, 2) OVER(PARTITION BY Gender ORDER BY CustomerID)
    END AS CorrectedAge,
    Gender
FROM 
    counted_fleet;

SELECT * FROM corrected_customers;"""

    return qry


def question_7():
    """
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`
    """

    qry = """____________________"""

    return qry
