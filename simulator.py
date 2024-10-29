import json
from agent.state import *
from agent.task import Task


class Simulator:
    def __init__(self):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def run(self):
        os.makedirs('output', exist_ok=True)
        output_path = os.path.join('output', 'output.json')

        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as file:
                results = json.load(file)
        else:
            results = {}

        for user_id in self.data:
            results.setdefault(user_id, {})

            for task_id in self.data[user_id]:
                if user_id in results and task_id in results[user_id]:
                    continue

                task = Task(task_id=task_id, real_task=self.data[user_id][task_id])
                results[user_id][task_id] = task.run()

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()
