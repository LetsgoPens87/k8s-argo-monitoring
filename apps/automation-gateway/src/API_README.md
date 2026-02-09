# Ansible Playbook API

A FastAPI endpoint to run Ansible playbooks from HTTP requests.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you're in the ansible-zos directory:
```bash
cd /home/ec2-user/ansible-zos
```

3. Ensure your Ansible playbooks and inventory files are in the `ansible/` subdirectory

## Running the API

```bash
python api.py
```

The API will start on `http://localhost:8000`

## API Endpoints

### POST /run-playbook
Runs an Ansible playbook and returns the output.

**Request body:**
```json
{
  "playbook": "create_hamlet_jcl.yml",
  "inventory": "inventory.yml",
  "extra_vars": {
    "variable_name": "value"
  }
}
```

**Parameters:**
- `playbook` (optional): Name of the playbook file (default: `create_hamlet_jcl.yml`)
- `inventory` (optional): Inventory file to use (default: `inventory.yml`)
- `extra_vars` (optional): Dictionary of additional variables to pass to the playbook

**Response:**
```json
{
  "success": true,
  "exit_code": 0,
  "stdout": "PLAY [default] ****...",
  "stderr": "",
  "playbook": "create_hamlet_jcl.yml"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /available-playbooks
Lists all available playbooks in the ansible directory.

**Response:**
```json
{
  "playbooks": ["create_hamlet_jcl.yml", "gather_facts.yml", ...],
  "directory": "/home/ec2-user/ansible-zos/ansible"
}
```

## Examples

### Using curl

Default playbook (create_hamlet_jcl.yml):
```bash
curl -X POST http://localhost:8000/run-playbook \
  -H "Content-Type: application/json" \
  -d '{}'
```

Specific playbook with extra variables:
```bash
curl -X POST http://localhost:8000/run-playbook \
  -H "Content-Type: application/json" \
  -d '{
    "playbook": "gather_facts.yml",
    "inventory": "inventory.yml",
    "extra_vars": {
      "target_host": "my_host"
    }
  }'
```

### Using Python requests

```python
import requests

payload = {
    "playbook": "create_hamlet_jcl.yml",
    "inventory": "inventory.yml"
}

response = requests.post(
    "http://localhost:8000/run-playbook",
    json=payload
)

result = response.json()
print(f"Success: {result['success']}")
print(f"Output:\n{result['stdout']}")
if result['stderr']:
    print(f"Errors:\n{result['stderr']}")
```

## Interactive API Documentation

Once the API is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These provide interactive documentation where you can test the endpoints directly.
