DELETE FROM [User]
WHERE [User ID]>101;

SELECT *
FROM [Follow];
SELECT COUNT(*)
FROM [Follow]
WHERE [Followed ID]=1 and [Following ID]=1;

INSERT INTO [User]
    ([User ID],[User Name],[Creating Time],[Password])
VALUES
    (103, '1', '2036-04-13 18:55:22', '2'); 