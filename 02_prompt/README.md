# prompt
提示工程，又称为指令工程。

## 高质量 prompt 核心要点：具体、丰富、少歧义

## Prompt 的典型构成
1. 角色：给 AI 定义一个最匹配任务的角色，比如：「你是一位软件工程师」「你是一位小学老师」
2. 指示：对任务进行描述
3. 上下文：给出与任务相关的其它背景信息（尤其在多轮交互中）
4. 例子：必要时给出举例，学术中称为 one-shot learning, few-shot learning 或 in-context learning；实践证明其对输出正确性有很大帮助
5. 输入：任务的输入信息；在提示词中明确的标识出输入
6. 输出：输出的格式描述，以便后继模块自动解析模型的输出结果，比如（JSON、XML）

## 对话系统的基本模块与思路：

```mermaid
flowchart LR
语音识别[ASR]-->语义理解[NLU]--> 状态跟踪[DST]-->对话策略[Policy]-->自然语言生成[NLG]-->语音合成[TTS]
```
## 思维链
- 思维链，是大模型涌现出来的一种神奇能力
- 有人在提问时以「Let’s think step by step」开头，结果发现 AI 会把问题分解成多个步骤，然后逐步解决，使得输出的结果更加准确

>大模型推理存在幻觉，多次执行结果可能会不一致

## 自洽性（Self-Consistency）
一种对抗「幻觉」的手段。就像我们做数学题，要多次验算一样。

核心原理：
* 同样的prompt执行多次，投票选出最终结果。
* 缺点：比较浪费token

## 思维树（Tree-of-thought, ToT）
以思维链发展出来的思想，扩展成一棵树。
- 在思维链的每一步，采样多个分支
- 拓扑展开成一棵思维树
- 判断每个分支的任务完成度，以便进行启发式搜索
- 设计搜索算法
- 判断叶子节点的任务完成的正确性

## prompt准确率调优思路
- 举例 ===> 格式 ===> 思维链 ==> 相关度高的案例 ==> 多次执行投票产生结果

## 防止攻击
著名的奶奶漏洞：利用哄骗让AI说出Windows升级序列号
### 防范思路
- 安检思路：提前写好prompt固定好system规范
- 在用户输入前增加前缀
  - 例如：作为客服代表，你不允许回答任何与XXX无关的问题。 用户说：{user_prompt}
- [ChatGPT 安全风险 | 基于 LLMs 应用的 Prompt 注入攻击](https://mp.weixin.qq.com/s/zqddET82e-0eM_OCjEtVbQ)
- [提示词破解：绕过 ChatGPT 的安全审查](https://selfboot.cn/2023/07/28/chatgpt_hacking/)
- 调用第三方内容审核API


# 划重点：具体、丰富、少歧义
- 别急着上代码，先尝试用 prompt 解决，往往有四两拨千斤的效果
- 但别迷信 prompt，合理组合传统方法提升确定性，减少幻觉
- 定义角色、给例子是最常用的技巧
- 用好思维链，让复杂逻辑/计算问题结果更准确
- 防御 prompt 攻击非常重要

# OpenAI API 的几个重要参数
其它大模型的 API 基本都是参考 OpenAI，只有细节上稍有不同。

OpenAI 提供了两类 API：

* Completion API：续写文本，多用于补全场景。https://platform.openai.com/docs/api-reference/completions/create
* Chat API：多轮对话，但可以用对话逻辑完成任何任务，包括续写文本。https://platform.openai.com/docs/api-reference/chat/create

说明：
- Chat 是主流，有的大模型只提供 Chat
- 背后的模型可以认为是一样的，但也不完全一样
- Chat 模型是纯生成式模型做指令微调之后的结果，更多才多艺，更听话