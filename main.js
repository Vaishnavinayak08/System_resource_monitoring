const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const si = require('systeminformation');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),  // Optional or remove
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    win.loadFile('index.html');

    setInterval(async () => {
        const cpu = await si.currentLoad();
        const memory = await si.mem();
        const disk = await si.fsSize();
        const network = await si.networkStats();

        win.webContents.send('system-stats', {
            cpu_usage: cpu.currentLoad.toFixed(2),
            memory_usage: ((memory.used / memory.total) * 100).toFixed(2),
            disk_usage: disk[0].use.toFixed(2),
            upload_speed: (network[0].tx_sec /1024/ 1024).toFixed(2),
            download_speed: (network[0].rx_sec /1024/ 1024).toFixed(2),
        });
    }, 1000);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
