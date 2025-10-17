"""
Database migration utilities
"""
from sqlalchemy import text
from app.db.session import engine


def run_migrations():
    """
    Run database migrations to update schema.
    This should be idempotent - safe to run multiple times.
    """
    migrations = [
        # Create dataset_records table
        """
        CREATE TABLE IF NOT EXISTS dataset_records (
            id SERIAL PRIMARY KEY,
            dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
            data JSONB NOT NULL DEFAULT '{}'::jsonb
        );
        """,
        "CREATE INDEX IF NOT EXISTS idx_dataset_records_dataset_id ON dataset_records(dataset_id);",
        
        # Create dataset_schema table
        """
        CREATE TABLE IF NOT EXISTS dataset_schema (
            id SERIAL PRIMARY KEY,
            dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
            column_name VARCHAR(100) NOT NULL,
            semantic_role VARCHAR(50),
            is_trigger_candidate BOOLEAN DEFAULT FALSE
        );
        """,
        "CREATE INDEX IF NOT EXISTS idx_dataset_schema_dataset_id ON dataset_schema(dataset_id);",
        
        # Add new columns to automations
        "ALTER TABLE automations ADD COLUMN IF NOT EXISTS trigger_column_name VARCHAR(100);",
        "ALTER TABLE automations ADD COLUMN IF NOT EXISTS mode VARCHAR(10) DEFAULT 'preview';",
        
        # Update existing automations with defaults
        "UPDATE automations SET trigger_column_name = 'birthday' WHERE trigger_column_name IS NULL;",
        "UPDATE automations SET mode = 'preview' WHERE mode IS NULL;",
        
        # Add new column to messages
        "ALTER TABLE messages ADD COLUMN IF NOT EXISTS record_id INTEGER;",
        
        # For PostgreSQL: make trigger_column_name NOT NULL if it exists
        """
        DO $$ 
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'automations' AND column_name = 'trigger_column_name'
            ) THEN
                ALTER TABLE automations ALTER COLUMN trigger_column_name SET NOT NULL;
            END IF;
        END $$;
        """,
    ]
    
    with engine.begin() as conn:
        for migration in migrations:
            try:
                conn.execute(text(migration))
                print(f"✓ Executed migration")
            except Exception as e:
                print(f"✗ Migration failed (may be already applied): {str(e)[:100]}")
    
    print("✓ All migrations completed")


if __name__ == "__main__":
    run_migrations()

