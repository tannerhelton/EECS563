const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const mongoose = require("mongoose");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Connect to MongoDB
mongoose.connect("your-mongodb-uri", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Define User Schema for MongoDB
const userSchema = new mongoose.Schema({
  username: String,
  password: String,
});

const User = mongoose.model("User", userSchema);

// Middleware to check authentication
const authenticateToken = (socket, next) => {
  const token = socket.handshake.query.token;
  if (token == null) return next(new Error("Authentication error"));

  jwt.verify(token, "your-secret-key", (err, user) => {
    if (err) return next(new Error("Authentication error"));
    socket.user = user;
    next();
  });
};

io.use(authenticateToken);

// Socket connection
io.on("connection", (socket) => {
  console.log("A user connected");

  // Emit online users
  const onlineUsers = Array.from(io.sockets.sockets.values()).map(
    (s) => s.user.username
  );
  io.emit("online-users", onlineUsers);

  socket.on("disconnect", () => {
    console.log("User disconnected");
    io.emit(
      "online-users",
      onlineUsers.filter((username) => username !== socket.user.username)
    );
  });
});

app.post("/register", async (req, res) => {
  try {
    const hashedPassword = await bcrypt.hash(req.body.password, 10);
    const user = new User({
      username: req.body.username,
      password: hashedPassword,
    });
    await user.save();
    res.status(201).send("User created");
  } catch {
    res.status(500).send();
  }
});

app.post("/login", async (req, res) => {
  const user = await User.findOne({ username: req.body.username });
  if (user == null) return res.status(400).send("Cannot find user");

  if (await bcrypt.compare(req.body.password, user.password)) {
    const accessToken = jwt.sign(
      { username: user.username },
      "your-secret-key"
    );
    res.json({ accessToken });
  } else {
    res.send("Not Allowed");
  }
});

server.listen(3000, () => {
  console.log("Server is running on port 3000");
});
