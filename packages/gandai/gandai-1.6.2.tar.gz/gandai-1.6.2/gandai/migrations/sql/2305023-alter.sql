ALTER TABLE checkpoint
DROP CONSTRAINT checkpoint_event_id_fkey,
ADD CONSTRAINT checkpoint_event_id_fkey
FOREIGN KEY (event_id)
REFERENCES event (id)
ON DELETE CASCADE;