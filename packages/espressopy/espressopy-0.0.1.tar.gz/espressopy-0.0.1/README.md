# Espresso.py
Espresso.py is the new way to develop Discord bots using Python.

Current Version: alpha-v0.0.2

# Usage
The `member` object is user to get and modify data for guild members.

### Ban
Usage: `espresso.member.ban("userid", "guildid", "reason", "delete_seconds")`  
User ID: The ID of the user to ban.  
Guild ID: Guild of which to ban the member in.  
Reason: Reason for ban.  
Delete Seconds: How many seconds worth of messages to delete, up to 604800 (7 days).

### Kick
Usage: `espresso.member.kick("userid", "guildid", "reason")`  
User ID: The ID of the user to kick.  
Guild ID: Guild ID of which to kick the member in.  
Reason: Reason for kick.