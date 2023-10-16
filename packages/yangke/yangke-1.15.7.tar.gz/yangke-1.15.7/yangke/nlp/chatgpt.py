# 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
import openai

openai.api_key = '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'

prompt = '你知道西安热工院吗？'


def completion(prompt):
    """
    根据提示续写文本内容

    :param prompt: 用户给出的提示文本
    :return:
    """
    engine = 'text-davinci-003'  # 两个模型
    engine = 'davinci'
    com = openai.Completion.create(engine=engine,
                                   prompt=prompt,
                                   max_tokens=1024,
                                   n=1,
                                   stop=None,
                                   temperature=0.5)

    response = com.choices[0].text
    return response


def chat(question):
    """
    聊天机器人，
    :param question: 用户发出的提问或回复
    :return:
    """
    model = 'gpt-3.5-turbo'
    model = 'gpt-3.5-turbo-0301'
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "一个有10年Python开发经验的资深算法工程师"},  # 机器人的人设，
            {"role": "user", "content": question}  # 表示是用户提问内容
        ]
    )

    text = response.get("choices")[0]["message"]["content"]
    return text


print(chat(prompt))
