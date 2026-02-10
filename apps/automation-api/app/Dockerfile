FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Ansible
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Ansible collections during build
RUN ansible-galaxy collection install ibm.ibm_zos_core community.general ansible.posix --upgrade

# ────────────── debug ──────────────
COPY main.py .
RUN ls -la /app && which ansible-playbook && ansible-galaxy collection list | grep ibm.ibm_zos_core
# ───────────────────────────────────

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
