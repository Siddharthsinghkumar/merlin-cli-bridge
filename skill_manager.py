import json
import os
import yaml

SKILL_PATHS = [
    os.path.expanduser("~/.config/devin/skills"),
    os.path.expanduser("~/.gemini/config/plugins/agent-skills/skills"),
    os.path.expanduser("~/.gemini/config/plugins/ponytail/skills"),
    os.path.expanduser("~/.gemini/antigravity-cli/builtin/skills"),
    os.path.join(os.getcwd(), ".agents/skills")
]

class SkillManager:
    def __init__(self):
        self.skills = {}
        
    def load_skills(self):
        self.skills = {}
        for path in SKILL_PATHS:
            if os.path.exists(path):
                for skill_name in os.listdir(path):
                    skill_dir = os.path.join(path, skill_name)
                    skill_md = os.path.join(skill_dir, "SKILL.md")
                    if os.path.isdir(skill_dir) and os.path.exists(skill_md):
                        # Simple frontmatter parsing
                        description = "No description"
                        with open(skill_md, "r", encoding="utf-8") as f:
                            content = f.read()
                            if content.startswith("---"):
                                try:
                                    end_idx = content.find("---", 3)
                                    if end_idx != -1:
                                        frontmatter = yaml.safe_load(content[3:end_idx])
                                        if isinstance(frontmatter, dict):
                                            description = frontmatter.get("description", description)
                                except Exception:
                                    pass
                        self.skills[skill_name] = {
                            "path": skill_md,
                            "description": description
                        }
        print(f"Loaded {len(self.skills)} skills as virtual MCP tools.")

    def get_tools(self):
        return [
            {
                "name": "list_skills",
                "description": "List all available AI skills and their descriptions.",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                },
                "server": "virtual_skill_server"
            },
            {
                "name": "read_skill",
                "description": "Read the instructions (SKILL.md) for a specific skill. You MUST read a skill before you execute it.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": "The name of the skill to read"
                        }
                    },
                    "required": ["skill_name"]
                },
                "server": "virtual_skill_server"
            }
        ]

    def call_tool(self, name, arguments):
        if name == "list_skills":
            skills_list = "\n".join([f"- {name}: {info['description']}" for name, info in self.skills.items()])
            return {"content": [{"type": "text", "text": f"Available Skills:\n{skills_list}"}]}
        elif name == "read_skill":
            skill_name = arguments.get("skill_name")
            if skill_name in self.skills:
                with open(self.skills[skill_name]["path"], "r", encoding="utf-8") as f:
                    content = f.read()
                return {"content": [{"type": "text", "text": content}]}
            else:
                return {"content": [{"type": "text", "text": f"Skill '{skill_name}' not found. Use list_skills to see available skills."}]}
        return None

    def get_skills_xml(self):
        xml = []
        for t in self.get_tools():
            xml.append(f"<plugin>\n<name>{t['name']}</name>\n<description>{t.get('description', '')}</description>\n<inputSchema>\n{json.dumps(t.get('inputSchema', {}), indent=2)}\n</inputSchema>\n</plugin>")
        return "\n".join(xml)
