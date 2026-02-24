"""
Backup script for SQLite data before migrating to PostgreSQL
Run this script before switching to PostgreSQL
"""
import os
import subprocess
import datetime

def backup_sqlite_data():
    """Create a backup of SQLite data using Django's dumpdata command"""
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"sqlite_backup_{timestamp}.json"
    
    print("=" * 60)
    print("SQLite to PostgreSQL Migration - Data Backup")
    print("=" * 60)
    print(f"\nCreating backup file: {backup_file}")
    
    try:
        # Run dumpdata command
        cmd = [
            'python', 'manage.py', 'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '-e', 'contenttypes',
            '-e', 'auth.Permission',
            '--indent', '4'
        ]
        
        print("\nExecuting backup command...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Write to file
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        
        print(f"\n✓ Backup successful!")
        print(f"✓ Data saved to: {backup_file}")
        print(f"\nBackup contains:")
        
        # Count records
        import json
        with open(backup_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"  - Total records: {len(data)}")
            
            # Count by model
            models = {}
            for item in data:
                model = item.get('model', 'unknown')
                models[model] = models.get(model, 0) + 1
            
            for model, count in sorted(models.items()):
                print(f"  - {model}: {count} record(s)")
        
        print("\n" + "=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print("1. Update your .env file with PostgreSQL credentials")
        print("2. Create the PostgreSQL database")
        print("3. Run: python manage.py migrate")
        print(f"4. Run: python manage.py loaddata {backup_file}")
        print("=" * 60)
        
        return backup_file
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error during backup:")
        print(f"  {e.stderr}")
        return None
    except Exception as e:
        print(f"\n✗ Unexpected error:")
        print(f"  {str(e)}")
        return None

if __name__ == '__main__':
    backup_sqlite_data()
