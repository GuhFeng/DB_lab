CREATE PROCEDURE get_password
    @uid INT
AS
BEGIN
    SELECT [Password]
    FROM [User]
    WHERE [User ID]=@uid
END;