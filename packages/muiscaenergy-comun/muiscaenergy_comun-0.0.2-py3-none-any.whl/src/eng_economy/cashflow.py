import pandas as pd


class CashFlowMeasures:
    """
    A class for performing cash flow measures.

    :param eco_lifetime: The economic lifetime of the project.
    :param interest_rate: The interest rate.
    :param compounding: The compounding frequency.
    Valid values are 'Y' for yearly, 'Q' for quarterly, 'M' for monthly, and 'D' for daily.

    Example: CashFlowMeasures(eco_lifetime=20, interest_rate=5, compounding='Y')
    get_capital_recovery_factor() returns 0.0945.
    """

    def __init__(self, eco_lifetime: int,
                 interest_rate: float,
                 compounding: str = 'Y'):
        self.eco_lifetime = eco_lifetime
        self.interest_rate = interest_rate / 100
        self.compounding = compounding

    def get_capital_recovery_factor(self):
        """
        Calculate the capital recovery factor.
        Example: CashFlowMeasures(eco_lifetime=20, interest_rate=5, compounding='Y')
        get_capital_recovery_factor() returns 0.0945.
        """
        n = self.eco_lifetime
        r = self.interest_rate
        c = self.compounding

        if c == 'Q':
            n *= 4
            r /= 4
        if c == 'M':
            n *= 12
            r /= 12
        if c == 'D':
            n *= 365
            r /= 365

        crf = (r * (1 + r) ** n) / ((1 + r) ** n - 1)

        return crf
