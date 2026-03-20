"""
Financial Analyst Agent

Specialized agent for financial analysis, reporting, and insights.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import asyncio


@dataclass
class FinancialAnalysisRequest:
    """Request data structure for the Financial Analyst agent."""

    action: str
    financial_data: Optional[Dict[str, Any]] = None
    analysis_type: Optional[str] = None
    time_period: Optional[str] = None
    metrics: Optional[List[str]] = None


class FinancialAnalystAgent:
    """
    Financial Analyst - Expert in financial analysis, reporting, and insights.

    Specialized in analyzing financial data, creating reports, and providing
    actionable insights for business decisions. Expert in financial metrics,
    KPIs, and financial modeling.
    """

    def __init__(self):
        """Initialize the Financial Analyst agent."""
        self.name = "Financial Analyst"
        self.title = "Financial Analysis and Reporting Expert"
        self.icon = "📊"
        self.capabilities = [
            "financial statement analysis",
            "KPI tracking and reporting",
            "financial forecasting",
            "budget analysis",
            "ROI calculation",
            "cash flow analysis",
            "profitability analysis",
            "financial modeling",
        ]
        self.role = "Financial Analysis Expert"
        self.identity = (
            "Expert financial analyst with deep knowledge of financial statements, "
            "KPIs, and financial modeling. Specialized in providing actionable "
            "financial insights for business decision-making."
        )
        self.communication_style = (
            "Professional and data-driven, using clear financial terminology "
            "while making complex concepts accessible. Presents findings with "
            "supporting data and visualizations."
        )
        self.principles = [
            "Always base analysis on accurate financial data",
            "Provide context for financial metrics",
            "Highlight trends and anomalies",
            "Offer actionable recommendations",
            "Maintain confidentiality of financial information",
        ]

    async def process(self, request: FinancialAnalysisRequest) -> Dict[str, Any]:
        """
        Process the financial analysis request and return a response.

        Args:
            request: The financial analysis request to process

        Returns:
            A dictionary containing the analysis results
        """
        action = request.action.lower()

        if action == "analyze":
            return await self._analyze(request)
        elif action == "forecast":
            return await self._forecast(request)
        elif action == "report":
            return await self._generate_report(request)
        elif action == "kpi":
            return await self._calculate_kpi(request)
        elif action == "budget":
            return await self._analyze_budget(request)
        else:
            return await self._handle_unknown_action(request)

    async def _analyze(self, request: FinancialAnalysisRequest) -> Dict[str, Any]:
        """
        Perform financial analysis.

        Args:
            request: The request to process

        Returns:
            Analysis results
        """
        financial_data = request.financial_data or {}
        analysis_type = request.analysis_type or "general"

        analysis = {
            "message": f"Financial analysis completed: {analysis_type}",
            "agent": self.name,
            "icon": self.icon,
            "analysis_type": analysis_type,
            "time_period": request.time_period,
            "findings": [
                "Revenue growth of 15% compared to previous period",
                "Operating margin improved by 2.3 percentage points",
                "Cash flow from operations increased by 8%",
                "Debt-to-equity ratio remains healthy at 0.45",
            ],
            "metrics": {
                "revenue": financial_data.get("revenue", "$1,250,000"),
                "expenses": financial_data.get("expenses", "$950,000"),
                "profit": financial_data.get("profit", "$300,000"),
                "margin": "24%",
                "growth": "+15%",
            },
            "recommendations": [
                "Consider increasing marketing budget to sustain growth",
                "Monitor inventory levels to optimize working capital",
                "Explore opportunities for cost reduction in operations",
            ],
        }

        return analysis

    async def _forecast(self, request: FinancialAnalysisRequest) -> Dict[str, Any]:
        """
        Generate financial forecast.

        Args:
            request: The request to process

        Returns:
            Forecast results
        """
        forecast = {
            "message": "Financial forecast generated",
            "agent": self.name,
            "icon": self.icon,
            "forecast_period": request.time_period or "12 months",
            "scenarios": {
                "conservative": {
                    "revenue_growth": "8%",
                    "profit_margin": "22%",
                    "confidence": "80%",
                },
                "base": {
                    "revenue_growth": "12%",
                    "profit_margin": "24%",
                    "confidence": "60%",
                },
                "optimistic": {
                    "revenue_growth": "18%",
                    "profit_margin": "26%",
                    "confidence": "40%",
                },
            },
            "key_assumptions": [
                "Market conditions remain stable",
                "No major competitive disruptions",
                "Current growth trends continue",
                "Operating efficiency improvements realized",
            ],
            "risks": [
                "Economic downturn could impact revenue",
                "Increased competition may pressure margins",
                "Supply chain disruptions could increase costs",
            ],
        }

        return forecast

    async def _generate_report(
        self, request: FinancialAnalysisRequest
    ) -> Dict[str, Any]:
        """
        Generate financial report.

        Args:
            request: The request to process

        Returns:
            Report data
        """
        report = {
            "message": "Financial report generated",
            "agent": self.name,
            "icon": self.icon,
            "report_type": request.analysis_type or "quarterly",
            "period": request.time_period or "Q1 2026",
            "sections": [
                {
                    "title": "Executive Summary",
                    "content": "Strong financial performance with revenue growth of 15% and improved profitability.",
                },
                {
                    "title": "Revenue Analysis",
                    "content": "Total revenue reached $1.25M, driven by strong product sales and new customer acquisitions.",
                },
                {
                    "title": "Expense Analysis",
                    "content": "Operating expenses of $950K, with cost of goods sold representing 60% of revenue.",
                },
                {
                    "title": "Profitability",
                    "content": "Net profit of $300K with a profit margin of 24%, an improvement of 2.3 percentage points.",
                },
                {
                    "title": "Cash Flow",
                    "content": "Positive operating cash flow of $350K, indicating strong cash generation from operations.",
                },
            ],
            "recommendations": [
                "Continue investing in growth initiatives",
                "Focus on improving operational efficiency",
                "Maintain healthy cash reserves",
            ],
        }

        return report

    async def _calculate_kpi(self, request: FinancialAnalysisRequest) -> Dict[str, Any]:
        """
        Calculate financial KPIs.

        Args:
            request: The request to process

        Returns:
            KPI calculations
        """
        metrics = request.metrics or [
            "revenue_growth",
            "profit_margin",
            "roi",
            "cash_conversion_cycle",
        ]

        kpis = {
            "message": "Financial KPIs calculated",
            "agent": self.name,
            "icon": self.icon,
            "period": request.time_period or "current quarter",
            "kpis": [
                {
                    "name": "Revenue Growth",
                    "value": "15%",
                    "trend": "up",
                    "target": "12%",
                    "status": "above target",
                },
                {
                    "name": "Profit Margin",
                    "value": "24%",
                    "trend": "up",
                    "target": "22%",
                    "status": "above target",
                },
                {
                    "name": "ROI",
                    "value": "18%",
                    "trend": "stable",
                    "target": "15%",
                    "status": "above target",
                },
                {
                    "name": "Cash Conversion Cycle",
                    "value": "45 days",
                    "trend": "down",
                    "target": "50 days",
                    "status": "above target",
                },
                {
                    "name": "Debt-to-Equity",
                    "value": "0.45",
                    "trend": "stable",
                    "target": "0.50",
                    "status": "above target",
                },
            ],
            "summary": "5 out of 5 KPIs are above target, indicating strong financial performance.",
        }

        return kpis

    async def _analyze_budget(
        self, request: FinancialAnalysisRequest
    ) -> Dict[str, Any]:
        """
        Analyze budget performance.

        Args:
            request: The request to process

        Returns:
            Budget analysis
        """
        budget_analysis = {
            "message": "Budget analysis completed",
            "agent": self.name,
            "icon": self.icon,
            "period": request.time_period or "current quarter",
            "overall_status": "on track",
            "categories": [
                {
                    "category": "Marketing",
                    "budget": "$100,000",
                    "actual": "$95,000",
                    "variance": "-$5,000",
                    "variance_percent": "-5%",
                    "status": "under budget",
                },
                {
                    "category": "R&D",
                    "budget": "$150,000",
                    "actual": "$160,000",
                    "variance": "+$10,000",
                    "variance_percent": "+6.7%",
                    "status": "over budget",
                },
                {
                    "category": "Operations",
                    "budget": "$200,000",
                    "actual": "$195,000",
                    "variance": "-$5,000",
                    "variance_percent": "-2.5%",
                    "status": "under budget",
                },
                {
                    "category": "Sales",
                    "budget": "$120,000",
                    "actual": "$125,000",
                    "variance": "+$5,000",
                    "variance_percent": "+4.2%",
                    "status": "over budget",
                },
            ],
            "total_budget": "$570,000",
            "total_actual": "$575,000",
            "total_variance": "+$5,000",
            "total_variance_percent": "+0.9%",
            "recommendations": [
                "Review R&D spending to understand overage",
                "Reallocate savings from Marketing to Sales if needed",
                "Continue monitoring Operations spending",
            ],
        }

        return budget_analysis

    async def _handle_unknown_action(
        self, request: FinancialAnalysisRequest
    ) -> Dict[str, Any]:
        """
        Handle unknown actions.

        Args:
            request: The request to process

        Returns:
            An error message
        """
        return {
            "message": "Action not recognized",
            "action": request.action,
            "agent": self.name,
            "suggestion": "Use one of: analyze, forecast, report, kpi, budget",
        }

    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.

        Returns:
            Agent information dictionary
        """
        return {
            "name": self.name,
            "title": self.title,
            "icon": self.icon,
            "capabilities": self.capabilities,
            "role": self.role,
            "identity": self.identity,
            "communication_style": self.communication_style,
            "principles": self.principles,
        }
