DELETE FROM [User]
WHERE [User ID]>101;


SELECT *
FROM [Follow] INNER JOIN [User] ON [Following ID]=[User ID]
SELECT *
FROM [Follow];

SELECT *
FROM [follow_view];

EXEC get_password @uid=1;

SELECT [Password]
FROM [User]
WHERE [User ID]=1;

SELECT COUNT(*)
FROM [Follow]
WHERE [Followed ID]=1 and [Following ID]=1;

INSERT INTO [User]
    ([User ID],[User Name],[Creating Time],[Password])
VALUES
    (103, '1', '2036-04-13 18:55:22', '2');

SELECT *
from [Post Content];