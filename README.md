# 🤖 MongoDB AI Agent with Streamlit

An intelligent chatbot that queries MongoDB databases using natural language, powered by OpenAI and Model Context Protocol (MCP).

## 🌟 Features

- **Natural Language Queries**: Ask questions in plain English instead of writing MongoDB queries
- **Smart Tool Selection**: AI automatically chooses the right MongoDB operations
- **Beautiful Web UI**: Built with Streamlit for an intuitive user experience
- **Real-time Execution**: See queries execute and results update in real-time
- **Multi-step Reasoning**: Handles complex queries that require multiple operations

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- MongoDB database (local or Atlas)
- OpenAI API key
- Docker (for MCP server)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
# MongoDB Configuration
MDB_MCP_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
MDB_MCP_DATABASE=your_database_name

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional
MDB_MCP_READ_ONLY=true
```

### 4. Start MCP Server

```bash
cd mcp_server
docker-compose up
```

### 5. Launch the Streamlit App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📚 Documentation

- **[STREAMLIT_README.md](STREAMLIT_README.md)** - Detailed app documentation
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Comprehensive usage guide with examples
- **[mcp_server/README.md](mcp_server/README.md)** - MCP server setup

## 💡 Example Queries

```
# Basic Operations
"List all collections in the database"
"Count documents in the events collection"
"Show me the first 10 documents from users"

# Time-based Queries
"Show all visitors from the past week"
"Find events created after January 1, 2025"
"Show check-ins from yesterday"

# Advanced Queries
"Show all enterEvents with type 'visitor' in the past month"
"Aggregate events by type and count them"
"Find all documents where status is 'active'"
```

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Streamlit UI       │
│  (app.py)           │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  OpenAI GPT-4       │
│  (Tool Selection)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  MCP Tools          │
│  (MongoDB Ops)      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  MongoDB Database   │
└─────────────────────┘
```

## 📁 Project Structure

```
data-crunching-chatbot/
├── app.py                  # Streamlit web application
├── mcp_agent.py           # CLI version of the agent
├── mcp_connect.py         # Direct MCP connection example
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── dataset/
│   └── questions_answers.json  # Sample queries
├── mcp_server/
│   ├── docker-compose.yml # MCP server configuration
│   └── README.md          # MCP server documentation
├── STREAMLIT_README.md    # App documentation
├── USAGE_GUIDE.md         # User guide
└── README.md              # This file
```

## 🛠️ Available Scripts

### Web Interface (Recommended)
```bash
streamlit run app.py
```

### Command Line Interface
```bash
python mcp_agent.py
```

### Direct MCP Connection
```bash
python mcp_connect.py
```

## 🎯 How It Works

1. **User Input**: Enter a natural language question
2. **AI Processing**: OpenAI GPT-4 analyzes the query
3. **Tool Selection**: AI chooses appropriate MongoDB MCP tools
4. **Query Execution**: Tools are executed against MongoDB
5. **Result Formatting**: Results are displayed in a readable format
6. **Iteration**: If needed, AI can make multiple tool calls

## 🔧 Technologies Used

- **Streamlit** - Web UI framework
- **OpenAI GPT-4** - Language model for query understanding
- **MCP (Model Context Protocol)** - Bridge between AI and MongoDB
- **MongoDB** - Database
- **Python 3.8+** - Backend language

## 📊 Features in Detail

### Smart Query Understanding
- Handles natural language with context
- Understands time expressions ("past week", "yesterday")
- Supports complex filters and aggregations

### Automatic Type Handling
- ObjectIds: `{"$oid": "..."}`
- Dates: `{"$date": "..."}`
- Regular expressions and other MongoDB types

### Error Handling
- Validates environment configuration
- Checks server connectivity
- Provides helpful error messages

### Visual Feedback
- Real-time execution status
- Tool call visualization
- Iteration tracking
- Pretty-printed results

## 🐛 Troubleshooting

### Connection Issues
```bash
# Check MCP server
cd mcp_server
docker-compose ps

# Check MongoDB connection
mongo "your-connection-string"

# Check Streamlit
streamlit --version
```

### Common Errors

**"MongoDB not configured"**
- Ensure `.env` file exists
- Check `MDB_MCP_CONNECTION_STRING` and `MDB_MCP_DATABASE`

**"OpenAI API not configured"**
- Add `OPENAI_API_KEY` to `.env`

**"Cannot connect to MCP server"**
- Ensure MCP server is running on port 3000
- Check `docker-compose ps` output

## 🚀 Future Enhancements

- [ ] Query history and favorites
- [ ] Export results (CSV, JSON, Excel)
- [ ] Visual query builder
- [ ] Multi-database support
- [ ] Custom tool definitions
- [ ] Advanced filtering UI
- [ ] Real-time data streaming
- [ ] Collaborative features

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions:
1. Check the documentation first
2. Review troubleshooting section
3. Open an issue on GitHub

---

**Made with ❤️ using OpenAI, MCP, and Streamlit**