import requests
import subprocess
import os
import glob

class CodingAgent:
    """Complete Python development agent"""

    def __init__(self):
        self.model = 'devstral-small-2'

    def chat(self, prompt):
        """Send prompt to ollama"""
        try:
            response = requests.post('http://localhost:11434/api/generate',
                                   json={
                                       'model': self.model,
                                       'prompt': prompt,
                                       'stream': False
                                   })
            return response.json()['response']
        except Exception as e:
            return f"Error: {e}"

    def analyze_project(self):
        """Analyze current Python project"""
        files = glob.glob("**/*.py", recursive=True)
        context = "Project structure:\n"
        for f in files[:5]:
            try:
                with open(f, 'r') as file:
                    content = file.read()[:150]
                    context += f"\n{f}:\n{content}...\n"
            except Exception:
                continue
        return context

    def create_plan(self, task):
        """Create development plan"""
        prompt = f"""Create a detailed development plan for: {task}

Format as numbered steps:
1. Step one
2. Step two
etc.

Be specific and actionable for Python development."""

        response = self.chat(prompt)
        steps = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                steps.append(line)
        return steps

    def generate_code(self, description, filename=None):
        """Generate Python code from description"""
        if not filename:
            if "test" in description.lower():
                filename = "test_generated.py"
            elif "main" in description.lower():
                filename = "main_generated.py"
            else:
                filename = "generated.py"

        prompt = f"""Write complete Python code for: {description}

Requirements:
- Working, executable code
- Proper functions and classes
- Error handling where needed
- Include main section if appropriate

Return only Python code."""

        code = self.chat(prompt)

        # Clean up response
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        return code, filename

    def test_code(self, filename):
        """Test Python code for errors"""
        if not os.path.exists(filename):
            return False, f"File {filename} not found"

        try:
            # Syntax check
            with open(filename, 'r') as f:
                code = f.read()
            compile(code, filename, 'exec')

            # Run test
            result = subprocess.run(['python', filename],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                return True, f"✓ {filename} works correctly"
            else:
                return False, f"✗ Runtime error: {result.stderr}"

        except Exception as e:
            return False, f"✗ Error: {e}"

    def full_development_workflow(self, request):
        """Complete development workflow"""
        result = f"🤖 Full Development Agent\n{'='*50}\n"

        # Step 1: Analyze current context
        result += "📋 Step 1: Project Analysis\n"
        context = self.analyze_project()
        result += context + "\n"

        # Step 2: Create plan
        result += "📝 Step 2: Development Plan\n"
        plan = self.create_plan(request)
        if plan:
            for step in plan:
                result += f"  {step}\n"
        result += "\n"

        # Step 3: Generate code
        result += "💻 Step 3: Code Generation\n"
        code, filename = self.generate_code(request)

        try:
            with open(filename, 'w') as f:
                f.write(code)
            result += f"Created {filename}:\n{code[:200]}...\n\n"
        except Exception as e:
            result += f"Error creating file: {e}\n\n"
            return result

        # Step 4: Test and validate
        result += "🧪 Step 4: Testing & Validation\n"
        success, message = self.test_code(filename)
        result += message + "\n\n"

        # Step 5: Summary
        result += "📊 Step 5: Summary\n"
        if success:
            result += f"✅ Successfully completed: {request}\n"
            result += f"📁 Generated file: {filename}\n"
        else:
            result += f"⚠️  Task completed with issues. Check {filename}\n"

        return result

def main():
    agent = CodingAgent()

    print("🤖 Full Python Development Agent")
    print("Type 'quit' to exit\n")

    while True:
        request = input("Describe your development task: ").strip()

        if request.lower() == 'quit':
            break

        if not request:
            continue

        print("\n" + agent.full_development_workflow(request))
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()