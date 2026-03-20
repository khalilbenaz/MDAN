"""Scenario tests for Financial Analyst agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.packs.fintech.agents.financial_analyst.agent import FinancialAnalyst


def test_financial_statement_analysis():
    """Test financial statement analysis capability."""
    agent = FinancialAnalyst()

    input_data = {
        "task": "Analyze the following financial data",
        "revenue": "5,000,000",
        "cost_of_goods_sold": "3,000,000",
        "operating_expenses": "1,000,000",
        "interest_expense": "100,000",
        "tax_rate": "25%",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "gross_profit" in result.lower() or "gross margin" in result.lower()
    assert "operating_income" in result.lower() or "operating profit" in result.lower()
    assert "net_income" in result.lower() or "net profit" in result.lower()
    print("✓ Financial statement analysis test passed")


def test_ratio_analysis():
    """Test financial ratio analysis capability."""
    agent = FinancialAnalyst()

    input_data = {
        "task": "Calculate and analyze key financial ratios",
        "current_assets": "2,000,000",
        "current_liabilities": "1,000,000",
        "total_assets": "10,000,000",
        "total_liabilities": "4,000,000",
        "net_income": "500,000",
        "revenue": "5,000,000",
        "shareholder_equity": "6,000,000",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "current_ratio" in result.lower() or "liquidity" in result.lower()
    assert "debt_to_equity" in result.lower() or "leverage" in result.lower()
    assert "return_on_equity" in result.lower() or "roe" in result.lower()
    print("✓ Ratio analysis test passed")


def test_investment_analysis():
    """Test investment analysis capability."""
    agent = FinancialAnalyst()

    input_data = {
        "task": "Evaluate investment opportunity",
        "company": "TechCorp Inc.",
        "current_price": "100",
        "target_price": "120",
        "dividend_yield": "2.5%",
        "pe_ratio": "25",
        "industry_pe": "30",
        "growth_rate": "15%",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "valuation" in result.lower() or "price" in result.lower()
    assert (
        "recommendation" in result.lower()
        or "buy" in result.lower()
        or "sell" in result.lower()
        or "hold" in result.lower()
    )
    print("✓ Investment analysis test passed")


def test_budget_forecasting():
    """Test budget forecasting capability."""
    agent = FinancialAnalyst()

    input_data = {
        "task": "Create budget forecast for next year",
        "current_revenue": "10,000,000",
        "growth_rate": "10%",
        "current_expenses": "8,000,000",
        "inflation_rate": "3%",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "forecast" in result.lower() or "projection" in result.lower()
    assert "revenue" in result.lower()
    assert "expenses" in result.lower()
    print("✓ Budget forecasting test passed")


def test_cash_flow_analysis():
    """Test cash flow analysis capability."""
    agent = FinancialAnalyst()

    input_data = {
        "task": "Analyze cash flow statement",
        "operating_cash_flow": "1,500,000",
        "investing_cash_flow": "-500,000",
        "financing_cash_flow": "-200,000",
        "beginning_cash": "500,000",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "cash_flow" in result.lower() or "cash flow" in result.lower()
    assert "free_cash_flow" in result.lower() or "net_cash" in result.lower()
    print("✓ Cash flow analysis test passed")


def test_valuation():
    """Test company valuation capability."""
    agent = FinancialAnalyst()

    input_data = {
        "task": "Value the company using DCF method",
        "free_cash_flow": "1,000,000",
        "growth_rate": "5%",
        "discount_rate": "10%",
        "terminal_growth_rate": "2%",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "valuation" in result.lower() or "value" in result.lower()
    assert "present_value" in result.lower() or "npv" in result.lower()
    print("✓ Valuation test passed")


def test_financial_reporting():
    """Test financial reporting capability."""
    agent = FinancialAnalyst()

    input_data = {
        "task": "Prepare financial summary report",
        "period": "Q4 2025",
        "revenue": "15,000,000",
        "expenses": "12,000,000",
        "net_income": "3,000,000",
        "assets": "50,000,000",
        "liabilities": "20,000,000",
        "equity": "30,000,000",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "summary" in result.lower() or "report" in result.lower()
    assert "revenue" in result.lower()
    assert "profitability" in result.lower() or "income" in result.lower()
    print("✓ Financial reporting test passed")


if __name__ == "__main__":
    print("Running Financial Analyst scenario tests...")
    print()

    test_financial_statement_analysis()
    test_ratio_analysis()
    test_investment_analysis()
    test_budget_forecasting()
    test_cash_flow_analysis()
    test_valuation()
    test_financial_reporting()

    print()
    print("All Financial Analyst tests passed! ✓")
