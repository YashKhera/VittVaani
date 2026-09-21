import unittest

from app.services.calculator_service import CalculatorService, EMIInput, EMISchedule


class TestEMIFormula(unittest.TestCase):
    """Direct EMI formula checks against known values."""

    def test_known_emi_value(self):
        # P=10,00,000, annual 12%, 120 months -> EMI ≈ ₹14,347.09
        emi = CalculatorService.compute_emi(1000000, 12.0, 120)
        self.assertAlmostEqual(emi, 14347.09, places=2)

    def test_zero_interest_equals_principal_over_tenure(self):
        emi = CalculatorService.compute_emi(100000, 0.0, 20)
        self.assertAlmostEqual(emi, 5000.0, places=2)

    def test_tenure_one_month_is_principal_plus_interest(self):
        principal = 100000
        rate = 12.0
        emi = CalculatorService.compute_emi(principal, rate, 1)
        expected = 100000 * 1.01
        self.assertAlmostEqual(emi, expected, places=2)

    def test_zero_principal_returns_zero(self):
        self.assertEqual(CalculatorService.compute_emi(0, 5.0, 12), 0.0)

    @unittest.expectedFailure
    def test_negative_tenure_raises(self):
        CalculatorService.compute_emi(100000, 5.0, -1)


class TestScheduleBasics(unittest.TestCase):
    def _input(self, **overrides):
        defaults = dict(
            project_cost=500000,
            interest_rate_annual=9.0,
            tenure_months=60,
            coverage_percent=100.0,
            moratorium_months=0,
            subsidy_amount=0.0,
            upfront_payment=0.0,
        )
        defaults.update(overrides)
        return EMIInput(**defaults)

    def test_full_amortization_sum(self):
        sched = CalculatorService.schedule(self._input())
        self.assertAlmostEqual(sched.total_payment, sched.principal + sched.total_interest, places=1)
        self.assertEqual(len(sched.rows), 60)

    def test_last_balance_is_zero(self):
        sched = CalculatorService.schedule(self._input())
        self.assertAlmostEqual(sched.rows[-1].closing_balance, 0.0, places=2)

    def test_emi_constant_except_last_adjustment(self):
        sched = CalculatorService.schedule(self._input())
        first = sched.rows[0].emi
        for row in sched.rows[:-1]:
            self.assertAlmostEqual(row.emi, first, places=2)

    def test_total_interest_equals_row_sum(self):
        sched = CalculatorService.schedule(self._input())
        row_interest = sum(r.interest for r in sched.rows)
        self.assertAlmostEqual(sched.total_interest, row_interest, places=1)

    def test_principal_monotonic_decrease(self):
        sched = CalculatorService.schedule(self._input())
        balances = [r.closing_balance for r in sched.rows]
        for i in range(1, len(balances)):
            self.assertLessEqual(balances[i], balances[i - 1] + 1e-6)


class TestCoverageSubsidy(unittest.TestCase):
    def test_coverage_caps_principal(self):
        data = EMIInput(project_cost=1000000, interest_rate_annual=9.0, tenure_months=36,
                        coverage_percent=50.0)
        self.assertAlmostEqual(data.financed, 500000.0, places=2)

    def test_90_percent_coverage(self):
        data = EMIInput(project_cost=1000000, interest_rate_annual=9.0, tenure_months=36,
                        coverage_percent=90.0)
        self.assertAlmostEqual(data.financed, 900000.0, places=2)

    def test_subsidy_reduces_principal(self):
        data = EMIInput(project_cost=1000000, interest_rate_annual=9.0, tenure_months=36,
                        coverage_percent=100.0, subsidy_amount=200000)
        self.assertAlmostEqual(data.financed, 800000.0, places=2)

    def test_upfront_payment_reduces_principal(self):
        data = EMIInput(project_cost=1000000, interest_rate_annual=9.0, tenure_months=36,
                        coverage_percent=100.0, upfront_payment=250000)
        self.assertAlmostEqual(data.financed, 750000.0, places=2)

    def test_subsidy_and_upfront_combine(self):
        data = EMIInput(project_cost=1000000, interest_rate_annual=9.0, tenure_months=36,
                        coverage_percent=80.0, subsidy_amount=100000, upfront_payment=50000)
        self.assertAlmostEqual(data.financed, 650000.0, places=2)

    def test_coverage_below_subsidy_never_negative(self):
        data = EMIInput(project_cost=100000, interest_rate_annual=9.0, tenure_months=36,
                        coverage_percent=10.0, subsidy_amount=50000)
        self.assertEqual(data.financed, 0.0)


class TestMoratorium(unittest.TestCase):
    def test_moratorium_interest_accrues(self):
        data = EMIInput(project_cost=100000, interest_rate_annual=12.0, tenure_months=12,
                        moratorium_months=6)
        sched = CalculatorService.schedule(data)
        # 100000 * (12/12/100) * 6 = 6000
        self.assertAlmostEqual(sched.moratorium_interest, 6000.0, places=2)

    def test_zero_moratorium_no_interest(self):
        sched = CalculatorService.schedule(
            EMIInput(project_cost=100000, interest_rate_annual=12.0, tenure_months=12)
        )
        self.assertEqual(sched.moratorium_interest, 0.0)

    def test_moratorium_principal_inflated_in_schedule(self):
        data = EMIInput(project_cost=100000, interest_rate_annual=12.0, tenure_months=12,
                        moratorium_months=6)
        sched = CalculatorService.schedule(data)
        self.assertAlmostEqual(sched.principal, 100000.0, places=2)
        # Amortized principal (internal) includes moratorium interest, so EMI is higher.
        no_mora = CalculatorService.schedule(
            EMIInput(project_cost=100000, interest_rate_annual=12.0, tenure_months=12)
        )
        self.assertGreater(sched.emi, no_mora.emi)


class TestValidation(unittest.TestCase):
    def test_invalid_interest_too_high(self):
        with self.assertRaises(ValueError):
            CalculatorService.validate(
                EMIInput(project_cost=1000, interest_rate_annual=101, tenure_months=12)
            )

    def test_invalid_interest_negative(self):
        with self.assertRaises(ValueError):
            CalculatorService.validate(
                EMIInput(project_cost=1000, interest_rate_annual=-1, tenure_months=12)
            )

    def test_invalid_tenure_too_low(self):
        with self.assertRaises(ValueError):
            CalculatorService.validate(
                EMIInput(project_cost=1000, interest_rate_annual=5.0, tenure_months=0)
            )

    def test_invalid_tenure_too_high(self):
        with self.assertRaises(ValueError):
            CalculatorService.validate(
                EMIInput(project_cost=1000, interest_rate_annual=5.0, tenure_months=361)
            )

    def test_invalid_coverage_above_100(self):
        with self.assertRaises(ValueError):
            CalculatorService.validate(
                EMIInput(project_cost=1000, interest_rate_annual=5.0, tenure_months=12,
                         coverage_percent=110)
            )

    def test_valid_bounds_pass(self):
        CalculatorService.validate(
            EMIInput(project_cost=1000, interest_rate_annual=5.0, tenure_months=12,
                     coverage_percent=90.0, moratorium_months=12)
        )


class TestScheduleSummaries(unittest.TestCase):
    def _input(self, **overrides):
        defaults = dict(
            project_cost=200000,
            interest_rate_annual=8.0,
            tenure_months=24,
            coverage_percent=100.0,
            moratorium_months=0,
            subsidy_amount=0.0,
            upfront_payment=0.0,
        )
        defaults.update(overrides)
        return EMIInput(**defaults)

    def test_summary_fields_present(self):
        data = self._input()
        sched = CalculatorService.schedule(data)
        summary = CalculatorService.summarize(data, sched)
        self.assertEqual(summary["project_cost"], 200000)
        self.assertEqual(summary["financed_amount"], 200000)
        self.assertEqual(summary["tenure_months"], 24)
        self.assertEqual(summary["interest_rate"], 8.0)
        self.assertEqual(summary["emi"], sched.emi)

    def test_no_effective_rate_note_without_moratorium(self):
        data = self._input()
        sched = CalculatorService.schedule(data)
        summary = CalculatorService.summarize(data, sched)
        self.assertIsNone(summary["effective_rate_note"])

    def test_rate_note_with_moratorium(self):
        data = self._input(moratorium_months=6)
        sched = CalculatorService.schedule(data)
        summary = CalculatorService.summarize(data, sched)
        self.assertIsNotNone(summary["effective_rate_note"])

    def test_short_tenure_higher_emi_than_long_tenure(self):
        short = CalculatorService.schedule(self._input(tenure_months=12))
        long_ = CalculatorService.schedule(self._input(tenure_months=24))
        self.assertGreater(short.emi, long_.emi)

    def test_higher_rate_greater_total_interest(self):
        low = CalculatorService.schedule(self._input(interest_rate_annual=6.0))
        high = CalculatorService.schedule(self._input(interest_rate_annual=12.0))
        self.assertGreater(high.total_interest, low.total_interest)


if __name__ == "__main__":
    unittest.main()