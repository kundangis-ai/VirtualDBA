# Virtual DBA - Installation & Setup Guide

## Quick Setup (2 minutes)

### Step 1: Verify Python Installation

```bash
python3 --version
# Expected: Python 3.7 or higher
```

### Step 2: Copy Files to Your Project Directory

Copy the following files to your project folder:
- `virtual_dba.py` - Core Virtual DBA module
- `dba_cli.py` - Interactive CLI interface
- `dba_demo.py` - Demonstration script
- `quickstart_vdba.py` - Quick start tutorial
- `dba_config.json` - Configuration file (optional)
- `README_VIRTUAL_DBA.md` - Full documentation

### Step 3: Verify Installation

```bash
python3 -c "from virtual_dba import VirtualDBA; print('✓ Virtual DBA ready!')"
```

## Getting Started

### Option A: Interactive CLI (Recommended for Beginners)

```bash
python3 dba_cli.py
```

Then type commands:
```
VirtualDBA> help                          # Show all commands
VirtualDBA> create_user scott tiger       # Create a user
VirtualDBA> list_users                    # View users
VirtualDBA> backup FULL                   # Backup database
VirtualDBA> status                        # Check status
VirtualDBA> quit                          # Exit
```

### Option B: Quick Start Tutorial

```bash
python3 quickstart_vdba.py
```

This provides an interactive tutorial that walks you through:
- Creating users with privileges
- Managing tablespaces
- Performing backups
- Monitoring performance

### Option C: Run Demo Script

```bash
python3 dba_demo.py
```

This demonstrates all features automatically:
- Connection management
- User & privilege management
- Tablespace operations
- Backup & recovery
- Performance monitoring
- Query execution
- Audit logging
- Advanced scenarios

### Option D: Use in Your Python Code

```python
from virtual_dba import VirtualDBA

# Initialize
dba = VirtualDBA(use_simulation=True)

# Create user
dba.create_user("analyst", "secure_pwd", "USERS", expiry_days=365)

# Grant privileges
dba.grant_privilege("analyst", "SELECT")
dba.grant_privilege("analyst", "INSERT")

# Perform operations
dba.list_users()
dba.get_database_status()
dba.backup_database("FULL", "./backups")
dba.export_metrics("report.json")
```

## File Organization

```
your_project/
├── virtual_dba.py              # Core module (required)
├── dba_cli.py                  # CLI interface
├── dba_demo.py                 # Demo script
├── quickstart_vdba.py          # Quick start
├── dba_config.json             # Configuration
├── README_VIRTUAL_DBA.md       # Documentation
└── SETUP_GUIDE.md              # This file
```

## System Requirements

### Minimum Requirements
- Python 3.7+
- 10 MB disk space
- No additional dependencies for simulation mode

### For Real Oracle Connections
- Oracle Instant Client (optional)
- Oracle database credentials
- Network access to Oracle database

## Features Overview

### ✓ User Management
- Create/drop users with expiry dates
- Grant/revoke privileges
- View user information

### ✓ Tablespace Management
- Create and manage tablespaces
- Monitor usage and capacity
- Track datafile locations

### ✓ Backup & Recovery
- Full, incremental, and archive backups
- Automatic backup tracking
- One-click restore functionality

### ✓ Performance Monitoring
- Real-time database status
- Performance metrics (CPU, memory, disk)
- Wait events analysis
- Transaction monitoring

### ✓ Query Execution
- Execute SQL queries
- Display results in table format
- Error handling and logging

### ✓ Audit & Compliance
- Comprehensive audit trail
- Action tracking and logging
- Export to JSON format
- Compliance reporting

## Configuration

### Default Configuration (dba_config.json)

```json
{
  "host": "localhost",
  "port": 1521,
  "username": "sys",
  "service_name": "ORCL",
  "password": "oracle123"
}
```

### Create Custom Configuration

In Python:
```python
dba = VirtualDBA()
dba.create_config(
    host="192.168.1.100",
    port=1521,
    username="admin",
    service_name="MYDB"
)
```

In CLI:
```
VirtualDBA> create_config 192.168.1.100 1521 admin MYDB
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'virtual_dba'"

**Solution:**
```bash
# Make sure you're in the correct directory
cd /path/to/virtual_dba
python3 dba_cli.py
```

### Issue: "KeyboardInterrupt" or Ctrl+C exits suddenly

**Solution:** This is normal behavior. Just run the program again.

### Issue: Commands not recognized in CLI

**Solution:**
```
VirtualDBA> help                          # See all commands
VirtualDBA> help create_user              # Get help for specific command
```

### Issue: Directory creation errors during backup

**Solution:**
```bash
# Ensure backup directory exists or use current directory
mkdir -p ./backups
```

## Common Usage Patterns

### Pattern 1: Setting Up a Development Environment

```python
dba = VirtualDBA()

# Create dev users
dba.create_user("devuser1", "dev123", "DEVELOPMENT")
dba.create_user("devuser2", "dev123", "DEVELOPMENT")

# Grant development privileges
for user in ["devuser1", "devuser2"]:
    dba.grant_privilege(user, "CONNECT")
    dba.grant_privilege(user, "RESOURCE")
    dba.grant_privilege(user, "CREATE TABLE")
    dba.grant_privilege(user, "CREATE INDEX")

# Create dev tablespace
dba.create_tablespace("DEV_DATA", 1024, "/u01/oradata/orcl/dev_data.dbf")

# Backup dev environment
dba.backup_database("FULL", "./backups/dev")
```

### Pattern 2: Monitoring Script

```python
dba = VirtualDBA()

# Check database health
status = dba.get_database_status()
metrics = dba.monitor_performance()
wait_events = dba.get_wait_events()

# Export report
dba.export_metrics("health_report.json")
```

### Pattern 3: User Provisioning Automation

```python
dba = VirtualDBA()

new_users = [
    ("alice", "alice123", "USERS"),
    ("bob", "bob123", "USERS"),
    ("charlie", "charlie123", "ANALYTICS")
]

for username, password, tablespace in new_users:
    dba.create_user(username, password, tablespace)
    dba.grant_privilege(username, "CONNECT")
    dba.grant_privilege(username, "SELECT")
    print(f"User {username} created successfully")
```

## Performance Tips

1. **For Large Datasets:** Export data directly instead of displaying
2. **For Frequent Operations:** Load configuration once and reuse connection
3. **For Batch Operations:** Group operations in loops
4. **For Audit Logs:** Regularly export and archive old logs

## Next Steps

1. **Learn More:** Read `README_VIRTUAL_DBA.md`
2. **Try Examples:** Run `dba_demo.py`
3. **Experiment:** Use `quickstart_vdba.py`
4. **Integrate:** Use in your own scripts

## Support Resources

- 📖 Full Documentation: `README_VIRTUAL_DBA.md`
- 🎓 Examples: `dba_demo.py`
- 🚀 Quick Start: `quickstart_vdba.py`
- 💻 Interactive CLI: `dba_cli.py`

## Version Information

- **Version:** 1.0
- **Release Date:** February 18, 2024
- **Python Support:** 3.7+
- **License:** Educational Use

---

**Ready to get started? Run:** `python3 dba_cli.py` 🚀
