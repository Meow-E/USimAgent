from config.config import *
from agent.agent import Agent
from abc import ABC, abstractmethod
from prompt.task_description import *


class StateBase(ABC):
    def __init__(self, task):
        self.task = task

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exec(self):
        pass

    @staticmethod
    def read_prompt(prompt_type):
        prompt_file = os.path.join(ROOT_PATH, "prompt", f"{prompt_type}.txt")
        assert os.path.exists(prompt_file)

        with open(prompt_file, "r", encoding="utf8") as file:
            prompt = file.read()
        return prompt


class Init(StateBase):
    def __init__(self, task):
        super().__init__(task)

    def enter(self):
        self.task.step = -1

    def exec(self):
        return Search(self.task)


class Search(StateBase):
    def __init__(self, task):
        super().__init__(task)
        self.model = None
        self.prompt_variables = {
            "task_description": task_description[self.task.task_id],
            "history": self.task.get_history_gq(self.task.step).strip(),
        }

    def enter(self):
        self.task.step += 1

    def get_thought(self):
        agent = Agent(prompt=StateBase.read_prompt("thought"), **self.prompt_variables)
        thought = agent.generate()['thought']
        return thought

    def exec(self):
        thought = self.get_thought()

        agent = Agent(prompt=StateBase.read_prompt("query"), thought=thought, **self.prompt_variables)
        query = agent.generate()['query']

        self.task.generate_task.append({
            'step': self.task.step,
            'query': query,
            'thought': thought,
            'real_query': self.task.real_task[self.task.step]['query'],
            'real_thought': self.task.real_task[self.task.step]['thought'],
        })

        return Click(self.task)


class Click(StateBase):
    def __init__(self, task):
        super().__init__(task)
        self.model = None
        self.prompt_variables = {
            "task_description": task_description[self.task.task_id],
            "history": self.task.get_history_gc(self.task.step).strip(),
            "thought": self.task.real_task[self.task.step]["thought"],
            "query": self.task.real_task[self.task.step]["query"],
            "serp": self.task.get_serp(self.task.step).strip(),
        }

    def enter(self):
        pass

    def exec(self):
        agent = Agent(prompt=StateBase.read_prompt("click"), **self.prompt_variables)
        results = agent.generate()

        self.task.generate_task[self.task.step].update({
            'clicks': results['clicks'],
            'real_clicks': [rank for rank, result in enumerate(self.task.real_task[self.task.step]['SERP']) if result['click'] == 1],
        })

        return Stop(self.task)


class Stop(StateBase):
    def __init__(self, task):
        super().__init__(task)
        self.model = None
        self.prompt_variables = {
            "task_description": task_description[self.task.task_id],
            "history": self.task.get_history_sc(self.task.step).strip(),
            "serp": self.task.get_serp(self.task.step).strip(),
        }

    def enter(self):
        pass

    def exec(self):
        agent = Agent(prompt=StateBase.read_prompt("stop"), **self.prompt_variables)
        results = agent.generate()

        self.task.generate_task[self.task.step].update({
            'stop': 1 if '结束会话' in results['action'] else 0,
        })

        if self.task.step + 1 == len(self.task.real_task):
            return Finish(self.task)
        else:
            return Search(self.task)


class Finish(StateBase):
    def __init__(self, task):
        super().__init__(task)

    def enter(self):
        pass

    def exec(self):
        pass
