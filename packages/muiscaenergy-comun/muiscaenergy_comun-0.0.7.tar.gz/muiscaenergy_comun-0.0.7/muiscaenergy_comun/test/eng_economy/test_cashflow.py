import unittest
from muiscaenergy_comun.src.eng_economy.cashflow import CashFlowMeasures


class TestCashFlowMeasures(unittest.TestCase):

    def test_get_capital_recovery_factor_yearly(self):
        cash_flow = CashFlowMeasures(eco_lifetime=20, interest_rate=5, compounding='Y')
        crf = cash_flow.get_capital_recovery_factor()
        self.assertAlmostEqual(crf, 0.08024, places=4)

    def test_get_capital_recovery_factor_quarterly(self):
        cash_flow = CashFlowMeasures(eco_lifetime=20, interest_rate=5, compounding='Q')
        crf = cash_flow.get_capital_recovery_factor()
        self.assertAlmostEqual(crf, 0.01984, places=4)

    def test_get_capital_recovery_factor_monthly(self):
        cash_flow = CashFlowMeasures(eco_lifetime=20, interest_rate=5, compounding='M')
        crf = cash_flow.get_capital_recovery_factor()
        self.assertAlmostEqual(crf, 0.00659, places=4)

    def test_get_capital_recovery_factor_daily(self):
        cash_flow = CashFlowMeasures(eco_lifetime=20, interest_rate=5, compounding='D')
        crf = cash_flow.get_capital_recovery_factor()
        self.assertAlmostEqual(crf, 0.000216, places=4)


if __name__ == '__main__':
    unittest.main()

