# USimAgent: Large Language Models for Simulating Search Users

Due to the advantages in the cost-efficiency and reproducibility, user simulation has become a promising solution to the user-centric evaluation of information retrieval systems. Nonetheless, accurately simulating user search behaviors has long been a challenge, be cause users’ actions in search are highly complex and driven by intricate cognitive processes such as learning, reasoning, and plan ning. Recently, Large Language Models (LLMs) have demonstrated remarked potential in simulating human-level intelligence and have been used in building autonomous agents for various tasks. How ever, the potential of using LLMs in simulating search behaviors has not yet been fully explored. In this paper, we introduce a LLM based user search behavior simulator, USimAgent. The proposed simulator can simulate users’ querying, clicking, and stopping be haviors during search, and thus, is capable of generating complete search sessions for specific search tasks. Empirical investigation on a real user behavior dataset shows that the proposed simulator outperforms existing methods in query generation and is compara ble to traditional methods in predicting user clicks and stopping behaviors. These results not only validate the effectiveness of using LLMs for user simulation but also shed light on the development of a more robust and generic user simulators.


## 🛠 Installation

To install RecAgent, one can follow the following steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/Meow-E/USimAgent.git
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key in the `config/config.py` file.

## 💡 Note

The discrepancies between the results in the code and those in the paper are due to:

- We have been striving for better prompts, transitioning from intricately designed prompts to concise and robust instructions. While these simplified instructions may initially lead to performance degradation, we are exploring methods beyond prompt engineering to enhance the capabilities of LLMs.
- Updates and iterations in OpenAI models: We have switched to the more cost-effective GPT-4o-mini model and set the temperature to 0.7.
- For query generation, BLEU is not a reliable evaluation metric. In our latest work, we have incorporated more query evaluation metrics for assessment. Therefore, the evaluation results based on BLEU may be somewhat distorted.

## 📚 Data

We evaluated our USimAgent on [The Search Evaluation Dataset – – THUIR](http://www.thuir.cn/KDD19-UserStudyDataset/).

We adhere to several rules for data filtration: 

+ Due to various reasons, search URLs for four tasks were predominantly invalid, unable to replicate the content originally viewed by the users, hence, those tasks were excluded. 
+ The original dataset featured SERPs of varying lengths; for lists exceeding ten results, only the top ten were retained. 
+ Incomplete sessions, characterized by missing click information or having partial SERPs, were removed.

Finally, 164 sessions from 40 users met these constrictions, and we retained these search sessions to form the evaluation dataset.

## 📄 Citation

Welcome to cite our paper if you find it helpful. [![Paper](https://img.shields.io/badge/arxiv-PDF-red)](https://arxiv.org/abs/2403.09142.pdf)

```
@misc{zhang2024usimagentlargelanguagemodels,
      title={USimAgent: Large Language Models for Simulating Search Users}, 
      author={Erhan Zhang and Xingzhu Wang and Peiyuan Gong and Yankai Lin and Jiaxin Mao},
      year={2024},
      eprint={2403.09142},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
      url={https://arxiv.org/abs/2403.09142}, 
}
```

