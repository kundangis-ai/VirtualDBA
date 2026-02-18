# Virtual DBA - Oracle Database Management Tool

A comprehensive Python-based Virtual DBA tool for managing Oracle databases. This tool provides features for user management, tablespace administration, backup & recovery, performance monitoring, and more.

## Features

### 🎯 Core Capabilities

#### Connection Management
- Create and save database configurations
- Test database connections
- Support for both real Oracle connections and simulation mode
- Secure password handling

#### User Management
- Create/drop database users
- Grant and revoke privileges
- User status monitoring
- Password expiry management
- Privilege tracking

#### Tablespace Management
- Create and manage tablespaces
- Monitor tablespace usage
- Track datafile locations
- Real-time capacity monitoring

#### Backup & Recovery
- Full, incremental, and archive log backups
- Backup history tracking
- Database restore functionality
- Backup location management

#### Performance Monitoring
- Database status checking
- Real-time performance metrics
- Wait events analysis
- CPU, memory, and disk usage tracking
- Transaction performance monitoring

#### Query Execution
- Execute SQL queries (simulated)
- Query result display
- Error handling and logging

#### Audit & Logging
- Comprehensive audit trail
- Action tracking and logging
- Audit log export
- Metrics export to JSON

## Installation

### Requirements
- Python 3.7+
- Standard library only (no external dependencies for simulation mode)
- Optional: Oracle client libraries for real database connections

### Setup

1. Clone or download the Virtual DBA files:
```bash
virtual_dba.py      # Main DBA module
dba_cli.py         # Interactive CLI interface
dba_demo.py        # Demo and examples
README.md          # This file
```

2. No additional installation required for simulation mode!

## Usage

### Option 1: Interactive CLI Interface (Recommended for Learning)

Start the interactive command-line interface:

```bash
python dba_cli.py
```

This opens an interactive shell where you can type commands:

```
VirtualDBA> help                    # Show all commands
VirtualDBA> test_connection         # Test connection
VirtualDBA> create_user scott tiger # Create user
VirtualDBA> list_users              # List all users
VirtualDBA> backup FULL             # Perform full backup
VirtualDBA> status                  # Get database status
VirtualDBA> quit                    # Exit
```

### Option 2: Run Demo Script

See comprehensive demonstrations of all features:

```bash
python dba_demo.py
```

This runs through:
- Connection management
- User management
- Tablespace operations
- Backup & recovery
- Performance monitoring
- Query execution
- Audit logging
- Advanced scenarios

### Option 3: Programmatic Usage (Python Scripts)

```python
from virtual_dba import VirtualDBA

# Initialize VirtualDBA
dba = VirtualDBA(use_simulation=True)

# Test connection
dba.test_connection()

# Create user
dba.create_user("scott", "tiger", tablespace="USERS", expiry_days=365)

# List users
dba.list_users()

# Create tablespace
dba.create_tablespace("ANALYTICS", 2048, "/u01/oradata/orcl/analytics01.dbf")

# Perform backup
dba.backup_database("FULL", "./backups")

# Get database status
status = dba.get_database_status()

# Monitor performance
metrics = dba.monitor_performance()

# Execute query
results = dba.execute_query("SELECT * FROM employees")

# View audit log
dba.view_audit_log(limit=20)

# Export metrics
dba.export_metrics("dba_report.json")
```

## API Reference

### Connection Management

```python
dba = VirtualDBA(config_file="dba_config.json", use_simulation=True)

# Create configuration
dba.create_config(host, port, username, service_name, password)

# Load configuration
dba.load_config()

# Test connection
dba.test_connection()
```

### User Management

```python
# Create user with 365-day password expiry
dba.create_user(username, password, tablespace="USERS", expiry_days=365)

# Drop user with CASCADE option
dba.drop_user(username, cascade=True)

# List all users
users = dba.list_users()

# Grant privilege
dba.grant_privilege(username, privilege)

# Revoke privilege
dba.revoke_privilege(username, privilege)
```

**Common Privileges:**
- SELECT, INSERT, UPDATE, DELETE (data manipulation)
- CONNECT, RESOURCE (roles)
- CREATE TABLE, CREATE INDEX, CREATE PROCEDURE
- ALTER SYSTEM, ALTER SESSION

### Tablespace Management

```python
# Create tablespace
dba.create_tablespace(name, size_mb, datafile_path)

# List all tablespaces
tablespaces = dba.list_tablespaces()
```

### Backup & Recovery

```python
# Perform backup (types: FULL, INCREMENTAL, ARCHIVE_LOG)
dba.backup_database(backup_type="FULL", backup_location="./backups")

# List backups
backups = dba.list_backups()

# Restore database
dba.restore_database(backup_id)
```

### Performance Monitoring

```python
# Get database status
status = dba.get_database_status()

# Monitor performance metrics
metrics = dba.monitor_performance()

# Get wait events
wait_events = dba.get_wait_events()
```

### Query Execution

```python
# Execute SQL query
results = dba.execute_query("SELECT * FROM table_name")
```

### Audit & Export

```python
# View audit log (last N entries)
audit = dba.view_audit_log(limit=20)

# Export metrics to JSON
dba.export_metrics("dba_metrics.json")
```

## CLI Commands Reference

```
CONNECTION:
  create_config <host> <port> <user> <service>  Create configuration
  load_config                                    Load saved config
  test_connection                                Test DB connection

USER MANAGEMENT:
  create_user <user> <pwd> [tablespace]          Create user
  drop_user <user> [cascade]                     Drop user
  list_users                                     List all users
  grant_privilege <user> <privilege>             Grant privilege
  revoke_privilege <user> <privilege>            Revoke privilege

TABLESPACE:
  create_tablespace <name> <size_mb> <path>      Create tablespace
  list_tablespaces                               List tablespaces

BACKUP & RECOVERY:
  backup [FULL|INCREMENTAL|ARCHIVE] [location]  Perform backup
  list_backups                                   List backups
  restore <backup_id>                            Restore database

MONITORING:
  status                                         Database status
  perf                                           Performance metrics
  wait_events                                    Top wait events

QUERIES:
  query <sql>                                    Execute SQL query

AUDIT & EXPORT:
  audit_log [limit]                              View audit log
  export [filename]                              Export metrics

OTHER:
  help [command]                                 Show help
  quit                                           Exit
```

## Examples

### Example 1: Setting Up a New Database User with Privileges

```bash
VirtualDBA> create_user analyst analytics_pass ANALYTICS
VirtualDBA> grant_privilege analyst SELECT
VirtualDBA> grant_privilege analyst INSERT
VirtualDBA> grant_privilege analyst UPDATE
VirtualDBA> list_users
```

### Example 2: Managing Backups

```bash
VirtualDBA> backup FULL ./backups
VirtualDBA> list_backups
VirtualDBA> restore abc12345
```

### Example 3: Performance Analysis

```bash
VirtualDBA> status
VirtualDBA> perf
VirtualDBA> wait_events
```

### Example 4: Audit Trail

```bash
VirtualDBA> audit_log 30
VirtualDBA> export dba_report.json
```

## Configuration File Format

When you create a configuration, it's saved as `dba_config.json`:

```json
{
  "host": "localhost",
  "port": 1521,
  "username": "admin",
  "service_name": "ORCL",
  "password": "admin123"
}
```

## Simulation Mode vs Real Oracle Connection

### Simulation Mode (Default)
- ✓ No Oracle client installation required
- ✓ No real database connection needed
- ✓ Perfect for learning and testing
- ✓ Simulates all operations
- ✗ Does not connect to real databases

### Real Oracle Connection
Set `use_simulation=False` when initializing:

```python
dba = VirtualDBA(use_simulation=False)
```

Requires:
- Oracle client libraries installed
- Valid database credentials
- Network access to Oracle database

## Audit Log Output

The virtual DBA maintains comprehensive audit logs:

```
timestamp                    action              result   details
2024-02-18T10:30:45.123456  CREATE_USER         SUCCESS  User scott created
2024-02-18T10:31:12.456789  GRANT_PRIVILEGE     SUCCESS  Privilege SELECT granted to scott
2024-02-18T10:32:00.789012  BACKUP_DATABASE     SUCCESS  Full backup completed
```

## Exported Metrics Format

When you export metrics, they're saved in JSON format:

```json
{
  "export_time": "2024-02-18T10:35:00",
  "users": { ... },
  "tablespaces": { ... },
  "backups": [ ... ],
  "audit_log": [ ... ]
}
```

## Use Cases

### 1. DBA Training and Learning
- Learn Oracle database administration concepts
- Practice SQL commands safely
- Understand backup and recovery procedures

### 2. Database Administration Automation
- Automate routine DBA tasks
- Script complex operations
- Monitor performance metrics programmatically

### 3. Development and Testing
- Create test databases with specific configurations
- Simulate database scenarios
- Test backup and recovery procedures

### 4. Performance Monitoring
- Track database performance metrics
- Analyze wait events
- Monitor user activity

### 5. Audit and Compliance
- Maintain audit trails of all operations
- Track user management changes
- Export compliance reports

## Error Handling

The tool includes comprehensive error handling:

```
✗ User scott already exists           # User creation error
✗ Configuration file not found        # Configuration error
✗ Backup backup_id not found          # Backup error
✗ Error executing query: ...          # Query error
```

Errors are logged to the audit trail for troubleshooting.

## Performance Considerations

- Simulation mode has minimal overhead
- Audit logging is lightweight
- JSON export is suitable for moderate datasets
- Scales well for typical DBA operations

## Advanced Features

### Custom Privilege Management
```python
privileges = ["SELECT", "INSERT", "UPDATE", "DELETE"]
for priv in privileges:
    dba.grant_privilege(username, priv)
```

### Bulk Operations
```python
# Create multiple users
for i in range(1, 6):
    dba.create_user(f"user{i}", f"pass{i}", "USERS")
```

### Automated Backups
```python
import schedule
import time

schedule.every().day.at("02:00").do(dba.backup_database, "FULL")

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Troubleshooting

### Connection Issues
- Verify database credentials
- Check network connectivity
- Review configuration file

### User Management
- Ensure usernames are unique
- Check tablespace exists
- Verify privileges are valid

### Backup Issues
- Ensure backup location exists
- Check disk space availability
- Review backup history

## Future Enhancements

Potential additions:
- Real Oracle database integration
- Advanced performance tuning
- Automated SQL generation
- Web-based dashboard
- REST API interface
- Database replication management
- Advanced security features
- Integration with monitoring tools

## Support

For issues or questions:
1. Check the help documentation: `help` command
2. Review the demo script: `python dba_demo.py`
3. Examine audit logs for error details
4. Check configuration settings

## License

This Virtual DBA tool is provided for educational and administrative purposes.

## Version History

- **v1.0** (2024-02-18)
  - Initial release
  - Core DBA functionality
  - Interactive CLI interface
  - Comprehensive demo script
  - Full documentation

---

**Happy Database Administration!** 🗄️✨
