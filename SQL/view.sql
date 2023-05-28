CREATE VIEW follow_view
AS
    SELECT *
    FROM [Follow] INNER JOIN [User] ON [Following ID]=[User ID]

