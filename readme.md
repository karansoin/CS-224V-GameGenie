# Celeste GameGenie Setup

## 1: Clone and Navigate to Repository
```bash
git clone https://github.com/karansoin/CS-224V-GameGenie.git
cd CS-224V-GameGenie
```

## 2: Conda environment setup
```bash
conda create -n celeste python=3.11
conda activate celeste
conda install -c conda-forge libffi
```

## 3: Install Genie Worksheets library
```bash
git clone https://github.com/stanford-oval/genie-worksheets.git
pip install uv
uv pip install -e ./genie-worksheets
```

## 4: Create env file with appropriate variables
```bash
cp .env.example .env
```

Edit `.env` and add your personal API key:
```
LLM_API_KEY=sk-your-api-key-here
EXA_API_KEY=your_database_api_key_here
LLM_API_BASE_URL=https://cs224v-litellm.genie.stanford.edu
LLM_API_ENDPOINT=https://cs224v-database-agent.genie.stanford.edu/database-exploration
```

## 5: Open / Start Notebook
```bash
jupyter notebook llm_notebook.ipynb
```

Then select Kernel → Change Kernel → `celeste`