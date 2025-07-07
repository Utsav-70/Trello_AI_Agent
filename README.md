# Trello Member Scraper & AI Analyst 🤖

A powerful Python automation tool that scrapes Trello board member data using browser automation and provides AI-powered analysis using Hugging Face models. This tool helps teams understand their Trello board composition, security posture, and user management insights.

## 🌟 Features

- **🔐 Secure Authentication**: Automated login with 2FA support
- **📊 Member Data Extraction**: Scrapes member information from Trello boards
- **🤖 AI-Powered Analysis**: Uses Hugging Face models for intelligent insights
- **📈 Comprehensive Reports**: Generates security, provisioning, and team analysis reports
- **🛡️ Stealth Browser Automation**: Uses Playwright with Firefox for reliable scraping
- **📁 Data Export**: Saves results to CSV and text files
- **🔄 Fallback Mechanisms**: Graceful degradation when AI services are unavailable

## 🏗️ Architecture

```
Trello_agent/
├── main.py                 # Main orchestrator
├── browser_actions.py      # Browser automation & scraping logic
├── trello_agent.py         # AI analysis & reporting
├── requirements.txt        # Dependencies
├── .env                    # Configuration (not in repo)
├── TECHNICAL_DOCUMENTATION.md # Detailed technical guide
└── data/                   # Output directory
    ├── members.csv         # Scraped member data
    └── analysis_results.txt # AI analysis results
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Firefox browser (for Playwright)
- Trello account with board access
- Hugging Face API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Trello_agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install firefox
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

### Configuration

Create a `.env` file with the following variables:

```env
# Trello Credentials
TRELLO_EMAIL=your_email@example.com
TRELLO_PASSWORD=your_password
TRELLO_BOARD_URL=https://trello.com/b/your_board_id

# Hugging Face API
HUGGINGFACE_API_KEY=your_hf_api_key
HF_MODEL_NAME=microsoft/DialoGPT-medium
```

### Usage

Run the main script:

```bash
python main.py
```

The tool will:
1. 🔐 Log into Trello (with 2FA support)
2. 📊 Scrape member data from your board
3. 🤖 Analyze data with AI
4. 📈 Generate comprehensive reports
5. 💾 Save results to `data/` directory

## 📊 Output

### Generated Files

- **`data/members.csv`**: Raw member data in CSV format
- **`data/analysis_results.txt`**: Complete AI analysis and reports

### Sample Output

```
📋 HUGGING FACE AI ANALYSIS RESULTS
==================================================
Team Composition Analysis:
- Total Members: 5
- Active Users: 3
- Inactive Users: 2

Security Recommendations:
- Enable 2FA for all members
- Regular access reviews
- Monitor board permissions

📊 PROVISIONING RECOMMENDATIONS
==================================================
{
  "total_members": 5,
  "recommendations": [
    "Review member access levels",
    "Remove inactive members",
    "Standardize naming conventions"
  ]
}
```

## 🔧 Technical Details

### Browser Automation

- **Engine**: Playwright with Firefox
- **Stealth Mode**: Removes automation indicators
- **Wait Strategy**: Network idle + explicit timeouts
- **Selector Strategy**: Data-testid attributes for reliability

### AI Integration

- **Primary**: Hugging Face Inference API
- **Fallback**: Local model support (optional)
- **Analysis Types**: Team composition, security, user management
- **Model**: Microsoft DialoGPT-medium (configurable)

### Data Processing

- **Format**: JSON → CSV export
- **Validation**: Data quality checks
- **Error Handling**: Graceful degradation
- **Memory Management**: Efficient async operations

## 🛠️ Advanced Usage

### Custom Model Configuration

```python
# In .env file
HF_MODEL_NAME=gpt2  # or any other Hugging Face model
```

### Local Model Usage

Uncomment the local model setup in `trello_agent.py`:

```python
# self.setup_local_model()  # Uncomment for local inference
```

### Custom Analysis Prompts

Modify the analysis prompt in `trello_agent.py`:

```python
prompt = f"""
Your custom analysis prompt here...
Team Member Data: {members_json}
"""
```

## 🔍 Troubleshooting

### Common Issues

1. **Login Failures**
   - Verify credentials in `.env`
   - Check 2FA settings
   - Ensure board access permissions

2. **Browser Issues**
   - Install Firefox: `playwright install firefox`
   - Check firewall settings
   - Verify Playwright installation

3. **AI Analysis Failures**
   - Verify Hugging Face API key
   - Check internet connection
   - Review model availability

4. **No Members Found**
   - Verify board URL
   - Check board permissions
   - Ensure members are visible on board

### Debug Mode

Enable debug output by modifying `browser_actions.py`:

```python
# Set headless=False for visible browser
self.browser = await playwright.firefox.launch(headless=False)
```

## 📚 Documentation

- **Technical Documentation**: See `TECHNICAL_DOCUMENTATION.md` for detailed technical insights
- **Code Comments**: Comprehensive inline documentation
- **Error Messages**: Clear feedback and troubleshooting hints

## 🔒 Security Considerations

- **Credentials**: Never commit `.env` files
- **2FA**: Manual entry required for security compliance
- **Data Privacy**: Local processing, no data sent to external services
- **Access Control**: Respect Trello's terms of service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Playwright**: Browser automation framework
- **Hugging Face**: AI model hosting and inference
- **Trello**: Board management platform
- **Python Community**: Excellent libraries and tools

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review technical documentation
3. Open an issue on GitHub
4. Check Trello's API documentation

---

**Note**: This tool is designed for legitimate team management purposes. Please respect Trello's terms of service and use responsibly. 