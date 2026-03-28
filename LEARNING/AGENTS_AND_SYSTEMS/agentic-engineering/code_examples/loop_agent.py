# loop_agent.py
import time
import random

class OptimizationAgent:
    def __init__(self, name="Optimizer"):
        self.name = name
        self.current_value = 50.0 # Initial value to optimize
        self.target_value = 10.0
        self.tolerance = 2.0

    def get_current_value(self) -> float:
        return self.current_value

    def propose_adjustment(self) -> float:
        # Simulate an LLM proposing an adjustment
        adjustment = random.uniform(-5.0, -1.0) # Always try to reduce the value
        print(f"[{self.name}] Proposing adjustment: {adjustment:.2f}")
        return adjustment

    def apply_adjustment(self, adjustment: float):
        self.current_value += adjustment
        print(f"[{self.name}] Applied adjustment. New value: {self.current_value:.2f}")
        time.sleep(0.5)

    def check_termination_condition(self) -> bool:
        is_close_enough = abs(self.current_value - self.target_value) <= self.tolerance
        print(f"[{self.name}] Current value: {self.current_value:.2f}, Target: {self.target_value:.2f}, Within tolerance ({self.tolerance})? {is_close_enough}")
        return is_close_enough

def run_loop_workflow():
    print("\n--- Running Loop Agent Workflow (Optimization) ---")
    optimizer = OptimizationAgent()

    iteration = 0
    max_iterations = 10

    while not optimizer.check_termination_condition() and iteration < max_iterations:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        adjustment = optimizer.propose_adjustment()
        optimizer.apply_adjustment(adjustment)

    print(f"\n--- Workflow Complete ---")
    if optimizer.check_termination_condition():
        print(f"Optimization successful! Final value: {optimizer.get_current_value():.2f}")
    else:
        print(f"Optimization stopped after {max_iterations} iterations. Final value: {optimizer.get_current_value():.2f}")

if __name__ == "__main__":
    run_loop_workflow()
