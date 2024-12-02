CREATE OR REPLACE FUNCTION editUserInfo(userID UUID, username TEXT, userBio TEXT)
RETURNS TABLE (changeSuccessful BOOLEAN, errorMessage TEXT) AS $$
DECLARE
    usernameUpdated BOOLEAN := FALSE;
    bioUpdated BOOLEAN := FALSE;
BEGIN
    -- Check and update username
    IF username IS NOT NULL AND TRIM(username) <> '' THEN
        UPDATE "Usuarios Auth"
        SET user_name = username
        WHERE id = userID;

        -- Check if any row was updated
        IF FOUND THEN
            usernameUpdated := TRUE;
        ELSE
            RETURN QUERY VALUES (FALSE, 'User ID not found for username update');
        END IF;
    END IF;

    -- Check and update bio
    IF userBio IS NOT NULL AND TRIM(userBio) <> '' THEN
        UPDATE "Usuarios Auth"
        SET bio = userBio
        WHERE id = userID;

        -- Check if any row was updated
        IF FOUND THEN
            bioUpdated := TRUE;
        ELSE
            RETURN QUERY VALUES (FALSE, 'User ID not found for bio update');
        END IF;
    END IF;

    -- Return success based on updates
    IF usernameUpdated OR bioUpdated THEN
        RETURN QUERY VALUES (TRUE, 'Changes applied successfully');
    ELSE
        RETURN QUERY VALUES (FALSE, 'No valid parameters provided or no changes applied');
    END IF;
END;
$$ LANGUAGE plpgsql;
