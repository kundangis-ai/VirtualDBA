"""
Virtual DBA - Demo and Usage Examples
Examples of using Virtual DBA for Oracle database management
"""

from virtual_dba import VirtualDBA
from datetime import datetime


def demo_connection_management():
    """Demonstrate connection management"""
    print("\n" + "="*70)
    print("DEMO 1: CONNECTION MANAGEMENT")
    print("="*70)
    
    # Create VirtualDBA instance
    dba = VirtualDBA(use_simulation=True)
    
    # Create configuration
    print("\n1. Creating database configuration...")
    dba.create_config(
        host="localhost",
        port=1521,
        username="admin",
        service_name="ORCL",
        password="admin123"
    )
    
    # Load configuration
    print("\n2. Loading configuration...")
    dba.load_config()
    
    # Test connection
    print("\n3. Testing connection...")
    dba.test_connection()
    
    return dba


def demo_user_management(dba):
    """Demonstrate user management operations"""
    print("\n" + "="*70)
    print("DEMO 2: USER MANAGEMENT")
    print("="*70)
    
    # Create users
    print("\n1. Creating database users...")
    dba.create_user("scott", "tiger", "USERS", expiry_days=365)
    dba.create_user("analytics_user", "analytics_pwd", "ANALYTICS", expiry_days=90)
    dba.create_user("developer", "dev_pass", "DEVELOPMENT")
    
    # List users
    print("\n2. Listing all users...")
    users = dba.list_users()
    
    # Grant privileges
    print("\n3. Granting privileges...")
    dba.grant_privilege("scott", "SELECT")
    dba.grant_privilege("scott", "INSERT")
    dba.grant_privilege("scott", "UPDATE")
    dba.grant_privilege("scott", "DELETE")
    dba.grant_privilege("analytics_user", "SELECT")
    dba.grant_privilege("developer", "CONNECT")
    dba.grant_privilege("developer", "RESOURCE")
    
    # List users again to see privileges
    print("\n4. Updated user list with privileges...")
    users = dba.list_users()
    
    # Revoke privilege
    print("\n5. Revoking privilege from scott...")
    dba.revoke_privilege("scott", "DELETE")
    
    return dba


def demo_tablespace_management(dba):
    """Demonstrate tablespace management"""
    print("\n" + "="*70)
    print("DEMO 3: TABLESPACE MANAGEMENT")
    print("="*70)
    
    # Create tablespaces
    print("\n1. Creating tablespaces...")
    dba.create_tablespace("USERS", 1024, "/u01/oradata/orcl/users01.dbf")
    dba.create_tablespace("ANALYTICS", 2048, "/u01/oradata/orcl/analytics01.dbf")
    dba.create_tablespace("DEVELOPMENT", 512, "/u01/oradata/orcl/dev01.dbf")
    dba.create_tablespace("TEMP", 256, "/u01/oradata/orcl/temp01.dbf")
    
    # List tablespaces
    print("\n2. Listing all tablespaces...")
    tablespaces = dba.list_tablespaces()
    
    return dba


def demo_backup_recovery(dba):
    """Demonstrate backup and recovery operations"""
    print("\n" + "="*70)
    print("DEMO 4: BACKUP AND RECOVERY")
    print("="*70)
    
    # Perform full backup
    print("\n1. Performing full database backup...")
    dba.backup_database("FULL", "./backups")
    
    # Perform incremental backup
    print("\n2. Performing incremental backup...")
    dba.backup_database("INCREMENTAL", "./backups")
    
    # Perform archive log backup
    print("\n3. Performing archive log backup...")
    dba.backup_database("ARCHIVE_LOG", "./backups")
    
    # List backups
    print("\n4. Listing backup history...")
    backups = dba.list_backups()
    
    # Restore database
    if backups:
        print("\n5. Initiating database restore...")
        backup_id = backups[0]['backup_id']
        dba.restore_database(backup_id)
    
    return dba


def demo_performance_monitoring(dba):
    """Demonstrate performance monitoring"""
    print("\n" + "="*70)
    print("DEMO 5: PERFORMANCE MONITORING")
    print("="*70)
    
    # Get database status
    print("\n1. Getting database status...")
    status = dba.get_database_status()
    
    # Monitor performance
    print("\n2. Monitoring performance metrics...")
    metrics = dba.monitor_performance()
    
    # Get wait events
    print("\n3. Analyzing top wait events...")
    wait_events = dba.get_wait_events()
    
    return dba


def demo_query_execution(dba):
    """Demonstrate query execution"""
    print("\n" + "="*70)
    print("DEMO 6: QUERY EXECUTION")
    print("="*70)
    
    # Execute SELECT query
    print("\n1. Executing SELECT query...")
    results = dba.execute_query("SELECT * FROM employees WHERE salary > 50000")
    
    # Execute another query
    print("\n2. Executing aggregate query...")
    results = dba.execute_query("SELECT department, COUNT(*) as emp_count FROM employees GROUP BY department")
    
    return dba


def demo_audit_logging(dba):
    """Demonstrate audit logging and export"""
    print("\n" + "="*70)
    print("DEMO 7: AUDIT LOGGING AND EXPORT")
    print("="*70)
    
    # View audit log
    print("\n1. Viewing audit log (last 10 entries)...")
    audit = dba.view_audit_log(limit=10)
    
    # Export metrics
    print("\n2. Exporting all metrics to JSON...")
    dba.export_metrics("dba_metrics_export.json")
    
    return dba


def advanced_scenario(dba):
    """Demonstrate an advanced scenario: Setting up analytics environment"""
    print("\n" + "="*70)
    print("ADVANCED SCENARIO: SETTING UP ANALYTICS ENVIRONMENT")
    print("="*70)
    
    # Create dedicated tablespace for analytics
    print("\n1. Creating dedicated analytics tablespace...")
    dba.create_tablespace("ANALYTICS_DATA", 5120, "/u02/oradata/orcl/analytics_data01.dbf")
    
    # Create analytics users
    print("\n2. Creating analytics users...")
    dba.create_user("analytics_admin", "analytics_admin_pwd", "ANALYTICS_DATA", expiry_days=365)
    dba.create_user("analytics_reader", "reader_pwd", "ANALYTICS_DATA", expiry_days=180)
    
    # Grant analytics-specific privileges
    print("\n3. Granting analytics privileges...")
    privileges = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE TABLE", "CREATE INDEX"]
    for priv in privileges:
        dba.grant_privilege("analytics_admin", priv)
    
    dba.grant_privilege("analytics_reader", "SELECT")
    
    # Backup analytics environment
    print("\n4. Backing up analytics environment...")
    dba.backup_database("FULL", "./backups/analytics")
    
    # Get status
    print("\n5. Final status check...")
    dba.get_database_status()
    
    return dba


def run_all_demos():
    """Run all demonstration scenarios"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           VIRTUAL DBA - COMPREHENSIVE DEMO                     ║")
    print("║                                                                ║")
    print("║  This script demonstrates all features of Virtual DBA:        ║")
    print("║  - Connection Management                                      ║")
    print("║  - User Management                                            ║")
    print("║  - Tablespace Management                                      ║")
    print("║  - Backup & Recovery                                          ║")
    print("║  - Performance Monitoring                                     ║")
    print("║  - Query Execution                                            ║")
    print("║  - Audit Logging                                              ║")
    print("║  - Advanced Scenarios                                         ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    try:
        # Run demos
        dba = demo_connection_management()
        demo_user_management(dba)
        demo_tablespace_management(dba)
        demo_backup_recovery(dba)
        demo_performance_monitoring(dba)
        demo_query_execution(dba)
        demo_audit_logging(dba)
        advanced_scenario(dba)
        
        # Final summary
        print("\n" + "="*70)
        print("DEMO SUMMARY")
        print("="*70)
        print(f"\n✓ All demonstrations completed successfully!")
        print(f"\nSummary Statistics:")
        print(f"  Total Users Created: {len(dba.sim_db['users'])}")
        print(f"  Total Tablespaces: {len(dba.sim_db['tablespaces'])}")
        print(f"  Total Backups: {len(dba.sim_db['backups'])}")
        print(f"  Audit Log Entries: {len(dba.audit_log)}")
        print(f"\nMetrics exported to: dba_metrics_export.json")
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n✗ Error during demo execution: {str(e)}")


if __name__ == "__main__":
    run_all_demos()
