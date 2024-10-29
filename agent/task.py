from agent.state import *


class Task:
    def __init__(self, **kwargs):
        self.current_state = None
        self.task_id = kwargs.get('task_id')
        self.real_task = kwargs.get('real_task')
        self.generate_task = []

    def get_history_query(self, step):
        history = ''
        action = self.real_task[step]

        if 'thought' in action:
            history += f'[思考] {action["thought"]}\n'
        history += f'[搜索] {action["query"]}\n'
        return history

    def get_history_click(self, step):
        history = ''
        action = self.real_task[step]

        clicked_serp = [item for item in action['SERP'] if item['click'] == 1]
        sorted_serp = sorted(clicked_serp, key=lambda x: int(x['order']))

        if sorted_serp:
            for rank, click in enumerate(sorted_serp):
                history += f'[点击] {click["title"]} {click["snippet"]}\n'
                history += f'[观察] {click["title"]} {click["observation"]}\n'
        else:
            history += f'[无点击]\n'
        return history

    def get_history_gq(self, step):
        history = ''

        for s in range(step):
            history += self.get_history_query(s)
            history += self.get_history_click(s)

        if history == '':
            history = '无搜索历史，本次为首次搜索\n'
        return history

    def get_history_gc(self, step):
        history = ''

        for s in range(step):
            history += self.get_history_query(s)
            history += self.get_history_click(s)

        history += self.get_history_query(step)

        if history == '':
            history = '无搜索历史，本次为首次搜索\n'
        return history

    def get_history_sc(self, step):
        history = ''

        for s in range(step):
            history += self.get_history_query(s)
            history += self.get_history_click(s)

        history += self.get_history_query(step)
        history += self.get_history_click(step)

        if history == '':
            history = '无搜索历史，本次为首次搜索\n'
        return history

    def get_serp(self, step):
        serp_str = ''
        serp = self.real_task[step]["SERP"]
        for rank, s in enumerate(serp):
            serp_str += f"[{rank}] {s['title']} {s['snippet']}\n"
        return serp_str

    def run(self):
        self.current_state = Init(self)
        self.current_state.enter()

        while not isinstance(self.current_state, Finish):
            new_state = self.current_state.exec()
            if new_state:
                self.current_state = new_state
                self.current_state.enter()

        return self.generate_task
