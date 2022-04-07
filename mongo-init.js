db.createUser(
        {
            user: "kani",
            pwd: "123456",
            roles: [
                {
                    role: "readWrite",
                    db: "test"
                }
            ]
        }
);