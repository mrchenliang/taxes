class IncomeCalculator:
    def __init__(self, annual_income, province, pay_periods=26):
        self.annual_income = annual_income
        self.province = province
        self.pay_periods = pay_periods

        # Federal Tax Rates for 2024
        self.federal_rates = [
            (0, 15705, 0),
            (15706, 53359, 0.15),
            (53360, 106717, 0.205),
            (106718, 170624, 0.26),
            (170625, 244791, 0.29),
            (244792, float('inf'), 0.33)
        ]

        # Provincial Tax Rates for 2024
        self.provincial_rates = {
            'ON': [
                (0, 12399, 0),
                (12400, 51446, 0.0505),
                (51447, 102894, 0.0915),
                (102895, 150000, 0.1116),
                (150001, 220000, 0.1216),
                (220001, float('inf'), 0.1316)
            ],
            'AB': [
                (0, 21885, 0),
                (21886, 148269, 0.1),
                (148270, 177922, 0.12),
                (177923, 237230, 0.13),
                (237231, 355845, 0.14),
                (355846, float('inf'), 0.15)
            ],
            'BC': [
                (0, 12580, 0),
                (12581, 47937, 0.0506),
                (47938, 95875, 0.077),
                (95876, 110076, 0.105),
                (110077, 133664, 0.1229),
                (133665, 181232, 0.147),
                (181233, 252752, 0.168),
                (252753, float('inf'), 0.205)
            ],
        }
    
        # CPP and EI rates and maximums for 2024
        self.cpp_rate = 0.0595  # Employee contribution rate
        self.cpp_max_premium = 3867.50  # Maximum annual employee contribution
        self.ei_rate = 0.0166  # Employee premium rate
        self.ei_max_premium = 1049.12  # Maximum annual employee premium
    
    def calculate_tax(self, rates, income):
        taxable_income = max(income, 0)
        tax = 0
        for start, end, rate in rates:
            if taxable_income > start:
                # Apply the rate only to the portion of income within the current bracket's range
                if taxable_income <= end:
                    tax += (taxable_income - start) * rate
                    break  # No further brackets apply since taxable income is within the current bracket
                else:
                    tax += (end - start) * rate  # Apply rate to the full bracket range
            else:
                break  # Taxable income does not reach this bracket
        return tax
    
    def calculate_cpp_ei(self, income):
        cpp = min(income * self.cpp_rate, self.cpp_max_premium)
        ei = min(income * self.ei_rate, self.ei_max_premium)
        return cpp, ei

    def calculate(self):
        federal_tax = self.calculate_tax(self.federal_rates, self.annual_income)
        provincial_tax = self.calculate_tax(self.provincial_rates[self.province], self.annual_income)
        cpp, ei = self.calculate_cpp_ei(self.annual_income)
        total_tax = federal_tax + provincial_tax + cpp + ei
        net_annual_income = self.annual_income - total_tax
        biweekly_paycheck = net_annual_income / self.pay_periods
        return federal_tax, provincial_tax, cpp, ei, total_tax, net_annual_income, biweekly_paycheck
    
def create_table(annual_income):
    table_data = []
    provinces = ['ON', 'AB', 'BC']

    for province in provinces:
        income_calculator = IncomeCalculator(annual_income, province)
        federal_tax, provincial_tax, cpp, ei, total_tax, net_annual_income, biweekly_paycheck = income_calculator.calculate()
        net_annual_income = annual_income - total_tax
        table_data.append((
            province,
            f"${federal_tax:,.2f}",
            f"${provincial_tax:,.2f}",
            f"${total_tax:,.2f}",
            f"${net_annual_income:,.2f}",
            f"${biweekly_paycheck:.2f}"
        ))

    print("\nBiweekly Paycheck Table for Annual Income: ${:,.2f}".format(annual_income))
    print("-" * 110)
    print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Province", "Federal Tax", "Provincial Tax", "Total Tax", "Net Annual Income", "Biweekly Paycheck"))
    print("-" * 110)
    for province, federal_tax, provincial_tax, total_tax, net_annual_income, biweekly_paycheck in table_data:
        print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format(province, federal_tax, provincial_tax, total_tax, net_annual_income, biweekly_paycheck))
    print("-" * 110)


create_table(200000)