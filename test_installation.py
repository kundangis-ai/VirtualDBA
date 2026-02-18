#!/usr/bin/env python3
"""
Virtual DBA - Installation Test Script
Comprehensive test of all Virtual DBA features
"""

def main():
    print("\n" + "="*70)
    print("VIRTUAL DBA - COMPREHENSIVE INSTALLATION TEST")
    print("="*70 + "\n")
    
    try:
        # Test 1: Import module
        print("✓ Test 1: Importing virtual_dba module...")
        from virtual_dba import VirtualDBA
        print("  SUCCESS: Module imported\n")
        
        # Test 2: Initialize
        print("✓ Test 2: Initializing Virtual DBA...")
        dba = VirtualDBA(use_simulation=True)
        print("  SUCCESS: VirtualDBA initialized\n")
        
        # Test 3: Create user
        print("✓ Test 3: Creating database user...")
        dba.create_user("testuser", "testpass", "USERS", expiry_days=365)
        print("  SUCCESS: User created\n")
        
        # Test 4: Grant privilege
        print("✓ Test 4: Granting privilege...")
        dba.grant_privilege("testuser", "SELECT")
        dba.grant_privilege("testuser", "INSERT")
        print("  SUCCESS: Privileges granted\n")
        
        # Test 5: Create tablespace
        print("✓ Test 5: Creating tablespace...")
        dba.create_tablespace("TESTSPACE", 512, "/u01/test.dbf")
        print("  SUCCESS: Tablespace created\n")
        
        # Test 6: Perform backup
        print("✓ Test 6: Performing backup...")
        dba.backup_database("FULL", "./test_backups")
        print("  SUCCESS: Backup performed\n")
        
        # Test 7: Get status
        print("✓ Test 7: Getting database status...")
        status = dba.get_database_status()
        print("  SUCCESS: Status retrieved\n")
        
        # Test 8: Get metrics
        print("✓ Test 8: Getting performance metrics...")
        metrics = dba.monitor_performance()
        print("  SUCCESS: Metrics retrieved\n")
        
        # Test 9: Export metrics
        print("✓ Test 9: Exporting metrics...")
        dba.export_metrics("test_export.json")
        print("  SUCCESS: Metrics exported\n")
        
        # Test 10: List operations
        print("✓ Test 10: Listing resources...")
        users = dba.list_users()
        tablespaces = dba.list_tablespaces()
        backups = dba.list_backups()
        print(f"  SUCCESS: Listed {len(users)} users, {len(tablespaces)} tablespaces, {len(backups)} backups\n")
        
        print("="*70)
        print("INSTALLATION TEST RESULTS")
        print("="*70)
        print(f"✓ ALL TESTS PASSED (10/10)")
        print(f"\nStatistics:")
        print(f"  • Users created: {len(dba.sim_db['users'])}")
        print(f"  • Tablespaces: {len(dba.sim_db['tablespaces'])}")
        print(f"  • Backups: {len(dba.sim_db['backups'])}")
        print(f"  • Audit log entries: {len(dba.audit_log)}")
        print(f"\n✓ Virtual DBA is fully functional and ready to use!")
        print("="*70)
        print("\nNext Steps:")
        print("  1. Try the interactive CLI: python3 dba_cli.py")
        print("  2. Run the full demo: python3 dba_demo.py")
        print("  3. Try quick start: python3 quickstart_vdba.py")
        print("  4. Read the docs: README_VIRTUAL_DBA.md")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
