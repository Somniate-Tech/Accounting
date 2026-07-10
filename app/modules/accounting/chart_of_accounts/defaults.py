DEFAULT_CHART_OF_ACCOUNTS = [

    # ==========================
    # ASSETS
    # ==========================
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
        "account_code": "1030",
        "account_name": "Petty Cash",
        "account_type": "ASSET",
        "parent": "Assets",
    },
    {
        "account_code": "1100",
        "account_name": "Accounts Receivable",
        "account_type": "ASSET",
        "parent": "Assets",
    },
    {
        "account_code": "1200",
        "account_name": "Inventory",
        "account_type": "ASSET",
        "parent": "Assets",
    },
    {
        "account_code": "1300",
        "account_name": "Input GST",
        "account_type": "ASSET",
        "parent": "Assets",
    },

    # ==========================
    # LIABILITIES
    # ==========================
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
    {
        "account_code": "2200",
        "account_name": "GST Payable",
        "account_type": "LIABILITY",
        "parent": "Liabilities",
    },
    {
        "account_code": "2210",
        "account_name": "CGST Payable",
        "account_type": "LIABILITY",
        "parent": "Liabilities",
    },
    {
        "account_code": "2220",
        "account_name": "SGST Payable",
        "account_type": "LIABILITY",
        "parent": "Liabilities",
    },
    {
        "account_code": "2230",
        "account_name": "IGST Payable",
        "account_type": "LIABILITY",
        "parent": "Liabilities",
    },

    # ==========================
    # EQUITY
    # ==========================
    {
        "account_code": "3000",
        "account_name": "Equity",
        "account_type": "EQUITY",
        "parent": None,
    },
    {
        "account_code": "3010",
        "account_name": "Owner Capital",
        "account_type": "EQUITY",
        "parent": "Equity",
    },
    {
        "account_code": "3020",
        "account_name": "Retained Earnings",
        "account_type": "EQUITY",
        "parent": "Equity",
    },

    # ==========================
    # REVENUE
    # ==========================
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
    {
        "account_code": "4020",
        "account_name": "Service Revenue",
        "account_type": "REVENUE",
        "parent": "Revenue",
    },

    # ==========================
    # EXPENSES
    # ==========================
    {
        "account_code": "5000",
        "account_name": "Expenses",
        "account_type": "EXPENSE",
        "parent": None,
    },
    {
        "account_code": "5010",
        "account_name": "Cost Of Goods Sold",
        "account_type": "EXPENSE",
        "parent": "Expenses",
    },
    {
        "account_code": "5020",
        "account_name": "General Expense",
        "account_type": "EXPENSE",
        "parent": "Expenses",
    },
    {
        "account_code": "5030",
        "account_name": "Purchase Expense",
        "account_type": "EXPENSE",
        "parent": "Expenses",
    },
    {
        "account_code": "5040",
        "account_name": "Salary Expense",
        "account_type": "EXPENSE",
        "parent": "Expenses",
    },
    {
        "account_code": "5050",
        "account_name": "Rent Expense",
        "account_type": "EXPENSE",
        "parent": "Expenses",
    },
    {
        "account_code": "5060",
        "account_name": "Electricity Expense",
        "account_type": "EXPENSE",
        "parent": "Expenses",
    },
]