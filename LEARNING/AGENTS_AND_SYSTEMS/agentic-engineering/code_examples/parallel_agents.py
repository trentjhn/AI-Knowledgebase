# parallel_agents.py
import time
import concurrent.futures

class DataCollectionAgent:
    def __init__(self, name="Collector"):
        self.name = name

    def collect_data(self, topic: str) -> str:
        print(f"[{self.name}] Starting data collection for '{topic}'...")
        time.sleep(2) # Simulate long-running task
        data = f"[{self.name}] Collected data points for '{topic}' (e.g., 100 entries)."
        print(f"[{self.name}] Finished data collection for '{topic}'.")
        return data

class AnalysisAgent:
    def __init__(self, name="Analyzer"):
        self.name = name

    def analyze_data(self, data: str) -> str:
        print(f"[{self.name}] Starting analysis of: '{data}'...")
        time.sleep(1.5) # Simulate work
        analysis_result = f"[{self.name}] Analysis complete: Trends identified from '{data}'."
        print(f"[{self.name}] Finished analysis.")
        return analysis_result

def run_parallel_workflow(topics: list[str]):
    print("\n--- Running Parallel Agent Workflow ---")
    collector1 = DataCollectionAgent("Collector_A")
    collector2 = DataCollectionAgent("Collector_B")
    analyzer = AnalysisAgent()

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit collection tasks in parallel
        future1 = executor.submit(collector1.collect_data, topics[0])
        future2 = executor.submit(collector2.collect_data, topics[1])

        # Wait for both collection tasks to complete and get results
        data1 = future1.result()
        data2 = future2.result()

        print("\n--- Collection complete, starting parallel analysis ---")
        # Submit analysis tasks in parallel
        future3 = executor.submit(analyzer.analyze_data, data1)
        future4 = executor.submit(analyzer.analyze_data, data2)

        # Wait for analysis tasks to complete
        analysis_result1 = future3.result()
        analysis_result2 = future4.result()

        results.extend([analysis_result1, analysis_result2])

    print(f"\n--- Workflow Complete ---")
    for res in results:
        print(f"Parallel Output: {res}")

if __name__ == "__main__":
    run_parallel_workflow(["Market Trends", "Customer Feedback"])
