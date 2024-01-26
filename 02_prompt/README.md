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
