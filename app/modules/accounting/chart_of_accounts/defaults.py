DEFAULT_CHART_OF_ACCOUNTS = [
    # Assets
    {
        "account_code": "1000",
        "account_name": "Assets",
        "account_type": "ASSET",
        "parent": None,
    },
    {
        "account_code": "1010",
        "account_name": "Cash",
        "account_type": "ASSET",
        "parent": "Assets",
    },
    {
        "account_code": "1020",
        "account_name": "Bank",
        "account_type": "ASSET",
        "parent": "Assets",
    },
    {
        "account_code": "1100",
        "account_name": "Accounts Receivable",
        "account_type": "ASSET",
        "parent": "Assets",
    },

    # Liabilities
    {
        "account_code": "2000",
        "account_name": "Liabilities",
        "account_type": "LIABILITY",
        "parent": None,
    },
    {
        "account_code": "2100",
        "account_name": "Accounts Payable",
        "account_type": "LIABILITY",
        "parent": "Liabilities",
    },

    # Income
    {
        "account_code": "4000",
        "account_name": "Revenue",
        "account_type": "REVENUE",
        "parent": None,
    },
    {
        "account_code": "4010",
        "account_name": "Sales Revenue",
        "account_type": "REVENUE",
        "parent": "Revenue",
    },

    # Expenses
    {
        "account_code": "5000",
        "account_name": "Expenses",
        "account_type": "EXPENSE",
        "parent": None,
    },
    {
        "account_code": "5010",
        "account_name": "General Expense",
        "account_type": "EXPENSE",
        "parent": "Expenses",
    },
]