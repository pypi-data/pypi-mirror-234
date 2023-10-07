from policyengine_canada.model_api import *


class self_employment_income(Variable):
    value_type = float
    entity = Person
    label = "Self-employment income"
    unit = CAD
    documentation = "Income from gainful employment"
    definition_period = YEAR
    reference = "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/personal-income/self-employment-income-lines-13499-14299-gross-income-lines-13500-14300-net-income.html"
