// runs automatically on first container start
db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE || "app_db");

db.createUser({
  user: process.env.MONGO_APP_USERNAME || "app_user",
  pwd:  process.env.MONGO_APP_PASSWORD || "app_pass",
  roles: [
    { role: "readWrite", db: db.getName() }
  ]
});
