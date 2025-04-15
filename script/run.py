import subprocess
import re
import openai
import os
import json

url_prompt_table = {
    "https://quote.eastmoney.com/globalfuture/GC00Y.html":"Please help extract COMEX黄金价格from the content",
    "https://www.balticexchange.com/en/index.html": "Please help extract BSPA index from the content, in format: BSPA: ANSWER",
    "https://www.sse.net.cn/index/singleIndex?indexType=ccfi": "Please help extract 中国出口集装箱运价综合指数 from the content, in format: 中国出口集装箱运价综合指数: ANSWER",
    "https://www.sse.net.cn/index/singleIndex?indexType=scfi": "Please help extract 综合指数 Comprehensive Index from the content, in format: 综合指数 Comprehensive Index: ANSWER",
    "https://www.sse.net.cn/index/singleIndex?indexType=cdi": "Please help extract 综合指数 from the content, in format: 综合指数 : ANSWER",
    "https://www.epanasia.com/freightIndex/": "新华-泛亚内贸集装箱船运价指数",
    "https://cn.investing.com/indices/usdollar": "Please help extract 美元指数from the content",
    "https://quote.eastmoney.com/globalfuture/GC00Y.html": "Please help extract COMEX黄金价格from the content",
    "https://quote.eastmoney.com/globalfuture/B00Y.html": "Please help extract 布伦特原油当月连续价格from the content",
}


def init_openai():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.organization = os.environ['ORG_ID']


def get_completion(prompt, temperature=0.0, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


def update_js_config(file_path, new_url, new_match, new_max_pages, new_output_file):
    """
    Update the JavaScript config file with new values for url, match, maxPagesToCrawl, and outputFileName.

    :param file_path: Path to the JavaScript config file.
    :param new_url: New value for the url.
    :param new_match: New value for the match.
    :param new_max_pages: New value for maxPagesToCrawl.
    :param new_output_file: New value for outputFileName.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith('url:'):
            new_lines.append(f'  url: "{new_url}",\n')
        elif line.strip().startswith('match:'):
            new_lines.append(f'  match: "{new_match}",\n')
        elif line.strip().startswith('maxPagesToCrawl:'):
            new_lines.append(f'  maxPagesToCrawl: {new_max_pages},\n')
        elif line.strip().startswith('outputFileName:'):
            new_lines.append(f'  outputFileName: "{new_output_file}",\n')
        else:
            new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)


def prepare_config_file(src_file, dest_file):
    import shutil
    # Copying config_base.ts to config.ts
    shutil.copyfile(src_file, dest_file)


def read_json(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    return str(json_data)


def generate_outfile_from_url(url):
    return re.sub(r'[^0-9a-zA-Z]+', '-', url)


def run_crawler():
    # Running the "npm start" command and waiting for it to finish
    process = subprocess.run(["npm", "start"], check=True)
    print("npm finishes its task")


def run_gpt_analysis():
    pass


if __name__ == '__main__':
    # init_openai()
    for url, prompt in url_prompt_table.items():
        prepare_config_file("../config_base.ts", "../config.ts")
        output_file = generate_outfile_from_url(url) + ".json"
        update_js_config(file_path="../config.ts", new_url=url, new_match=url, new_max_pages=50,
                         new_output_file=output_file)

        run_crawler()
        # json_data_str = read_json("../" + output_file)
        # prompt_qa = "The following content is scraped from a website and stored in json format: \n" + json_data_str + "\n" + prompt
        # result = get_completion(prompt=prompt_qa)
        # print(result)
