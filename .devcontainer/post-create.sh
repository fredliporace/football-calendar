set -euo pipefail

# Fix ownership on mounted volumes (Docker volumes are usually root:root)
echo "=== AWS setup ==="
sudo chown -R vscode:vscode /home/vscode/.aws || true

echo "=== Cline persistence setup starting ==="

# Fix ownership on mounted volumes (Docker volumes are usually root:root)
sudo chown -R vscode:vscode /home/vscode/.cline || true
sudo chown -R vscode:vscode /home/vscode/.cline-history || true

# Ensure all needed subdirectories exist in the persistent volume
mkdir -p /home/vscode/.cline-history/{cache,checkpoints,settings,state,tasks}

# Ensure the target globalStorage directory exists
sudo mkdir -p /home/vscode/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev
sudo chown -R vscode:vscode /home/vscode/.vscode-server/data || true

# Create symlinks so Cline writes/reads from the persistent volume
ln -sfn /home/vscode/.cline-history/cache    /home/vscode/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/cache || true
ln -sfn /home/vscode/.cline-history/checkpoints    /home/vscode/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/checkpoints || true
ln -sfn /home/vscode/.cline-history/settings /home/vscode/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/settings || true
ln -sfn /home/vscode/.cline-history/state    /home/vscode/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/state || true
ln -sfn /home/vscode/.cline-history/tasks    /home/vscode/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/tasks || true

echo "Persisted directories:"
ls -ld /home/vscode/.cline-history/* 2>/dev/null || true

echo "=== Cline persistence setup completed ==="

# SSH keys
echo "=== SSH setup ==="
sudo chown -R vscode:vscode /home/vscode/.ssh || true

# echo "=== Installing project dev dependencies ==="
sudo chown -R vscode:vscode /home/vscode/.local/bin || true
pip install -e .[dev,aws,cli] -c requirements.txt
pre-commit install
pre-commit install-hooks
