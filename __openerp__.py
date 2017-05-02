{
        "name" : "Account Bank Statement Plaid",
        "version" : "10.0.1",
        "author" : "BachacoVE",
        "website" : "http://www.bachaco.org.ve",
        "category" : "Accounting",
        "description": """ Module for connection to PLAID api""",
        "depends" : ['account_accountant'],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "data" : ['views/bank_plaid_view.xml','data/ir.cron.xml'],
        "installable": True
        #"external_dependencies": {'python': ['plaid']},
}
