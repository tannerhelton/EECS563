const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const mongoose = require("mongoose");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
require("dotenv").config();
const cors = require("cors");
const cookieParser = require("cookie-parser");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.json());
app.use(cookieParser());
app.use(cors());
app.use(express.static("public"));

// Connect to MongoDB
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.error("MongoDB connection error:", err));

// Define User Schema for MongoDB
const userSchema = new mongoose.Schema({
  username: { type: String, unique: true },
  password: String,
});

const User = mongoose.model("User", userSchema);

// Define Message Schema for MongoDB
const messageSchema = new mongoose.Schema({
  username: String,
  message: String,
  timestamp: { type: Date, default: Date.now },
});

const Message = mongoose.model("Message", messageSchema);

// Middleware to check authentication
const authenticateToken = (socket, next) => {
  const token = socket.handshake.query.token;
  if (token == null) return next(new Error("Authentication error"));

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return next(new Error("Authentication error"));
    socket.user = user;
    next();
  });
};

io.use(authenticateToken);

// Socket connection
io.on("connection", (socket) => {
  console.log("A user connected");
  updateOnlineUsers();

  socket.on("disconnect", () => {
    console.log("User disconnected");
    updateOnlineUsers();
  });

  socket.on("join-chat", (username) => {
    socket.user.username = username;
    updateOnlineUsers();
  });

  socket.on("send-message", async (data) => {
    io.emit("receive-message", data);
    const message = new Message({
      username: data.username,
      message: data.message,
    });
    await message.save();
  });

  function updateOnlineUsers() {
    const onlineUsers = Array.from(io.sockets.sockets.values()).map(
      (s) => s.user.username
    );
    io.emit("online-users", onlineUsers);
  }
});

app.post("/register", async (req, res) => {
  try {
    const existingUser = await User.findOne({ username: req.body.username });
    if (existingUser) {
      return res.status(400).send("Username already exists");
    }
    const hashedPassword = await bcrypt.hash(req.body.password, 10);
    const user = new User({
      username: req.body.username,
      password: hashedPassword,
    });
    await user.save();
    const accessToken = jwt.sign(
      { username: user.username },
      process.env.JWT_SECRET
    );
    res.cookie("token", accessToken, { httpOnly: true });
    res.status(201).json({ accessToken });
  } catch (error) {
    console.error(error);
    res.status(500).send("An error occurred");
  }
});

app.post("/login", async (req, res) => {
  try {
    const user = await User.findOne({ username: req.body.username });
    if (user == null) return res.status(400).send("Cannot find user");

    if (await bcrypt.compare(req.body.password, user.password)) {
      const accessToken = jwt.sign(
        { username: user.username },
        process.env.JWT_SECRET
      );
      res.cookie("token", accessToken, { httpOnly: true });
      res.json({ accessToken });
    } else {
      res.send("Not Allowed");
    }
  } catch (error) {
    console.error(error);
    res.status(500).send("An error occurred");
  }
});

app.post("/logout", (req, res) => {
  res.clearCookie("token");
  res.send("Logged out");
});

app.get("/chat-history", async (req, res) => {
  try {
    const messages = await Message.find().sort({ timestamp: 1 }).exec();
    res.json(messages);
  } catch (error) {
    console.error(error);
    res.status(500).send("An error occurred");
  }
});

server.listen(3000, () => {
  console.log("Server is running on port 3000");
});
