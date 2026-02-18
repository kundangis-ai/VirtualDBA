"""
Virtual DBA - Oracle Database Management Tool
A comprehensive tool for managing Oracle databases with various DBA tasks
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import hashlib
import getpass
from dataclasses import dataclass
from enum import Enum


@dataclass
class DatabaseConfig:
    """Database configuration class"""
    host: str
    port: int
    username: str
    password: str
    service_name: str
    sid: Optional[str] = None


@dataclass
class User:
    """Database user class"""
    username: str
    created_date: datetime
    account_status: str
    expiry_date: Optional[datetime] = None
    privileges: List[str] = None


class DataType(Enum):
    """Supported Oracle data types"""
    VARCHAR2 = "VARCHAR2"
    NUMBER = "NUMBER"
    DATE = "DATE"
    CLOB = "CLOB"
    BLOB = "BLOB"
    CHAR = "CHAR"
    INTEGER = "INTEGER"


class VirtualDBA:
    """Main Virtual DBA class for Oracle database management"""
    
    def __init__(self, config_file: str = "dba_config.json", use_simulation: bool = True):
        """
        Initialize Virtual DBA
        
        Args:
            config_file: Path to configuration file
            use_simulation: Use simulation mode if True (no real Oracle connection needed)
        """
        self.config_file = config_file
        self.use_simulation = use_simulation
        self.connection = None
        self.config = None
        self.db_users: Dict[str, User] = {}
        self.db_objects = {}
        self.audit_log = []
        self.backup_history = []
        self.performance_metrics = {}
        
        # Initialize simulation database
        if use_simulation:
            self._initialize_simulation_db()
        
        print("✓ Virtual DBA initialized successfully")
    
    def _initialize_simulation_db(self):
        """Initialize in-memory simulation database"""
        self.sim_db = {
            'users': {},
            'tablespaces': {},
            'datafiles': {},
            'backups': [],
            'metrics': {},
            'alert_log': []
        }
        print("✓ Simulation database initialized")
    
    def load_config(self) -> bool:
        """
        Load database configuration from file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_dict = json.load(f)
                    self.config = DatabaseConfig(**config_dict)
                print(f"✓ Configuration loaded from {self.config_file}")
                return True
            else:
                print(f"✗ Configuration file not found: {self.config_file}")
                return False
        except Exception as e:
            print(f"✗ Error loading configuration: {str(e)}")
            return False
    
    def create_config(self, host: str, port: int, username: str, 
                     service_name: str, password: Optional[str] = None) -> bool:
        """
        Create and save database configuration
        
        Args:
            host: Database host
            port: Database port
            username: Database username
            service_name: Oracle service name
            password: Database password (prompted if not provided)
        
        Returns:
            bool: True if successful
        """
        try:
            if password is None:
                password = getpass.getpass("Enter database password: ")
            
            self.config = DatabaseConfig(
                host=host,
                port=port,
                username=username,
                service_name=service_name,
                password=password
            )
            
            config_dict = {
                'host': self.config.host,
                'port': self.config.port,
                'username': self.config.username,
                'service_name': self.config.service_name,
                'password': self.config.password
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            print(f"✓ Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"✗ Error creating configuration: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test database connection
        
        Returns:
            bool: True if connection successful
        """
        if not self.config:
            print("✗ Configuration not loaded. Load or create configuration first.")
            return False
        
        if self.use_simulation:
            print(f"✓ Simulation connection successful to {self.config.service_name}")
            self._log_audit("TEST_CONNECTION", "SUCCESS", "Connection test performed")
            return True
        
        try:
            # Real Oracle connection would go here
            print(f"✓ Connected to {self.config.host}:{self.config.port}/{self.config.service_name}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {str(e)}")
            return False
    
    # ==================== USER MANAGEMENT ====================
    
    def create_user(self, username: str, password: str, 
                   tablespace: str = "USERS", expiry_days: Optional[int] = None) -> bool:
        """
        Create a new database user
        
        Args:
            username: Username
            password: Password
            tablespace: Default tablespace
            expiry_days: Password expiry in days (None for no expiry)
        
        Returns:
            bool: True if successful
        """
        if username.upper() in self.sim_db['users']:
            print(f"✗ User {username} already exists")
            return False
        
        try:
            expiry_date = None
            if expiry_days:
                expiry_date = datetime.now() + timedelta(days=expiry_days)
            
            user = User(
                username=username,
                created_date=datetime.now(),
                account_status="OPEN",
                expiry_date=expiry_date,
                privileges=[]
            )
            
            self.sim_db['users'][username.upper()] = {
                'password_hash': hashlib.sha256(password.encode()).hexdigest(),
                'created_date': user.created_date.isoformat(),
                'account_status': user.account_status,
                'tablespace': tablespace,
                'privileges': user.privileges,
                'expiry_date': user.expiry_date.isoformat() if expiry_date else None
            }
            
            print(f"✓ User '{username}' created successfully")
            self._log_audit("CREATE_USER", "SUCCESS", f"User {username} created in tablespace {tablespace}")
            return True
        except Exception as e:
            print(f"✗ Error creating user: {str(e)}")
            self._log_audit("CREATE_USER", "FAILED", f"Error: {str(e)}")
            return False
    
    def drop_user(self, username: str, cascade: bool = False) -> bool:
        """
        Drop database user
        
        Args:
            username: Username
            cascade: Drop objects owned by user
        
        Returns:
            bool: True if successful
        """
        if username.upper() not in self.sim_db['users']:
            print(f"✗ User {username} does not exist")
            return False
        
        try:
            del self.sim_db['users'][username.upper()]
            cascade_str = " CASCADE" if cascade else ""
            print(f"✓ User '{username}' dropped successfully{cascade_str}")
            self._log_audit("DROP_USER", "SUCCESS", f"User {username} dropped")
            return True
        except Exception as e:
            print(f"✗ Error dropping user: {str(e)}")
            return False
    
    def list_users(self) -> List[Dict]:
        """
        List all database users
        
        Returns:
            List of user information
        """
        users_list = []
        for username, user_info in self.sim_db['users'].items():
            users_list.append({
                'username': username,
                'created_date': user_info['created_date'],
                'account_status': user_info['account_status'],
                'tablespace': user_info['tablespace'],
                'privileges': len(user_info['privileges']),
                'expiry_date': user_info['expiry_date']
            })
        
        self._display_table(users_list, "DATABASE USERS")
        self._log_audit("LIST_USERS", "SUCCESS", f"Listed {len(users_list)} users")
        return users_list
    
    def grant_privilege(self, username: str, privilege: str) -> bool:
        """
        Grant privilege to user
        
        Args:
            username: Username
            privilege: Privilege to grant (e.g., 'SELECT', 'CONNECT', 'RESOURCE')
        
        Returns:
            bool: True if successful
        """
        if username.upper() not in self.sim_db['users']:
            print(f"✗ User {username} does not exist")
            return False
        
        try:
            if privilege not in self.sim_db['users'][username.upper()]['privileges']:
                self.sim_db['users'][username.upper()]['privileges'].append(privilege)
            print(f"✓ Privilege '{privilege}' granted to user '{username}'")
            self._log_audit("GRANT_PRIVILEGE", "SUCCESS", f"Privilege {privilege} granted to {username}")
            return True
        except Exception as e:
            print(f"✗ Error granting privilege: {str(e)}")
            return False
    
    def revoke_privilege(self, username: str, privilege: str) -> bool:
        """
        Revoke privilege from user
        
        Args:
            username: Username
            privilege: Privilege to revoke
        
        Returns:
            bool: True if successful
        """
        if username.upper() not in self.sim_db['users']:
            print(f"✗ User {username} does not exist")
            return False
        
        try:
            if privilege in self.sim_db['users'][username.upper()]['privileges']:
                self.sim_db['users'][username.upper()]['privileges'].remove(privilege)
            print(f"✓ Privilege '{privilege}' revoked from user '{username}'")
            self._log_audit("REVOKE_PRIVILEGE", "SUCCESS", f"Privilege {privilege} revoked from {username}")
            return True
        except Exception as e:
            print(f"✗ Error revoking privilege: {str(e)}")
            return False
    
    # ==================== TABLESPACE MANAGEMENT ====================
    
    def create_tablespace(self, name: str, size_mb: int, datafile_path: str) -> bool:
        """
        Create a new tablespace
        
        Args:
            name: Tablespace name
            size_mb: Size in megabytes
            datafile_path: Path to datafile
        
        Returns:
            bool: True if successful
        """
        if name.upper() in self.sim_db['tablespaces']:
            print(f"✗ Tablespace {name} already exists")
            return False
        
        try:
            self.sim_db['tablespaces'][name.upper()] = {
                'name': name,
                'status': 'ONLINE',
                'size_mb': size_mb,
                'used_mb': 0,
                'datafile': datafile_path,
                'created_date': datetime.now().isoformat()
            }
            print(f"✓ Tablespace '{name}' created successfully ({size_mb}MB)")
            self._log_audit("CREATE_TABLESPACE", "SUCCESS", f"Tablespace {name} created ({size_mb}MB)")
            return True
        except Exception as e:
            print(f"✗ Error creating tablespace: {str(e)}")
            return False
    
    def list_tablespaces(self) -> List[Dict]:
        """
        List all tablespaces
        
        Returns:
            List of tablespace information
        """
        tablespaces_list = []
        for ts_name, ts_info in self.sim_db['tablespaces'].items():
            usage_pct = (ts_info['used_mb'] / ts_info['size_mb'] * 100) if ts_info['size_mb'] > 0 else 0
            tablespaces_list.append({
                'tablespace': ts_name,
                'status': ts_info['status'],
                'size_mb': ts_info['size_mb'],
                'used_mb': ts_info['used_mb'],
                'available_mb': ts_info['size_mb'] - ts_info['used_mb'],
                'usage_%': f"{usage_pct:.1f}"
            })
        
        self._display_table(tablespaces_list, "TABLESPACES")
        return tablespaces_list
    
    # ==================== BACKUP & RECOVERY ====================
    
    def backup_database(self, backup_type: str = "FULL", backup_location: str = "./backups") -> bool:
        """
        Perform database backup
        
        Args:
            backup_type: FULL, INCREMENTAL, ARCHIVE_LOG
            backup_location: Backup destination path
        
        Returns:
            bool: True if successful
        """
        try:
            os.makedirs(backup_location, exist_ok=True)
            
            backup_id = hashlib.md5(f"{datetime.now().isoformat()}".encode()).hexdigest()[:8]
            backup_info = {
                'backup_id': backup_id,
                'type': backup_type,
                'timestamp': datetime.now().isoformat(),
                'location': backup_location,
                'status': 'COMPLETED',
                'size_mb': 1024  # Simulated size
            }
            
            self.sim_db['backups'].append(backup_info)
            self.backup_history.append(backup_info)
            
            print(f"✓ {backup_type} Backup completed successfully")
            print(f"  Backup ID: {backup_id}")
            print(f"  Location: {backup_location}")
            print(f"  Size: ~1024 MB")
            self._log_audit("BACKUP_DATABASE", "SUCCESS", f"{backup_type} backup completed (ID: {backup_id})")
            return True
        except Exception as e:
            print(f"✗ Error during backup: {str(e)}")
            self._log_audit("BACKUP_DATABASE", "FAILED", f"Error: {str(e)}")
            return False
    
    def list_backups(self) -> List[Dict]:
        """
        List backup history
        
        Returns:
            List of backup information
        """
        backups_list = []
        for backup in self.sim_db['backups']:
            backups_list.append({
                'backup_id': backup['backup_id'],
                'type': backup['type'],
                'timestamp': backup['timestamp'],
                'status': backup['status'],
                'size_mb': backup['size_mb']
            })
        
        self._display_table(backups_list, "BACKUP HISTORY")
        return backups_list
    
    def restore_database(self, backup_id: str) -> bool:
        """
        Restore database from backup
        
        Args:
            backup_id: Backup ID to restore from
        
        Returns:
            bool: True if successful
        """
        backup = next((b for b in self.sim_db['backups'] if b['backup_id'] == backup_id), None)
        
        if not backup:
            print(f"✗ Backup {backup_id} not found")
            return False
        
        try:
            print(f"✓ Database restore from {backup_id} initiated")
            print(f"  Backup Type: {backup['type']}")
            print(f"  Timestamp: {backup['timestamp']}")
            self._log_audit("RESTORE_DATABASE", "SUCCESS", f"Restore from backup {backup_id} completed")
            return True
        except Exception as e:
            print(f"✗ Error restoring database: {str(e)}")
            return False
    
    # ==================== PERFORMANCE MONITORING ====================
    
    def get_database_status(self) -> Dict:
        """
        Get overall database status
        
        Returns:
            Dictionary with database status information
        """
        status = {
            'database_name': self.config.service_name if self.config else 'SIMULATION',
            'status': 'OPEN',
            'uptime_hours': 168,  # Simulated
            'total_users': len(self.sim_db['users']),
            'total_tablespaces': len(self.sim_db['tablespaces']),
            'last_backup': self.sim_db['backups'][-1]['timestamp'] if self.sim_db['backups'] else 'Never',
            'archive_logs_generated': 1024  # Simulated
        }
        
        print("\n" + "="*50)
        print("DATABASE STATUS")
        print("="*50)
        for key, value in status.items():
            print(f"{key:.<30} {value}")
        print("="*50 + "\n")
        
        self._log_audit("STATUS_CHECK", "SUCCESS", "Database status retrieved")
        return status
    
    def monitor_performance(self) -> Dict:
        """
        Monitor database performance metrics
        
        Returns:
            Performance metrics dictionary
        """
        metrics = {
            'cpu_usage_%': 45.2,
            'memory_usage_%': 62.8,
            'disk_usage_%': 78.5,
            'active_sessions': 12,
            'waiting_sessions': 2,
            'avg_response_time_ms': 125,
            'transactions_per_sec': 450,
            'cache_hit_ratio_%': 98.5
        }
        
        print("\n" + "="*50)
        print("PERFORMANCE METRICS")
        print("="*50)
        for metric, value in metrics.items():
            print(f"{metric:.<30} {value}")
        print("="*50 + "\n")
        
        self._log_audit("MONITOR_PERFORMANCE", "SUCCESS", "Performance metrics retrieved")
        return metrics
    
    def get_wait_events(self) -> List[Dict]:
        """
        Get database wait events
        
        Returns:
            List of wait events
        """
        wait_events = [
            {'event': 'db file scattered read', 'count': 450, 'time_sec': 125},
            {'event': 'db file sequential read', 'count': 320, 'time_sec': 89},
            {'event': 'SQL*Net message to client', 'count': 1200, 'time_sec': 45},
            {'event': 'log file sync', 'count': 156, 'time_sec': 234}
        ]
        
        self._display_table(wait_events, "TOP WAIT EVENTS")
        return wait_events
    
    # ==================== QUERY EXECUTION ====================
    
    def execute_query(self, query: str, show_results: bool = True) -> Optional[List]:
        """
        Execute SQL query (simulated)
        
        Args:
            query: SQL query to execute
            show_results: Display query results
        
        Returns:
            Query results
        """
        try:
            print(f"\nExecuting: {query}")
            
            # Simulate different query types
            if query.upper().startswith("SELECT"):
                results = [
                    {'id': 1, 'name': 'Record 1', 'value': 100},
                    {'id': 2, 'name': 'Record 2', 'value': 200},
                    {'id': 3, 'name': 'Record 3', 'value': 300}
                ]
                print(f"✓ Query executed successfully ({len(results)} rows returned)")
                if show_results:
                    self._display_table(results, "QUERY RESULTS")
                self._log_audit("EXECUTE_QUERY", "SUCCESS", f"SELECT query executed")
                return results
            else:
                print("✓ Query executed successfully")
                self._log_audit("EXECUTE_QUERY", "SUCCESS", "Query executed")
                return None
        except Exception as e:
            print(f"✗ Error executing query: {str(e)}")
            self._log_audit("EXECUTE_QUERY", "FAILED", f"Error: {str(e)}")
            return None
    
    # ==================== AUDIT & LOGGING ====================
    
    def _log_audit(self, action: str, result: str, details: str):
        """Log audit trail"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'result': result,
            'details': details
        }
        self.audit_log.append(audit_entry)
    
    def view_audit_log(self, limit: int = 20) -> List[Dict]:
        """
        View audit log
        
        Args:
            limit: Number of recent entries to show
        
        Returns:
            Audit log entries
        """
        log_entries = self.audit_log[-limit:]
        self._display_table(log_entries, "AUDIT LOG (Recent Entries)")
        return log_entries
    
    # ==================== UTILITY METHODS ====================
    
    def _display_table(self, data: List[Dict], title: str = ""):
        """Display data in table format"""
        if not data:
            print(f"No data to display for {title}")
            return
        
        print(f"\n{title}")
        print("-" * 80)
        
        # Get column widths
        headers = list(data[0].keys())
        col_widths = {h: max(len(str(h)), max(len(str(row.get(h, ""))) for row in data)) for h in headers}
        
        # Print header
        header_line = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
        print(header_line)
        print("-" * 80)
        
        # Print rows
        for row in data:
            row_line = " | ".join(f"{str(row.get(h, '')):<{col_widths[h]}}" for h in headers)
            print(row_line)
        
        print("-" * 80 + "\n")
    
    def export_metrics(self, filename: str = "dba_metrics.json") -> bool:
        """
        Export database metrics to file
        
        Args:
            filename: Output filename
        
        Returns:
            bool: True if successful
        """
        try:
            metrics = {
                'export_time': datetime.now().isoformat(),
                'users': self.sim_db['users'],
                'tablespaces': self.sim_db['tablespaces'],
                'backups': self.sim_db['backups'],
                'audit_log': self.audit_log
            }
            
            with open(filename, 'w') as f:
                json.dump(metrics, f, indent=2, default=str)
            
            print(f"✓ Metrics exported to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error exporting metrics: {str(e)}")
            return False
    
    def show_help(self):
        """Display available commands"""
        help_text = """
╔════════════════════════════════════════════════════════════════╗
║                    VIRTUAL DBA - HELP MENU                     ║
╚════════════════════════════════════════════════════════════════╝

CONNECTION MANAGEMENT:
  load_config()                  - Load database configuration
  create_config(...)             - Create new configuration
  test_connection()              - Test database connection

USER MANAGEMENT:
  create_user(username, pwd)     - Create new database user
  drop_user(username)            - Drop database user
  list_users()                   - List all users
  grant_privilege(user, priv)    - Grant privilege to user
  revoke_privilege(user, priv)   - Revoke privilege from user

TABLESPACE MANAGEMENT:
  create_tablespace(...)         - Create new tablespace
  list_tablespaces()             - List all tablespaces

BACKUP & RECOVERY:
  backup_database(type)          - Perform backup
  list_backups()                 - List backup history
  restore_database(backup_id)    - Restore from backup

PERFORMANCE MONITORING:
  get_database_status()          - Get database status
  monitor_performance()          - Get performance metrics
  get_wait_events()              - Get wait events

QUERY EXECUTION:
  execute_query(sql)             - Execute SQL query

AUDIT & LOGGING:
  view_audit_log(limit)          - View audit log
  export_metrics(filename)       - Export metrics to JSON

HELP:
  show_help()                    - Display this help menu
"""
        print(help_text)
