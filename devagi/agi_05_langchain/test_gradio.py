import gradio as gr
import os

def save_file(input_file):
    # 打印文件名和文件大小
    print(f"File name: {input_file.name}")
    # save_directory = "uploads"  # 指定保存目录
    # os.makedirs(save_directory, exist_ok=True)  # 如果目录不存在则创建
    # save_path = os.path.join(save_directory, input_file.name)  # 构建保存路径
    # with open(save_path, "wb") as f:
    #     f.write(input_file.read())  # 将上传的文件写入到指定目录中
    return "文件已保存。"

# 创建 Gradio 接口
interface = gr.Interface(
    fn=save_file,
    inputs=gr.File(label="上传文件", type="filepath"),
    outputs="text",
    title="上传文件并保存到指定目录",
    description="上传文件并将其保存到指定目录中。",
)
interface.launch()
