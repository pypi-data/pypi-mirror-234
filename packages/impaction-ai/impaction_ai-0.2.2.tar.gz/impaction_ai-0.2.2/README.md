# impaction.ai Python SDK

This is the official server-side Python SDK for [impaction.ai](https://impaction.ai/). This library allows you to easily send your data to impaction.ai.

Visit the [full documentation](https://docs.impaction.ai/introduction) to see the detailed usage.


# Installation

Install the Python SDK with pip:

```python
pip install impaction-ai
```

# Getting Started

Below is a typical usage of the SDK:

```python
from impaction_ai import ImpactionAI
from impaction_ai.constants import ROLE_USER

# Initialize SDK Client
imp = ImpactionAI(
    project_id="PROJECT_ID",
    api_key="API_KEY"
)

# Record a user
imp.identify_user(
    user_id="USER_ID",
    email="USER_EMAIL",
    country_code="US"
)

# Open a session
imp.open_session(
    session_id="SESSION_ID",
    user_id="USER_ID",
    assistant_id="ASSISTANT_ID"
)

# Record a message
imp.create_message(
    session_id="SESSION_ID",
    message_index=1,
    role=ROLE_USER,
    content="Hey, you there?"
)

# Close a session
imp.close_session(
    session_id="SESSION_ID"
)
```

Refer to the documentation to see more detailed usage.

# Contribution

If you have any issues with the SDK, feel free to open Github issues and we'll get to it as soon as possible.

We welcome your contributions and suggestions!