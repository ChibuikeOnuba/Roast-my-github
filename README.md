# 🔥 GitHub Profile Roaster

## This a fun project i built out of boredom. [See tweet here](https://x.com/chibuike_heis/status/1961957547146940601)


A savage but constructive AI-powered tool that analyzes GitHub profiles and delivers witty roasts based on the gap between what developers claim to be and what their code actually shows.

## ✨ Features

- **Bio vs Reality Check**: Exposes mismatches between claimed expertise and actual repositories
- **Repository Quality Analysis**: Roasts generic naming, abandoned projects, and poor documentation
- **Coding Pattern Detection**: Identifies outdated practices and missing industry trends
- **Professional Consistency Audit**: Compares experience claims with project complexity
- **Adjustable Temperature**: Control how savage or gentle the roast is
- **Real-time Statistics**: Shows detailed GitHub profile metrics

## 🎯 What Gets Roasted

- "Senior Full-Stack Developer" with only HTML/CSS repos
- "AI Engineer" with zero Python or data science projects
- Generic repository names like "test", "my-project", "hello-world"
- High fork-to-original repository ratio
- Missing modern technologies (TypeScript, React hooks, serverless, etc.)
- Sporadic commit patterns and abandoned projects
- Inflated bio claims vs actual project sophistication

## 🚀 Live Demo

[Try it here!](https://roast-my-app-hirnkkh2cvoyr4sraxbwre.streamlit.app/)

## 🛠️ Local Setup

### Prerequisites
- Python 3.7+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ChibuikeOnuba/Roast-my-github.git
   cd github-roaster
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud

1. **Push to GitHub** (make sure `.streamlit/` is in `.gitignore`)
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub repo**
4. **Add your OpenAI API key** in Streamlit Cloud Settings → Secrets:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```
5. **Deploy!** 🚀

## 🎛️ Customization

### Adjust Roast Temperature
Use the slider in the app to control creativity:
- **0.1-0.3**: Focused, consistent roasts
- **0.4-0.6**: Balanced creativity
- **0.7-0.9**: Creative and unpredictable
- **1.0**: Maximum chaos mode

### Modify Roast Style
Edit the `system_prompt` in `generate_roast()` function to change:
- Personality (friendly vs savage)
- Focus areas (what to analyze)
- Output format (length, structure)
- Tone and humor style

## 📊 Analysis Metrics

The tool analyzes:
- **Profile Data**: Bio, company, location, follower count
- **Repository Stats**: Total repos, forks vs originals, stars
- **Language Usage**: Diversity and modern framework adoption
- **Activity Patterns**: Commit frequency and recent activity
- **Code Quality**: Naming conventions, documentation, project completion

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Example Output

```
I see you're a "Senior Full-Stack Developer with 5+ years experience" whose most 
complex project is a calculator app from 2022. Your repository screams "tutorial 
graduate" more than "industry veteran." While the world moved to TypeScript and 
serverless architecture, you're still wrestling with vanilla JavaScript and 
wondering why your commits look like a heart monitor during a panic attack.

But hey, at least your repository naming is consistently inconsistent. That takes 
real commitment to chaos.
```

## ⚠️ Important Notes

- **Keep it fun**: This tool is meant for constructive humor, not genuine harassment
- **Rate Limits**: GitHub API allows 60 requests/hour without authentication
- **API Costs**: OpenAI charges per request - monitor your usage
- **Privacy**: Only analyzes public GitHub repositories

## 🛡️ Security

- Never commit your OpenAI API key to version control
- Use environment variables or Streamlit secrets for API keys
- The `.streamlit/` folder is gitignored for security

## 📄 License

MIT License - Feel free to roast responsibly!

## 🐛 Issues & Support

Found a bug or have a suggestion? [Open an issue](https://github.com/ChibuikeOnuba/Roast-my-github/issues)

---

**Disclaimer**: This tool is for entertainment and constructive feedback purposes. All roasts are AI-generated and meant to be taken with humor. Keep coding and improving! 💪