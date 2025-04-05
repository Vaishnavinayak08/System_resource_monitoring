const { app, BrowserWindow } = require("electron");
const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");
const si = require("systeminformation");

const server = express();
server.use(cors());

server.get("/stats", async (req, res) => {
  try {
    const cpuUsage = await si.currentLoad();
    const memory = await si.mem();
    const disk = await si.fsSize();
    const network = await si.networkStats();

    res.json({
      cpu_usage: cpuUsage.currentLoad.toFixed(2),
      memory_usage: ((memory.used / memory.total) * 100).toFixed(2),
      disk_usage: ((disk[0].used / disk[0].size) * 100).toFixed(2),
      upload_speed: (network[0].tx_sec / 1024 / 1024).toFixed(2), // MB/s
      download_speed: (network[0].rx_sec / 1024 / 1024).toFixed(2), // MB/s
    });
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch system stats" });
  }
});

server.listen(3000, () => console.log("Server running on http://localhost:3000"));

app.whenReady().then(() => {
  const win = new BrowserWindow({
    width: 900,
    height: 700,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  win.loadFile("index.html");
});
