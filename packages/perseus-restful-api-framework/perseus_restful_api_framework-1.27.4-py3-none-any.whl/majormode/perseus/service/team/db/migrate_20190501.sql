ALTER TABLE team_member ADD COLUMN role text;
UPDATE team_member SET role = CASE WHEN is_administrator THEN 'administrator' ELSE 'member' END;
ALTER TABLE team_member ALTER COLUMN role SET NOT NULL;
ALTER TABLE team_member DROP COLUMN is_administrator;
