## Activate Environment
- To activte the virtual environment for this application:
`source finance_venv/bin/activate`

- save dependencies:
` pip freeze > requirements.txt`

- When DONE:
`deactivate`

## Current Structure
finance_app/
│
├── app.py                  # Main Dash app entry point
├── requirements.txt        # Python dependencies
├── .env                    # API keys and secrets (e.g., GEMINI_API_KEY)
│
├── data/
│   └── fetch_yahoo.py      # Scripts for fetching and updating Yahoo Finance data
│
├── components/
│   ├── dashboard.py        # Dashboard layout and callbacks
│   ├── chatbot.py          # Chatbot UI and integration logic
│   └── utils.py            # Helper functions (formatting, calculations, etc.)
│
├── assets/
│   └── custom.css          # Custom styles for Dash/Bootstrap
│
└── README.md               # Project overview and setup instructions

