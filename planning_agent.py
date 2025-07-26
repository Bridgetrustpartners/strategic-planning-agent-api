"""
Strategic Planning Agent for Start‑ups
------------------------------------

This module defines a ``StrategicPlanningAgent`` class that helps early‑stage
companies build a structured three‑year strategic plan.  The agent collects
basic information about the business, generates measurable goals using the
SMART framework, assembles a SWOT analysis, proposes winning moves for
revenue and profit, recommends key performance indicators (KPIs), outlines
milestones, and suggests external service providers for legal, marketing,
accounting, HR, payroll and AI support.  It can also produce a strategic
narrative and a high‑level pitch deck outline.

The design draws upon widely accepted strategic planning practices and
recent guidance for small businesses.  For example, strategic plans
typically include an executive summary, clear business goals and
objectives, an industry analysis, a SWOT analysis, marketing
strategies, resource requirements, an organizational plan, a
timeline and budget, and a set of KPIs to measure progress
【920896470864837†L288-L375】.  SMART goals (Specific, Measurable,
Attainable, Relevant and Time‑bound) help ensure targets are clear and
actionable【920896470864837†L340-L347】.  Milestones give business owners a
visual roadmap for when tasks should be completed【920896470864837†L489-L497】.

For revenue and profit growth, companies should identify a handful of
"Winning Moves"—strategic initiatives that can double revenue over
three to five years—then assign owners, set success criteria and
revenue projections, test assumptions and build execution plans
【919335318974169†L248-L310】.  The agent encapsulates this process.

The recommendations for service providers are informed by recent
rankings and expert reviews.  For example, top online legal
platforms like LegalZoom, Firstbase.io and Rocket Lawyer offer
cost‑effective incorporation, compliance and document services
【281454364276471†L133-L215】.  Payroll software such as Gusto and OnPay
automates tax filing and integrates with HR systems【650362062059969†L118-L170】.
Accounting tools like Brex, QuickBooks Online and Xero provide
automated expense management, invoicing and multi‑currency support
【845881733227047†L65-L107】【845881733227047†L182-L211】.  Marketing
platforms such as HubSpot Marketing, Canva and Google Analytics offer
CRM integration, design templates and website insights
【663494913940269†L499-L529】【663494913940269†L565-L576】【663494913940269†L622-L633】.
AI technologies are reshaping HR, improving productivity, and
enabling proactive recruitment and retention: AI tools have boosted
productivity by 63 %, automate 55 % of manual tasks and could save
US$1.2 trillion globally by 2025【179547689127451†L129-L148】.

Example usage::

    from planning_agent import StrategicPlanningAgent
    agent = StrategicPlanningAgent(
        company_name="Acme Widgets", mission="Make building widgets easy", vision="World‑class widgets", core_values=["Integrity", "Innovation", "Customer focus"],
        baseline_metrics={"annual_revenue": 2_000_000, "customers": 200, "gross_margin": 0.3}
    )
    agent.set_targets(
        revenue_targets={2025: 5_000_000, 2026: 7_500_000, 2027: 10_000_000},
        customer_targets={2025: 400, 2026: 600, 2027: 800},
        margin_targets={2025: 0.35, 2026: 0.38, 2027: 0.4},
        other_targets={"net_profit": {2025: 500_000, 2026: 1_000_000, 2027: 1_500_000}}
    )
    agent.identify_winning_moves(
        revenue_moves=["Launch premium widget subscription", "Expand to European market"],
        profit_moves=["Automate manufacturing", "Negotiate bulk material contracts"]
    )
    swot = agent.create_swot(
        strengths=["Strong brand", "Innovative technology"],
        weaknesses=["Limited capital", "Small team"],
        opportunities=["Growing demand for widgets", "Untapped international markets"],
        threats=["New competitors", "Supply chain instability"]
    )
    plan = agent.build_plan()
    narrative = agent.generate_narrative()
    services = agent.recommend_services()

The agent does not connect to external APIs.  All recommendations
should be taken as general guidance and tailored to your specific
business context.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple


def _year_list(start_year: int, years: int = 3) -> List[int]:
    """Generate a consecutive list of years starting from ``start_year``.

    Args:
        start_year: First year in the sequence.
        years: Number of years to include.

    Returns:
        A list of integer years.
    """
    return [start_year + i for i in range(years)]


@dataclass
class StrategicPlanningAgent:
    """Agent that builds a three‑year strategic plan for start‑ups.

    Attributes:
        company_name: Name of the business.
        mission: Mission statement describing the company's purpose.
        vision: Vision statement describing the long‑term aspiration.
        core_values: List of core values guiding the organisation.
        baseline_metrics: Baseline metrics such as current revenue, customers,
            gross margin and any other relevant metrics.  These help establish
            realistic targets.
    """

    company_name: str
    mission: str
    vision: str
    core_values: List[str]
    baseline_metrics: Dict[str, Any]

    revenue_targets: Dict[int, float] = field(default_factory=dict)
    customer_targets: Dict[int, int] = field(default_factory=dict)
    margin_targets: Dict[int, float] = field(default_factory=dict)
    other_targets: Dict[str, Dict[int, float]] = field(default_factory=dict)
    revenue_moves: List[str] = field(default_factory=list)
    profit_moves: List[str] = field(default_factory=list)
    swot: Optional[Dict[str, List[str]]] = None

    start_year: int = field(default_factory=lambda: datetime.datetime.now().year)

    def set_targets(
        self,
        revenue_targets: Dict[int, float],
        customer_targets: Dict[int, int],
        margin_targets: Dict[int, float],
        other_targets: Optional[Dict[str, Dict[int, float]]] = None,
    ) -> None:
        """Define numeric targets for the three‑year plan.

        You should provide a revenue target, customer target and gross margin
        target for each year in the planning horizon.  Additional targets
        (e.g. net profit, EBITDA) can be supplied via ``other_targets``.

        Args:
            revenue_targets: Mapping of year → revenue goal.
            customer_targets: Mapping of year → number of customers.
            margin_targets: Mapping of year → gross margin (as a decimal, e.g. 0.35).
            other_targets: Optional mapping of metric name → year → value.
        """
        self.revenue_targets = revenue_targets
        self.customer_targets = customer_targets
        self.margin_targets = margin_targets
        if other_targets:
            self.other_targets = other_targets

    def identify_winning_moves(self, revenue_moves: List[str], profit_moves: List[str]) -> None:
        """Record strategic initiatives (Winning Moves) to drive revenue and profit.

        According to strategic planning best practice, businesses should limit
        themselves to three to five high‑impact initiatives that can double
        revenue or improve profitability over the next three to five years
        【919335318974169†L248-L310】.  For each move, you should later assign an owner,
        success criteria and revenue projections; however this method only
        stores the descriptions.

        Args:
            revenue_moves: List of initiatives aimed at growing revenue.
            profit_moves: List of initiatives aimed at improving profit margins.
        """
        self.revenue_moves = revenue_moves
        self.profit_moves = profit_moves

    def create_swot(self, strengths: List[str], weaknesses: List[str], opportunities: List[str], threats: List[str]) -> Dict[str, List[str]]:
        """Create a SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis.

        A SWOT analysis summarizes internal strengths and weaknesses and
        external opportunities and threats【920896470864837†L372-L375】.  Conducting a
        SWOT analysis helps translate industry research into actionable
        insights【920896470864837†L361-L375】.  The result is stored on the agent and
        returned for convenience.

        Args:
            strengths: Internal factors that give your company an advantage.
            weaknesses: Internal factors that place the company at a disadvantage.
            opportunities: External factors that the company could exploit.
            threats: External factors that could cause trouble.

        Returns:
            A dictionary with four lists keyed by 'strengths', 'weaknesses',
            'opportunities' and 'threats'.
        """
        self.swot = {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "opportunities": opportunities,
            "threats": threats,
        }
        return self.swot

    def suggest_kpis(self) -> Dict[str, List[str]]:
        """Suggest common key performance indicators (KPIs) for start‑ups.

        KPIs are the data points a business will prioritize to measure progress
        【920896470864837†L499-L508】.  This method proposes KPIs grouped by category
        (financial, customer, marketing, operations and HR).  Use these
        suggestions as a starting point; tailor them to your business model.

        Returns:
            A dictionary keyed by category with lists of KPI names.
        """
        return {
            "financial": [
                "Annual revenue",
                "Gross margin",
                "Net profit",
                "EBITDA",
                "Cash burn rate",
                "Runway (months of operating cash)"
            ],
            "customer": [
                "Number of customers",
                "Customer acquisition cost (CAC)",
                "Customer lifetime value (LTV)",
                "Churn rate",
                "Net promoter score (NPS)"
            ],
            "marketing": [
                "Website traffic",
                "Leads generated",
                "Conversion rate",
                "Cost per lead",
                "Social media engagement"
            ],
            "operations": [
                "Product/service delivery time",
                "Defect/return rate",
                "Operational efficiency (output per employee)",
                "Inventory turnover rate",
                "On‑time project completion percentage"
            ],
            "hr": [
                "Employee retention rate",
                "Employee satisfaction score",
                "Time to hire",
                "Diversity ratio",
                "AI adoption in HR processes"
            ]
        }

    def generate_milestones(self, months_per_milestone: int = 6) -> List[Tuple[datetime.date, str]]:
        """Generate high‑level milestones over the three‑year period.

        A timeline is important because it shows when tasks should be
        completed and in what order【920896470864837†L489-L497】.  This method
        automatically produces semiannual milestones (or another interval
        defined by ``months_per_milestone``) starting from the first month of
        the plan.

        Args:
            months_per_milestone: Number of months between milestones.  The
                default value (6) yields two milestones per year.

        Returns:
            A list of tuples, each containing a date and a descriptive
            milestone label.
        """
        milestones: List[Tuple[datetime.date, str]] = []
        start_date = datetime.date(self.start_year, 1, 1)
        total_months = 36  # three years
        for i in range(0, total_months, months_per_milestone):
            date = start_date + datetime.timedelta(days=30 * i)
            year_offset = (date.year - start_date.year) + 1
            milestone_name = f"Milestone {i // months_per_milestone + 1} – Year {year_offset}"
            milestones.append((date, milestone_name))
        return milestones

    def recommend_services(self) -> Dict[str, Any]:
        """Suggest external service providers for core business functions.

        The recommendations draw from expert articles and rankings.  For legal
        services, online platforms like LegalZoom, Firstbase.io and Rocket
        Lawyer provide cost‑effective incorporation, compliance and document
        support【281454364276471†L133-L215】.  Payroll services such as
        Gusto, Wave Payroll, OnPay and Rippling automate tax filing and
        integrate with HR systems【650362062059969†L118-L170】.  Accounting tools
        like Brex, QuickBooks Online, Xero, Sage Intacct and Wave combine
        automated expense management, invoicing and reporting, and offer
        multi‑currency support【845881733227047†L65-L107】【845881733227047†L182-L211】.
        Marketing platforms like HubSpot Marketing, Canva and Google
        Analytics provide CRM integration, graphic design and website
        insights【663494913940269†L499-L529】【663494913940269†L565-L576】【663494913940269†L622-L633】.  HR tools
        using AI can improve recruitment, engagement and performance, as
        research shows AI boosts productivity, automates routine tasks and
        enables smarter decisions【179547689127451†L129-L149】.

        Returns:
            A dictionary describing recommended providers by category with
            key features.
        """
        return {
            "legal": [
                {
                    "name": "LegalZoom",
                    "features": ["Unlimited legal consultations", "Annual business evaluation", "150+ legal forms"],
                    "notes": "Top overall online legal service for startups, offering incorporation, intellectual property and compliance support"
                },
                {
                    "name": "Firstbase.io",
                    "features": ["Automated compliance reminders", "Registered agent service", "Annual reports and franchise tax filings"],
                    "notes": "Best for startup incorporation and compliance bundles"
                },
                {
                    "name": "Rocket Lawyer",
                    "features": ["On‑call attorneys", "Customizable legal forms", "Document defence"],
                    "notes": "Best for complex legal issues and access to attorneys"
                },
                {
                    "name": "Clerky",
                    "features": ["Variety of fundraising documents", "Pay‑per‑use filing"],
                    "notes": "Best for fundraising and accurate legal paperwork"
                },
            ],
            "payroll": [
                {
                    "name": "Gusto",
                    "features": ["Automatic federal, state and local tax filing", "Unlimited payroll runs", "State new‑hire reporting", "PTO and holiday pay"],
                    "notes": "Full‑service payroll for small businesses" 
                },
                {
                    "name": "Wave Payroll",
                    "features": ["Full service payroll with tax filing in selected states", "Self‑service option for other states", "Integration with Wave accounting"],
                    "notes": "Payroll add‑on to the free Wave accounting platform"
                },
                {
                    "name": "OnPay",
                    "features": ["Digital document storage", "HR compliance tracking", "Integration with QuickBooks and Xero"],
                    "notes": "Best for recordkeeping and HR compliance"
                },
                {
                    "name": "Rippling",
                    "features": ["Automated payroll processing", "Integration with HR, IT and benefits", "500+ third‑party tool integrations"],
                    "notes": "Best for startups wanting seamless payroll and HR integration"
                },
            ],
            "accounting": [
                {
                    "name": "Brex",
                    "features": ["Automatic expense categorization", "Real‑time spend tracking", "Customizable approval workflows", "Detailed financial reporting", "1000+ software integrations"],
                    "notes": "All‑in‑one expense management and accounting platform tailored for startups"
                },
                {
                    "name": "QuickBooks Online",
                    "features": ["Automated bank feeds", "Customizable invoicing", "Expense tracking with receipt capture", "Inventory management", "40+ reporting templates"],
                    "notes": "Industry‑standard cloud accounting solution with extensive integrations"
                },
                {
                    "name": "Xero",
                    "features": ["Bank reconciliation with machine learning", "Customizable invoicing", "Project costing and time tracking", "Inventory tracking", "Multi‑currency support"],
                    "notes": "User‑friendly cloud accounting system with strong international support"
                },
                {
                    "name": "Sage Intacct",
                    "features": ["Revenue recognition automation", "Multi‑entity management", "Customizable reporting", "Project accounting", "AI‑powered timesheets"],
                    "notes": "Best for complex or multi‑entity startups requiring GAAP/IFRS compliance"
                },
                {
                    "name": "Wave Accounting",
                    "features": ["Free double‑entry bookkeeping", "Customizable invoicing", "Receipt scanning", "Basic financial reports", "Multi‑currency support"],
                    "notes": "Best free accounting software for small teams and freelancers"
                },
            ],
            "marketing": [
                {
                    "name": "HubSpot Marketing",
                    "features": ["CRM integration", "Marketing automation", "Email and social media management", "Lead scoring", "Analytics and reporting"],
                    "notes": "Comprehensive platform that combines marketing, sales and service tools"
                },
                {
                    "name": "Canva",
                    "features": ["Drag‑and‑drop design editor", "Templates and stock media", "Logo maker", "Animation and video creation", "Collaboration tools"],
                    "notes": "Easy graphics creation for branding, content and presentations"
                },
                {
                    "name": "Google Analytics",
                    "features": ["Website traffic insights", "Goal and conversion tracking", "Audience segmentation", "Reporting dashboards", "Integration with advertising platforms"],
                    "notes": "Essential tool for understanding website performance and user behaviour"
                },
                {
                    "name": "Mailchimp or Klaviyo",
                    "features": ["Email marketing automation", "Personalized campaigns", "Segmentation and A/B testing", "Analytics", "Ecommerce integrations"],
                    "notes": "Popular platforms for email marketing and customer engagement"
                },
                {
                    "name": "Buffer or Hootsuite",
                    "features": ["Social media scheduling", "Multi‑platform posting", "Engagement tracking", "Analytics", "Team collaboration"],
                    "notes": "Tools to plan and analyse social media content"
                },
            ],
            "hr_ai": [
                {
                    "name": "AI‑powered HR tools",
                    "features": ["Automated candidate screening", "Chatbots for recruiting", "Predictive analytics for flight risks", "Sentiment analysis for engagement", "Personalized learning and development"],
                    "notes": "AI boosts HR productivity and enables proactive talent management; studies report a 63 % productivity boost and 55 % automation of manual tasks【179547689127451†L129-L149】"
                }
            ]
        }

    def build_plan(self) -> Dict[str, Any]:
        """Assemble the strategic plan into a structured dictionary.

        Returns:
            A nested dictionary representing the plan.  The structure
            includes an executive summary, company profile, mission/vision
            statements, core values, strategic targets, winning moves, SWOT
            analysis, milestones, recommended KPIs and services.  This plan
            can be further formatted into a report or presentation as needed.
        """
        years = sorted(set(
            list(self.revenue_targets.keys()) +
            list(self.customer_targets.keys()) +
            list(self.margin_targets.keys())
        ))
        # Build annual targets summary
        targets_summary = []
        for year in years:
            targets_summary.append({
                "year": year,
                "revenue": self.revenue_targets.get(year),
                "customers": self.customer_targets.get(year),
                "gross_margin": self.margin_targets.get(year),
                **{metric: values.get(year) for metric, values in self.other_targets.items()}
            })
        # Compose plan
        return {
            "executive_summary": f"{self.company_name} aims to realise its vision of {self.vision} by executing a three‑year plan built around SMART goals, clear milestones and disciplined measurement.",
            "company_profile": {
                "name": self.company_name,
                "mission": self.mission,
                "vision": self.vision,
                "core_values": self.core_values,
            },
            "baseline_metrics": self.baseline_metrics,
            "strategic_targets": targets_summary,
            "winning_moves": {
                "revenue_moves": self.revenue_moves,
                "profit_moves": self.profit_moves,
            },
            "swot_analysis": self.swot,
            "milestones": [
                {"date": date.isoformat(), "description": name}
                for date, name in self.generate_milestones()
            ],
            "recommended_kpis": self.suggest_kpis(),
            "service_recommendations": self.recommend_services(),
        }

    def generate_narrative(self) -> str:
        """Generate a strategic narrative summarizing the plan.

        The narrative tells the story of where the company is today, where it
        wants to be in three years and how it will get there.  It weaves
        together the mission and vision, highlights key targets and winning
        moves, reflects on the SWOT analysis, and underscores the importance
        of data‑driven execution.

        Returns:
            A multi‑paragraph narrative.
        """
        plan = self.build_plan()
        # Compose narrative sections
        intro = (
            f"{self.company_name} exists to {self.mission}.  Our vision is to {self.vision}. "
            "To achieve this ambition, we have created a three‑year strategic plan grounded in our core values: "
            + ", ".join(self.core_values) + "."
        )
        targets_lines = []
        for t in plan["strategic_targets"]:
            lines = [
                f"In {t['year']}, we aim to generate ${t['revenue']:,.0f} in revenue and serve {t['customers']} customers, achieving a gross margin of {t['gross_margin']*100:.0f}%"
            ]
            for metric, value in t.items():
                if metric not in {"year", "revenue", "customers", "gross_margin"}:
                    lines.append(f"with {metric.replace('_', ' ')} of ${value:,.0f}")
            targets_lines.append(" ".join(lines) + ".")
        targets_paragraph = " ".join(targets_lines)
        moves_paragraph = (
            "To realise these goals, we will pursue a focused set of Winning Moves. "
            "On the revenue side we will: " + "; ".join(self.revenue_moves) + ". "
            "On the profitability side we will: " + "; ".join(self.profit_moves) + "."
        )
        swot_paragraph = (
            "Our SWOT analysis reveals that our strengths—" + ", ".join(self.swot.get("strengths", [])) + 
            "—position us well to capitalise on opportunities such as " + ", ".join(self.swot.get("opportunities", [])) + 
            ".  However, we must mitigate weaknesses like " + ", ".join(self.swot.get("weaknesses", [])) + 
            " and guard against threats such as " + ", ".join(self.swot.get("threats", [])) + "."
        )
        execution_paragraph = (
            "We will execute against clear milestones every six months and monitor key performance indicators across finance, customers, marketing, operations and HR. "
            "Our plan leverages best‑in‑class service providers for legal, accounting, payroll, marketing and AI‑enabled HR to build a strong operational foundation."
        )
        closing = (
            "By aligning our team around this roadmap and measuring our progress relentlessly, "
            f"{self.company_name} will be well positioned to achieve its three‑year objectives and move closer to its long‑term vision."
        )
        return "\n\n".join([intro, targets_paragraph, moves_paragraph, swot_paragraph, execution_paragraph, closing])


if __name__ == "__main__":
    # Example execution for demonstration
    agent = StrategicPlanningAgent(
        company_name="DemoCo",
        mission="simplify home automation for everyday consumers",
        vision="make smart homes accessible worldwide",
        core_values=["Innovation", "Reliability", "Customer focus"],
        baseline_metrics={"annual_revenue": 1_000_000, "customers": 100, "gross_margin": 0.25}
    )
    current_year = datetime.datetime.now().year
    # define targets for next three years
    agent.set_targets(
        revenue_targets={current_year: 2_000_000, current_year + 1: 3_500_000, current_year + 2: 5_000_000},
        customer_targets={current_year: 250, current_year + 1: 400, current_year + 2: 600},
        margin_targets={current_year: 0.30, current_year + 1: 0.35, current_year + 2: 0.40},
        other_targets={"net_profit": {current_year: 200_000, current_year + 1: 500_000, current_year + 2: 1_000_000}}
    )
    agent.identify_winning_moves(
        revenue_moves=["Launch subscription services", "Expand to Europe"],
        profit_moves=["Automate support with AI", "Negotiate supplier contracts"]
    )
    agent.create_swot(
        strengths=["Proprietary technology", "Strong customer service"],
        weaknesses=["Limited brand recognition", "Small marketing budget"],
        opportunities=["Growing smart home market", "Partnerships with telecom providers"],
        threats=["Entrenched competitors", "Supply chain disruptions"]
    )
    plan = agent.build_plan()
    print("Strategic Plan Summary:\n", plan)
    narrative = agent.generate_narrative()
    print("\nStrategic Narrative:\n", narrative)