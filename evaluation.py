import json
import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class Evaluation:
    def __init__(self):
        os.makedirs('evaluation', exist_ok=True)

        with open(os.path.join('output', 'output.json'), 'r', encoding='utf-8') as file:
            self.generate_data = json.load(file)

    def query(self):
        output_path = os.path.join('evaluation', 'query.txt')
        output_str = ''

        text = {
            'p_text': [[], [], [], [], []],
            'q_text': [[], [], [], [], []]
        }

        for user_id in self.generate_data:
            for task_id in self.generate_data[user_id]:
                for action in self.generate_data[user_id][task_id]:
                    text['p_text'][int(task_id) - 1].append(action['real_query'])
                    text['q_text'][int(task_id) - 1].append(action['query'])

        all_bleu_scores = []
        all_bleu_scores2 = []
        smoothie = SmoothingFunction().method1

        for index in range(len(text['p_text'])):
            bleu_scores = []
            for p, q in zip(text['p_text'][index], text['q_text'][index]):

                bleu_score = sentence_bleu([q], p, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothie)
                bleu_scores.append(bleu_score)
                all_bleu_scores2.append(bleu_score)

            output_str += f'Task{index}: Average BLEU: {str(sum(bleu_scores) / len(bleu_scores))}\n'
            all_bleu_scores.append(sum(bleu_scores) / len(bleu_scores))

        output_str += f'All Task: Average BLEU: {str(sum(all_bleu_scores) / len(all_bleu_scores))}\n'
        output_str += f'All Query: Average BLEU: {str(sum(all_bleu_scores2) / len(all_bleu_scores2))}\n'

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(output_str)

    @staticmethod
    def _evaluate(p, q):
        output_str = ''
        accuracy = accuracy_score(p, q)
        precision = precision_score(p, q)
        recall = recall_score(p, q)
        f1 = f1_score(p, q)

        output_str += f'Accuracy:{accuracy}\n'
        output_str += f'Precision:{precision}\n'
        output_str += f'Recall:{recall}\n'
        output_str += f'F1 Score:{f1}\n'

        return output_str

    def click(self):
        output_path = os.path.join('evaluation', 'click.txt')

        clicks = {'p': [], 'q': []}

        for user_id in self.generate_data:
            for task_id in self.generate_data[user_id]:
                for action in self.generate_data[user_id][task_id]:
                    clicks['p'].extend([1 if i in action['real_clicks'] else 0 for i in range(10)])
                    clicks['q'].extend([1 if i in action['clicks'] else 0 for i in range(10)])

        output_str = Evaluation._evaluate(clicks['p'], clicks['q'])

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(output_str)

    def stop(self):
        output_path = os.path.join('evaluation', 'stop.txt')

        stop = {'p': [], 'q': []}

        for user_id in self.generate_data:
            for task_id in self.generate_data[user_id]:
                for index, action in enumerate(self.generate_data[user_id][task_id]):
                    if index < len(self.generate_data[user_id][task_id]) - 1:
                        stop['p'].append(0)
                    else:
                        stop['p'].append(1)
                    stop['q'].append(action['stop'])

        output_str = Evaluation._evaluate(stop['p'], stop['q'])

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(output_str)


if __name__ == '__main__':
    e = Evaluation()
    e.stop()
