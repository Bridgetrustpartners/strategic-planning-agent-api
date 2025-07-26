"""
Flask API wrapper for the StrategicPlanningAgent class.

This module exposes a simple web service that allows clients to generate
a strategic plan by sending company details and goals to a REST
endpoint. The API accepts JSON payloads describing the company's
mission, vision, values, targets, SWOT analysis and strategic moves
and returns a structured plan, narrative and service recommendations.

Usage:

    python agent_api.py

The service will listen on the default Flask port (5000) and can be
interacted with using standard HTTP tools (curl, requests, fetch, etc.).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, request
from flask_cors import CORS

# Import the planning agent. Ensure that planning_agent.py is in the
# same directory or installed in your PYTHONPATH.
try:
    from planning_agent import StrategicPlanningAgent
except ImportError as e:
    raise ImportError("Unable to import StrategicPlanningAgent from planning_agent.py. "
                      "Make sure planning_agent.py is available in the same directory.") from e


def create_app() -> Flask:
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)
    # Enable CORS so that browser-based clients on different domains can
    # access the API without running into cross‑origin restrictions.
    CORS(app)

    # Instantiate the planning agent with placeholder values. The actual
    # company-specific data (name, mission, vision, core values and baseline
    # metrics) will be supplied from the JSON payload in each request.
    agent = StrategicPlanningAgent(
        company_name="",
        mission="",
        vision="",
        core_values=[],
        baseline_metrics={},
    )

    @app.route("/generate_plan", methods=["POST"])
    def generate_plan() -> Any:
        """Endpoint to generate a strategic plan.

        Expects a JSON payload with the following structure:

        {
            "company_name": "Acme Corp",
            "mission": "Our mission is ...",
            "vision": "Our vision is ...",
            "core_values": ["innovation", "integrity", ...],
            "targets": {
                "year1": {"revenue": 1000000, "customers": 1000, "margin": 0.2},
                "year2": {...},
                "year3": {...}
            },
            "winning_moves": [
                {
                    "description": "Launch new product",
                    "owner": "CEO",
                    "success_criteria": "Reach $500k in sales",
                    "projected_revenue": 500000,
                    "testing_metrics": "User adoption rate"
                },
                ...
            ],
            "swot": {
                "strengths": ["strong brand", ...],
                "weaknesses": [...],
                "opportunities": [...],
                "threats": [...]
            }
        }

        Returns a JSON response with the plan components.
        """
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json(force=True)
        try:
            # Extract required fields with basic validation.
            company_name: str = data.get("company_name", "Your Company")
            mission: str = data.get("mission", "")
            vision: str = data.get("vision", "")
            core_values: List[str] = data.get("core_values", [])

            # Targets: convert nested dict into list of year-wise dicts
            targets_input: Dict[str, Dict[str, Any]] = data.get("targets", {})
            targets: List[Dict[str, Any]] = []
            for year_key in ["year1", "year2", "year3"]:
                year_data = targets_input.get(year_key, {})
                targets.append({
                    "revenue_target": year_data.get("revenue"),
                    "customer_target": year_data.get("customers"),
                    "margin_target": year_data.get("margin")
                })

            # Winning moves
            winning_moves: List[Dict[str, Any]] = data.get("winning_moves", [])

            # SWOT analysis
            swot = data.get("swot", {})
            strengths = swot.get("strengths", [])
            weaknesses = swot.get("weaknesses", [])
            opportunities = swot.get("opportunities", [])
            threats = swot.get("threats", [])

            # Update agent attributes with current company data
            agent.company_name = company_name
            agent.mission = mission
            agent.vision = vision
            agent.core_values = core_values
            # Use baseline metrics from input if provided, else empty dict
            baseline_metrics = data.get("baseline_metrics", {})
            agent.baseline_metrics = baseline_metrics

            # Build the plan using the agent
            agent.set_targets(targets)
            if winning_moves:
                agent.add_winning_moves(winning_moves)
            if any([strengths, weaknesses, opportunities, threats]):
                agent.add_swot(strengths, weaknesses, opportunities, threats)

            plan = agent.assemble_plan(company_name)

            # Generate narrative
            narrative = agent.generate_narrative(plan)

            return jsonify({
                "plan": plan,
                "narrative": narrative
            })
        except Exception as exc:
            # Catch unexpected exceptions and return an error response
            return jsonify({"error": f"Failed to generate plan: {exc}"}), 500

    return app

# Create the Flask application at module level. This allows
# Gunicorn or other WSGI servers to import the `app` object directly
# (e.g. via ``gunicorn agent_api:app``) without invoking the factory.
app = create_app()


if __name__ == "__main__":
    # Only run the server if this script is executed directly.
    # The global ``app`` defined above is used by WSGI servers like Gunicorn.
    app.run(host="0.0.0.0", port=5000, debug=True)