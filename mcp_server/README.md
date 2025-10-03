# MongoDB MCP Server - HTTP Mode (No Proxy)

## Setup (3 steps)

1. **Create `.env` file:**
   ```powershell
   Copy-Item env-template.txt .env
   ```

2. **Edit `.env` with your MongoDB connection string:**
   ```powershell
   notepad .env
   ```

3. **Start the server (HTTP mode):**
   ```powershell
   docker-compose up -d
   ```
   The server will listen on `http://localhost:3000`.

## Commands

```powershell
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

## How it works

- The container is started with:
  ```
  --transport http --httpHost 0.0.0.0 --httpPort 3000
  ```
- Port `3000` is published and accessible from your host.
- Your client can connect directly using HTTP/SSE transport.

## Client URLs

- iOS Simulator: `http://localhost:3000`
- Android Emulator: `http://10.0.2.2:3000`
- Physical Device: `http://<YOUR_IP>:3000`

## Files

- `docker-compose.yml` - Docker configuration
- `env-template.txt` - Template for your `.env` file
- `.gitignore` - Protects your credentials from being committed

**Note:** Never commit your `.env` file - it contains sensitive credentials.

