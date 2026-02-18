#!/usr/bin/env python3
"""
Virtual DBA - Quick Start Guide
Get started with Virtual DBA in minutes
"""

from virtual_dba import VirtualDBA


def quick_start_tutorial():
    """Interactive quick start tutorial"""
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║         VIRTUAL DBA - QUICK START TUTORIAL                     ║
║                                                                ║
║  This tutorial will walk you through the basic operations     ║
║  You can follow along step by step                            ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Initialize
    print("\n[STEP 1] Initializing Virtual DBA...")
    print("-" * 60)
    dba = VirtualDBA(use_simulation=True)
    
    input("\nPress ENTER to continue...")
    
    # Step 2: Connection
    print("\n[STEP 2] Creating and Testing Connection...")
    print("-" * 60)
    print("Creating configuration for ORCL database...")
    dba.create_config(
        host="localhost",
        port=1521,
        username="sys",
        service_name="ORCL",
        password="oracle123"
    )
    
    print("\nTesting connection...")
    dba.test_connection()
    
    input("\nPress ENTER to continue...")
    
    # Step 3: Create Users
    print("\n[STEP 3] Creating Database Users...")
    print("-" * 60)
    print("Creating three users: scott, analyst, developer")
    
    dba.create_user("scott", "tiger", "USERS", expiry_days=365)
    dba.create_user("analyst", "analyst123", "USERS", expiry_days=180)
    dba.create_user("developer", "dev123", "USERS")
    
    input("\nPress ENTER to continue...")
    
    # Step 4: Manage Privileges
    print("\n[STEP 4] Granting Privileges to Users...")
    print("-" * 60)
    
    print("\nGranting SELECT, INSERT, UPDATE to scott...")
    dba.grant_privilege("scott", "SELECT")
    dba.grant_privilege("scott", "INSERT")
    dba.grant_privilege("scott", "UPDATE")
    
    print("\nGranting SELECT to analyst...")
    dba.grant_privilege("analyst", "SELECT")
    
    print("\nGranting CONNECT and RESOURCE to developer...")
    dba.grant_privilege("developer", "CONNECT")
    dba.grant_privilege("developer", "RESOURCE")
    
    input("\nPress ENTER to continue...")
    
    # Step 5: View Users
    print("\n[STEP 5] Viewing All Users and Their Privileges...")
    print("-" * 60)
    users = dba.list_users()
    
    input("\nPress ENTER to continue...")
    
    # Step 6: Create Tablespaces
    print("\n[STEP 6] Creating Tablespaces...")
    print("-" * 60)
    print("Creating tablespaces: USERS, ANALYTICS, DEVELOPMENT")
    
    dba.create_tablespace("USERS", 1024, "/u01/oradata/orcl/users01.dbf")
    dba.create_tablespace("ANALYTICS", 2048, "/u01/oradata/orcl/analytics01.dbf")
    dba.create_tablespace("DEVELOPMENT", 512, "/u01/oradata/orcl/dev01.dbf")
    
    input("\nPress ENTER to continue...")
    
    # Step 7: View Tablespaces
    print("\n[STEP 7] Viewing All Tablespaces...")
    print("-" * 60)
    tablespaces = dba.list_tablespaces()
    
    input("\nPress ENTER to continue...")
    
    # Step 8: Perform Backup
    print("\n[STEP 8] Performing Database Backups...")
    print("-" * 60)
    print("Performing FULL backup...")
    dba.backup_database("FULL", "./backups")
    
    print("\nPerforming INCREMENTAL backup...")
    dba.backup_database("INCREMENTAL", "./backups")
    
    input("\nPress ENTER to continue...")
    
    # Step 9: View Backups
    print("\n[STEP 9] Viewing Backup History...")
    print("-" * 60)
    backups = dba.list_backups()
    
    input("\nPress ENTER to continue...")
    
    # Step 10: Monitor Database
    print("\n[STEP 10] Monitoring Database...")
    print("-" * 60)
    print("\nDatabase Status:")
    status = dba.get_database_status()
    
    print("\nPerformance Metrics:")
    metrics = dba.monitor_performance()
    
    print("\nTop Wait Events:")
    wait_events = dba.get_wait_events()
    
    input("\nPress ENTER to continue...")
    
    # Step 11: Execute Queries
    print("\n[STEP 11] Executing Queries...")
    print("-" * 60)
    print("Executing sample queries...")
    
    dba.execute_query("SELECT * FROM employees WHERE salary > 50000")
    print()
    dba.execute_query("SELECT department, COUNT(*) FROM employees GROUP BY department")
    
    input("\nPress ENTER to continue...")
    
    # Step 12: View Audit Log
    print("\n[STEP 12] Viewing Audit Log...")
    print("-" * 60)
    print("Last 10 operations:")
    audit = dba.view_audit_log(limit=10)
    
    input("\nPress ENTER to continue...")
    
    # Step 13: Export Metrics
    print("\n[STEP 13] Exporting Metrics...")
    print("-" * 60)
    dba.export_metrics("quickstart_metrics.json")
    
    # Summary
    print("\n[COMPLETED] Quick Start Tutorial Summary")
    print("=" * 60)
    print(f"""
✓ Tutorial Completed Successfully!

What You Learned:
  ✓ Initialized Virtual DBA
  ✓ Created database configuration
  ✓ Created {len(dba.sim_db['users'])} database users
  ✓ Managed user privileges
  ✓ Created {len(dba.sim_db['tablespaces'])} tablespaces
  ✓ Performed {len(dba.sim_db['backups'])} backups
  ✓ Monitored database performance
  ✓ Executed SQL queries
  ✓ Reviewed audit logs
  ✓ Exported metrics

Next Steps:
  1. Try the interactive CLI: python dba_cli.py
  2. Run the full demo: python dba_demo.py
  3. Read the documentation: README_VIRTUAL_DBA.md
  4. Integrate into your own scripts

Questions?
  - Type 'help' in the CLI for all commands
  - Check README_VIRTUAL_DBA.md for detailed documentation
  - Review dba_demo.py for advanced examples

Happy Database Administration! 🗄️✨
""")
    print("=" * 60)


def simple_example():
    """Simple usage example without tutorial"""
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║              VIRTUAL DBA - SIMPLE EXAMPLE                      ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Create DBA instance
    dba = VirtualDBA(use_simulation=True)
    
    # Create and manage a user
    print("\n1. Creating database user...")
    dba.create_user("john", "secure_password", "USERS", expiry_days=365)
    
    # Grant privileges
    print("\n2. Granting privileges...")
    dba.grant_privilege("john", "SELECT")
    dba.grant_privilege("john", "INSERT")
    
    # List users
    print("\n3. Listing users...")
    dba.list_users()
    
    # Create tablespace
    print("\n4. Creating tablespace...")
    dba.create_tablespace("APP_DATA", 1024, "/u01/oradata/orcl/app_data01.dbf")
    
    # Perform backup
    print("\n5. Backing up database...")
    dba.backup_database("FULL", "./backups")
    
    # Monitor database
    print("\n6. Monitoring database...")
    dba.get_database_status()
    
    # Export metrics
    print("\n7. Exporting metrics...")
    dba.export_metrics("example_metrics.json")
    
    print("\n✓ Example completed!")


def interactive_menu():
    """Interactive menu for quick start"""
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║           VIRTUAL DBA - QUICK START LAUNCHER                   ║
╚════════════════════════════════════════════════════════════════╝

Choose an option:

1. Run Interactive Tutorial    (Guided step-by-step walkthrough)
2. Run Simple Example          (Quick demonstration)
3. Exit

    """)
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        quick_start_tutorial()
    elif choice == "2":
        simple_example()
    elif choice == "3":
        print("\nGoodbye!")
    else:
        print("Invalid choice. Please try again.")
        interactive_menu()


if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\nTutorial interrupted by user. Goodbye!")
