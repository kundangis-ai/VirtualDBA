# Virtual DBA - Quick Reference

## Launch Options

```bash
python3 dba_cli.py           # Interactive CLI interface
python3 dba_demo.py          # Run full demonstration
python3 quickstart_vdba.py   # Interactive quick start tutorial
```

## Python API Quick Reference

### Initialize
```python
from virtual_dba import VirtualDBA
dba = VirtualDBA(use_simulation=True)
```

### Connection
```python
dba.create_config(host, port, username, service_name)
dba.load_config()
dba.test_connection()
```

### User Management
```python
dba.create_user(username, password, tablespace="USERS", expiry_days=365)
dba.drop_user(username, cascade=False)
dba.list_users()
dba.grant_privilege(username, privilege)
dba.revoke_privilege(username, privilege)
```

### Tablespace Management
```python
dba.create_tablespace(name, size_mb, datafile_path)
dba.list_tablespaces()
```

### Backup & Recovery
```python
dba.backup_database(backup_type="FULL", backup_location="./backups")
  # Types: "FULL", "INCREMENTAL", "ARCHIVE_LOG"
dba.list_backups()
dba.restore_database(backup_id)
```

### Monitoring
```python
dba.get_database_status()
dba.monitor_performance()
dba.get_wait_events()
dba.execute_query(query_string)
```

### Audit & Export
```python
dba.view_audit_log(limit=20)
dba.export_metrics(filename="dba_metrics.json")
```

## CLI Command Reference

### Connection
```
create_config <h> <p> <u> <s>    Create config
load_config                       Load config
test_connection                   Test DB connection
```

### Users
```
create_user <u> <p> [ts]          Create user
drop_user <u> [cascade]           Drop user
list_users                        List users
grant_privilege <u> <priv>        Grant privilege
revoke_privilege <u> <priv>       Revoke privilege
```

### Tablespaces
```
create_tablespace <n> <s> <p>     Create tablespace
list_tablespaces                  List tablespaces
```

### Backup
```
backup [type] [location]          Perform backup
list_backups                      List backups
restore <backup_id>               Restore DB
```

### Monitoring
```
status                            Database status
perf                              Performance metrics
wait_events                       Top wait events
```

### Queries
```
query <sql>                       Execute query
```

### Other
```
audit_log [limit]                 View audit log
export [filename]                 Export metrics
help                              Show help
quit                              Exit
```

## Privilege Types

```
Data Manipulation: SELECT, INSERT, UPDATE, DELETE
Roles: CONNECT, RESOURCE
Objects: CREATE TABLE, CREATE INDEX, CREATE PROCEDURE
System: ALTER SYSTEM, ALTER SESSION
```

## Common Tasks

### Create User with Full Permissions
```python
dba.create_user("analyst", "secure_pwd", "USERS")
dba.grant_privilege("analyst", "SELECT")
dba.grant_privilege("analyst", "INSERT")
dba.grant_privilege("analyst", "UPDATE")
```

### Setup Database
```python
dba.create_config("localhost", 1521, "sys", "ORCL")
dba.test_connection()
dba.create_tablespace("USERS", 1024, "/u01/users.dbf")
```

### Perform Backup
```python
dba.backup_database("FULL", "./backups")
backups = dba.list_backups()
```

### Monitor Database
```python
status = dba.get_database_status()
metrics = dba.monitor_performance()
```

### Export Report
```python
dba.export_metrics("report.json")
```

## Return Values

```python
# List operations return data structures
users = dba.list_users()        # Returns: List[Dict]
backups = dba.list_backups()    # Returns: List[Dict]
spaces = dba.list_tablespaces() # Returns: List[Dict]

# Status operations return dictionaries
status = dba.get_database_status()    # Returns: Dict
metrics = dba.monitor_performance()   # Returns: Dict

# Query operations return results
results = dba.execute_query(sql)      # Returns: List[Dict] or None
```

## File Paths

```
virtual_dba.py                   Main module
dba_cli.py                       CLI interface
dba_demo.py                      Demo script
quickstart_vdba.py               Quick start
dba_config.json                  Configuration
README_VIRTUAL_DBA.md            Full documentation
SETUP_GUIDE.md                   Setup instructions
QUICK_REFERENCE.md               This file
```

## Return Codes

```
True                             Success
False                            Failure
None                             No data/not applicable
```

## Common Parameters

```
backup_type: "FULL" | "INCREMENTAL" | "ARCHIVE_LOG"
tablespace: String (default: "USERS")
privilege: String (custom or predefined)
cascade: True | False (default: False)
expiry_days: Integer | None (default: None)
```

## Example Scenarios

### Scenario 1: New User Onboarding
```python
dba = VirtualDBA()
dba.create_user("newuser", "temppass", "USERS")
dba.grant_privilege("newuser", "SELECT")
dba.grant_privilege("newuser", "INSERT")
dba.list_users()
```

### Scenario 2: Database Backup & Recovery
```python
dba.backup_database("FULL")
backups = dba.list_backups()
backup_id = backups[0]['backup_id']
dba.restore_database(backup_id)
```

### Scenario 3: Performance Analysis
```python
status = dba.get_database_status()
metrics = dba.monitor_performance()
events = dba.get_wait_events()
dba.export_metrics("analysis.json")
```

### Scenario 4: Audit Review
```python
audit = dba.view_audit_log(limit=50)
dba.export_metrics("audit_report.json")
```

## Tips & Tricks

1. **Check Return Values:** Always check if operations returned True/False
2. **Export Data:** Use `export_metrics()` for reporting
3. **Review Audit:** Check `view_audit_log()` for troubleshooting
4. **Test First:** Use `test_connection()` before operations
5. **Batch Operations:** Loop for creating multiple users/tablespaces

## Keyboard Shortcuts (CLI)

```
Ctrl+C                            Exit/Interrupt
↑                                 Previous command
↓                                 Next command
Tab                               Auto-complete (if available)
```

## Troubleshooting Quick Guide

| Issue | Solution |
|-------|----------|
| Module not found | Verify file path and Python version |
| Command not found | Type `help` to see available commands |
| Connection failed | Check credentials in config file |
| User exists error | User already created, use different name |
| Privilege not granted | Verify privilege name is valid |

## Version & Info

- **Current Version:** 1.0
- **Python:** 3.7+
- **Mode:** Simulation (no external dependencies)
- **Status:** Ready to use

---

**Quick Start:** `python3 dba_cli.py` and type `help`
