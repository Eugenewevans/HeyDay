-- Migration script to update database schema for Phase 1-7 refactoring
-- Run this in your Neon database console or via psql

-- Step 1: Create new tables
CREATE TABLE IF NOT EXISTS dataset_records (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    data JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS idx_dataset_records_dataset_id ON dataset_records(dataset_id);

CREATE TABLE IF NOT EXISTS dataset_schema (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(100) NOT NULL,
    semantic_role VARCHAR(50),
    is_trigger_candidate BOOLEAN DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_dataset_schema_dataset_id ON dataset_schema(dataset_id);

-- Step 2: Add new columns to automations table
ALTER TABLE automations ADD COLUMN IF NOT EXISTS trigger_column_name VARCHAR(100) DEFAULT 'birthday';
ALTER TABLE automations ADD COLUMN IF NOT EXISTS mode VARCHAR(10) DEFAULT 'preview';

-- Step 3: Modify messages table
-- First, create the new record_id column
ALTER TABLE messages ADD COLUMN IF NOT EXISTS record_id INTEGER;

-- If you have existing data with customer_id, you'll need to handle the migration
-- For now, we'll just make record_id nullable and add the foreign key
-- ALTER TABLE messages ADD CONSTRAINT fk_messages_record_id FOREIGN KEY (record_id) REFERENCES dataset_records(id) ON DELETE CASCADE;

-- Step 4: Update existing automations to have required trigger_column_name
UPDATE automations SET trigger_column_name = 'birthday' WHERE trigger_column_name IS NULL;
UPDATE automations SET mode = 'preview' WHERE mode IS NULL;

-- Make trigger_column_name NOT NULL after setting defaults
ALTER TABLE automations ALTER COLUMN trigger_column_name SET NOT NULL;

-- Step 5: Verify changes
SELECT 'Migration complete!' as status;

