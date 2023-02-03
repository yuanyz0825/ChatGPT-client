import tkinter as tk
import openai
from collections import deque  # 加入deque版本号

#openai.api_key = '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'
openai.api_key='替换自己的key'
history = deque(maxlen=10)  # 新增处


def send_message():
    global history
    new_prompt = entry.get('1.0', tk.END)
    prompt = ''.join(history) + new_prompt  # 新增处
    history.append(f"{'请回答: '}{new_prompt}")  # 新增处
    if prompt[-1] == 'Q':
        root.quit()
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )
        text.config(state='normal')  # 使框可编辑
        text.insert(tk.END, "Human: " + new_prompt + "\n", 'yes')
        text.insert(tk.END, "AI: " + response['choices'][0]['text'].strip() + "\n", 'no')
        text.tag_config('yes', foreground='blue')  # 设置文字颜色
        text.tag_config('no', foreground='red')
        text.config(state='disabled')  # 使文本框不可编辑
        history.append(f"{'上面问题的回答: '}{response['choices'][0]['text'].strip()}\n")  # 新增处
        entry.delete('1.0', tk.END)
    except Exception as e:

        text.insert(tk.END, str(e), 'err')  # 设置提示文本
        text.tag_config('err', foreground='red')
        text.insert(tk.END, "\n")


root = tk.Tk()
root.title("OpenAI Chatbot")

frame = tk.Frame(root)
frame.pack(pady=10)

text = tk.Text(frame, height=15, width=50)
text.pack(side=tk.LEFT, fill=tk.Y)

scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

text.configure(yscrollcommand=scroll.set)  # 加入滚动条
scroll.config(command=text.yview)

entry = tk.Text(root, width=50, height=5)
entry.pack(pady=5)
entry.configure(yscrollcommand=scroll.set)  # 加入滚动条
scroll.config(command=entry.yview)

send = tk.Button(root, text="Send", command=send_message)
send.pack()

root.mainloop()
