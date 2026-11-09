# Dozer Remote

Dozer Remote is a browser-based controller for a Windows PC you own.

## Current build: LAN prototype

The Windows host and Chromebook-friendly controller are in `host/`.

### Windows PC setup

1. Download or clone this repository on your Windows 11 PC.
2. Open the `host` folder.
3. Double-click `start.bat`. It creates a Python virtual environment and installs the required packages.
4. Keep the terminal open. It prints a local address and a six-digit pairing code.
5. On another device connected to the **same trusted Wi-Fi/LAN**, open the printed address and enter the code.

### Controls

- Screen preview (refreshes periodically)
- Mouse movement and left/right click
- Text entry
- Basic navigation keys

Move the pointer to the top-left corner to trigger PyAutoGUI's emergency failsafe. Press Ctrl+C in the host terminal to stop the server.

## Important connection limits

This version is **local-network only**. It does not work across different Wi-Fi networks or through a school network that blocks remote-control connections. GitHub Pages hosts static files; it is not a live relay server.

I will not add traffic disguise, filter evasion, hidden persistence, or public unauthenticated access. For cross-network use, a legitimate encrypted relay or VPN must be available and permitted on both networks. Do not expose port 8765 to the public internet or configure router port forwarding.

## Security notes

- Use only on a trusted private network and on a PC you own or are authorized to control.
- The pairing code is printed in the Windows terminal. Keep it private.
- Stop the host when finished.
- This prototype uses HTTP on the local network; do not use it on public Wi-Fi or untrusted networks.
- The pairing code is short-lived only in the sense that it changes each time the host restarts; anyone who obtains it while the host is running may pair. Restart the host if you suspect it was shared.

## GitHub Pages

The static project dashboard is deployed at:

https://owarellano-eng.github.io/dozer_remote/

GitHub Pages does not run the Windows host or relay live screen/input data.
