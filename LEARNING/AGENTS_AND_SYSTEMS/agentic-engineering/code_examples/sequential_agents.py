# sequential_agents.py
import time

class PlanningAgent:
    def __init__(self, name="Planner"):
        self.name = name

    def plan_task(self, query: str) -> str:
        print(f"[{self.name}] Receiving query: '{query}'")
        time.sleep(0.5) # Simulate work
        plan = f"Detailed plan for: '{query}'. First, research '{query} basics'. Second, analyze '{query} implications'."
        print(f"[{self.name}] Generated plan: '{plan}'")
        return plan

class ResearchAgent:
    def __init__(self, name="Researcher"):
        self.name = name

    def conduct_research(self, plan: str) -> str:
        print(f"[{self.name}] Receiving plan: '{plan}'")
        time.sleep(1) # Simulate work
        research_summary = f"Research results for: '{plan.split('First, ')[1].split('.')[0]}'. Key findings: initial data collected."
        print(f"[{self.name}] Research summary: '{research_summary}'")
        return research_summary

class ReportAgent:
    def __init__(self, name="Reporter"):
        self.name = name

    def generate_report(self, research_summary: str) -> str:
        print(f"[{self.name}] Receiving research summary: '{research_summary}'")
        time.sleep(0.7) # Simulate work
        final_report = f"Final report based on: '{research_summary}'. Conclusion: Actionable insights derived."
        print(f"[{self.name}] Final report: '{final_report}'")
        return final_report

def run_sequential_workflow(query: str):
    print("\n--- Running Sequential Agent Workflow ---")
    planner = PlanningAgent()
    researcher = ResearchAgent()
    reporter = ReportAgent()

    # Step 1: Planning
    plan = planner.plan_task(query)

    # Step 2: Research based on plan
    research_summary = researcher.conduct_research(plan)

    # Step 3: Report based on research
    final_report = reporter.generate_report(research_summary)

    print(f"\n--- Workflow Complete ---")
    print(f"Final Output: {final_report}")

if __name__ == "__main__":
    run_sequential_workflow("Impact of AI on software development")
