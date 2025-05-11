# AI-discord
Links LM studio with your personal discord account 

# Features:
- Only authorized people can chat with AI

# Step 1
- pip uninstall discord.py
- pip install git+https://github.com/dolfies/discord.py-self
- (other way around when done)

# Step 2
- Open in code editor

# Step 3
- Open your account that you want to use in your browser. Press CTRL+I+SHIFT (to open network tab). then send a message to anyone. Click the sent message in the network tab. Look for "AUTHORIZED" property. There should be your discord token.

# Step 4
- Put discord token in TOKEN
- Put LLM in payload ("model": "YOUR_LLM",)
- Put user ID's in AUTHORIZED_USER_IDS 

