"""
Virtual DBA - Interactive CLI Interface
Command-line interface for managing Oracle databases through Virtual DBA
"""

from virtual_dba import VirtualDBA
import cmd
import sys
from typing import Optional


class VirtualDBAShell(cmd.Cmd):
    """Interactive command shell for Virtual DBA"""
    
    intro = """
╔════════════════════════════════════════════════════════════════╗
║                   VIRTUAL DBA - ORACLE MANAGEMENT               ║
║                                                                ║
║  An intelligent tool for managing Oracle databases             ║
║  Type 'help' to see available commands                        ║
║  Type 'quit' to exit                                          ║
╚════════════════════════════════════════════════════════════════╝
"""
    
    prompt = "VirtualDBA> "
    
    def __init__(self):
        super().__init__()
        self.dba = VirtualDBA(use_simulation=True)
        self.dba.test_connection()
        print()
    
    # ==================== CONNECTION MANAGEMENT ====================
    
    def do_create_config(self, arg):
        """Create database configuration: create_config host port username service_name"""
        args = arg.split()
        if len(args) < 4:
            print("Usage: create_config <host> <port> <username> <service_name>")
            return
        
        host, port, username, service_name = args[0], int(args[1]), args[2], args[3]
        self.dba.create_config(host, port, username, service_name)
    
    def do_load_config(self, arg):
        """Load configuration from file"""
        self.dba.load_config()
    
    def do_test_connection(self, arg):
        """Test database connection"""
        self.dba.test_connection()
    
    # ==================== USER MANAGEMENT ====================
    
    def do_create_user(self, arg):
        """Create database user: create_user username password [tablespace]"""
        args = arg.split()
        if len(args) < 2:
            print("Usage: create_user <username> <password> [tablespace]")
            return
        
        username, password = args[0], args[1]
        tablespace = args[2] if len(args) > 2 else "USERS"
        self.dba.create_user(username, password, tablespace)
    
    def do_drop_user(self, arg):
        """Drop database user: drop_user username [cascade]"""
        args = arg.split()
        if not args:
            print("Usage: drop_user <username> [cascade]")
            return
        
        username = args[0]
        cascade = len(args) > 1 and args[1].lower() == 'cascade'
        self.dba.drop_user(username, cascade)
    
    def do_list_users(self, arg):
        """List all database users"""
        self.dba.list_users()
    
    def do_grant_privilege(self, arg):
        """Grant privilege to user: grant_privilege username privilege"""
        args = arg.split(maxsplit=1)
        if len(args) < 2:
            print("Usage: grant_privilege <username> <privilege>")
            print("Common privileges: SELECT, INSERT, UPDATE, DELETE, CONNECT, RESOURCE")
            return
        
        username, privilege = args[0], args[1]
        self.dba.grant_privilege(username, privilege)
    
    def do_revoke_privilege(self, arg):
        """Revoke privilege from user: revoke_privilege username privilege"""
        args = arg.split(maxsplit=1)
        if len(args) < 2:
            print("Usage: revoke_privilege <username> <privilege>")
            return
        
        username, privilege = args[0], args[1]
        self.dba.revoke_privilege(username, privilege)
    
    # ==================== TABLESPACE MANAGEMENT ====================
    
    def do_create_tablespace(self, arg):
        """Create tablespace: create_tablespace name size_mb datafile_path"""
        args = arg.split(maxsplit=2)
        if len(args) < 3:
            print("Usage: create_tablespace <name> <size_mb> <datafile_path>")
            return
        
        name, size_mb, datafile_path = args[0], int(args[1]), args[2]
        self.dba.create_tablespace(name, size_mb, datafile_path)
    
    def do_list_tablespaces(self, arg):
        """List all tablespaces"""
        self.dba.list_tablespaces()
    
    # ==================== BACKUP & RECOVERY ====================
    
    def do_backup(self, arg):
        """Perform backup: backup [FULL|INCREMENTAL|ARCHIVE_LOG] [location]"""
        args = arg.split()
        backup_type = args[0].upper() if args else "FULL"
        location = args[1] if len(args) > 1 else "./backups"
        
        if backup_type not in ["FULL", "INCREMENTAL", "ARCHIVE_LOG"]:
            print("Backup type must be: FULL, INCREMENTAL, or ARCHIVE_LOG")
            return
        
        self.dba.backup_database(backup_type, location)
    
    def do_list_backups(self, arg):
        """List backup history"""
        self.dba.list_backups()
    
    def do_restore(self, arg):
        """Restore from backup: restore backup_id"""
        if not arg:
            print("Usage: restore <backup_id>")
            return
        
        self.dba.restore_database(arg)
    
    # ==================== PERFORMANCE MONITORING ====================
    
    def do_status(self, arg):
        """Get database status"""
        self.dba.get_database_status()
    
    def do_perf(self, arg):
        """Get performance metrics"""
        self.dba.monitor_performance()
    
    def do_wait_events(self, arg):
        """Get top wait events"""
        self.dba.get_wait_events()
    
    # ==================== QUERY EXECUTION ====================
    
    def do_query(self, arg):
        """Execute SQL query: query SELECT * FROM table"""
        if not arg:
            print("Usage: query <SQL_QUERY>")
            return
        
        self.dba.execute_query(arg)
    
    # ==================== AUDIT & LOGGING ====================
    
    def do_audit_log(self, arg):
        """View audit log: audit_log [number_of_entries]"""
        limit = int(arg) if arg else 20
        self.dba.view_audit_log(limit)
    
    def do_export(self, arg):
        """Export metrics to JSON: export [filename]"""
        filename = arg if arg else "dba_metrics.json"
        self.dba.export_metrics(filename)
    
    # ==================== HELP ====================
    
    def do_help(self, arg):
        """Show help for commands"""
        if arg:
            super().do_help(arg)
        else:
            help_text = """
╔════════════════════════════════════════════════════════════════╗
║                   VIRTUAL DBA - COMMANDS                       ║
╚════════════════════════════════════════════════════════════════╝

CONNECTION:
  create_config <host> <port> <user> <service>  - Create configuration
  load_config                                    - Load saved config
  test_connection                                - Test DB connection

USER MANAGEMENT:
  create_user <user> <pwd> [tablespace]          - Create user
  drop_user <user> [cascade]                     - Drop user
  list_users                                     - List all users
  grant_privilege <user> <privilege>             - Grant privilege
  revoke_privilege <user> <privilege>            - Revoke privilege

TABLESPACE:
  create_tablespace <name> <size_mb> <path>      - Create tablespace
  list_tablespaces                               - List tablespaces

BACKUP & RECOVERY:
  backup [FULL|INCREMENTAL|ARCHIVE] [location]  - Perform backup
  list_backups                                   - List backups
  restore <backup_id>                            - Restore database

MONITORING:
  status                                         - Database status
  perf                                           - Performance metrics
  wait_events                                    - Top wait events

QUERIES:
  query <sql>                                    - Execute SQL query

AUDIT & EXPORT:
  audit_log [limit]                              - View audit log
  export [filename]                              - Export metrics

OTHER:
  help [command]                                 - Show this help
  quit                                           - Exit program
"""
            print(help_text)
    
    def do_quit(self, arg):
        """Exit Virtual DBA"""
        print("\n✓ Thank you for using Virtual DBA. Goodbye!")
        return True
    
    def do_exit(self, arg):
        """Exit Virtual DBA"""
        return self.do_quit(arg)
    
    def emptyline(self):
        """Override default behavior for empty line"""
        pass
    
    def default(self, line):
        """Override default behavior for unrecognized commands"""
        print(f"✗ Unknown command: '{line}'. Type 'help' for available commands.")


def main():
    """Main entry point"""
    try:
        shell = VirtualDBAShell()
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\n\n✓ Virtual DBA terminated by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
