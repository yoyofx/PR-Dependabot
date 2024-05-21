import os
from pathlib import Path
import subprocess
from langchain_openai import OpenAI,ChatOpenAI
from langchain.prompts import PromptTemplate

# os.environ['OPENAI_API_BASE'] =  "xxxx"
# os.environ['OPENAI_API_KEY'] = "xxxxx"
defaultModelName = 'gpt-3.5-turbo'

llm = ChatOpenAI(temperature=0.95 , model_name = defaultModelName, max_tokens=1500)

# 定义命令和参数
command = ["trivy", "fs", "-f", "json", "-o", "results.json", "."]
try:
    # 执行命令并等待其完成
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("Command executing .......")
    # 打印命令的标准输出和标准错误
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    print("Command executed successfully.")

except subprocess.CalledProcessError as e:
    # 命令执行失败时处理错误
    print("An error occurred while executing the command.")
    print("stderr:", e.stderr)

with open("results.json", 'r', encoding='utf-8') as file:
    vuln_file = file.read()

with open("results.json", 'r', encoding='utf-8') as file:
    gomod_file = file.read()

# 定义模板
pr_template = """
请对比组件内容和组件漏洞清单,生产一个Github格式的PR:

组件漏洞清单如下:
{vuln_file}

go.mod文件 组件内容如下:
{gomod_file}

参考如下格式:
## Changes

Bumps golang.org/x/net from 0.19.0 to 0.21.0.

Bumps golang.org/x/xx from 0.10.0 to 0.11.0.

## Testing

Ensure all tests pass and the application functions as expected.

## References

- [CVE-2023-45288](https://avd.aquasec.com/nvd/cve-2023-45288)
- [CVE-2024-24786](https://avd.aquasec.com/nvd/cve-2024-24786)
"""

# 定义 PromptTemplate
prompt = PromptTemplate(
    input_variables=["vuln_file", "gomod_file"],
    template=pr_template
)

# 生成描述
pr_description = prompt.format(
    vuln_file=vuln_file,
    gomod_file=gomod_file
)

# print(pr_description)
# 使用 LLM 生成输出
output = llm.predict(pr_description)

# 打印生成的 Pull Request 描述
print(output)


