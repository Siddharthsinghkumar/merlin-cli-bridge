import re

with open("server.py", "r") as f:
    content = f.read()

# Fix the is_local line
content = content.replace('if is_local and "@models" not in last_msg and "!effert" not in last_msg:', 'if is_local and "#models" not in last_msg and "#effort" not in last_msg and "#effert" not in last_msg:')
content = content.replace('if is_local and "#models" not in last_msg and "#effort" not in last_msg and "#effert" not in last_msg and "#effort" not in last_msg and "#effert" not in last_msg:', 'if is_local and "#models" not in last_msg and "#effort" not in last_msg and "#effert" not in last_msg:')

# Replace @models with #models in the intercept block
content = content.replace('if "@models" in last_msg:', 'if "#models" in last_msg:')
content = content.replace('Intercept @models command', 'Intercept #models command')

# Clean up the duplicated block injected by multi_replace_file_content
content = re.sub(r'       # Intercept #models command for live scraping.*?except Exception as e:\n            pass', '', content, flags=re.DOTALL)

with open("server.py", "w") as f:
    f.write(content)
