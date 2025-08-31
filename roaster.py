import streamlit as st
import requests
import json
from datetime import datetime
from openai import OpenAI
import re


# Configure OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) # Add this to Streamlit secrets

def extract_username_from_url(github_url):
    """Extract username from various GitHub URL formats"""
    patterns = [
        r'github\.com/([^/]+)/?$',  # https://github.com/username
        r'github\.com/([^/]+)/.*',  # https://github.com/username/anything
    ]
    
    for pattern in patterns:
        match = re.search(pattern, github_url.lower())
        if match:
            return match.group(1)
    
    # If no pattern matches, assume it's just a username
    return github_url.strip().replace('@', '')

def fetch_github_data(username):
    """Fetch GitHub profile and repository data"""
    try:
        # Get profile data
        profile_url = f"https://api.github.com/users/{username}"
        profile_response = requests.get(profile_url)
        
        if profile_response.status_code != 200:
            return None, f"User '{username}' not found on GitHub"
        
        profile_data = profile_response.json()
        
        # Get repositories data
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
        repos_response = requests.get(repos_url)
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        # Filter out private repos and get useful info
        public_repos = []
        for repo in repos_data:
            if not repo.get('private', True):  # Only public repos
                public_repos.append({
                    'name': repo['name'],
                    'description': repo.get('description', ''),
                    'language': repo.get('language', 'Unknown'),
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'is_fork': repo['fork'],
                    'updated_at': repo['updated_at'],
                    'created_at': repo['created_at'],
                    'size': repo['size']  # Repository size in KB
                })
        
        return {
            'profile': {
                'username': profile_data['login'],
                'name': profile_data.get('name', ''),
                'bio': profile_data.get('bio', ''),
                'company': profile_data.get('company', ''),
                'location': profile_data.get('location', ''),
                'blog': profile_data.get('blog', ''),
                'public_repos': profile_data['public_repos'],
                'followers': profile_data['followers'],
                'following': profile_data['following'],
                'created_at': profile_data['created_at'],
                'updated_at': profile_data['updated_at']
            },
            'repositories': public_repos
        }, None
        
    except Exception as e:
        return None, f"Error fetching GitHub data: {str(e)}"

def analyze_github_data(github_data):
    """Generate insights about the GitHub profile for AI analysis"""
    profile = github_data['profile']
    repos = github_data['repositories']
    
    # Calculate statistics
    total_repos = len(repos)
    fork_count = sum(1 for repo in repos if repo['is_fork'])
    original_repos = total_repos - fork_count
    
    # Language analysis
    languages = {}
    for repo in repos:
        lang = repo['language']
        if lang and lang != 'Unknown':
            languages[lang] = languages.get(lang, 0) + 1
    
    # Recent activity analysis
    recent_repos = [repo for repo in repos if repo['updated_at'] > '2024-01-01']
    
    # Repository naming analysis
    generic_names = ['test', 'hello-world', 'my-project', 'untitled', 'new-project', 'temp']
    generic_repo_count = sum(1 for repo in repos if any(generic in repo['name'].lower() for generic in generic_names))
    
    # Empty or minimal repos
    minimal_repos = sum(1 for repo in repos if repo['size'] < 10)  # Less than 10KB
    
    analysis = {
        'total_repos': total_repos,
        'original_repos': original_repos,
        'fork_percentage': (fork_count / max(total_repos, 1)) * 100,
        'top_languages': dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]),
        'recent_activity': len(recent_repos),
        'generic_names': generic_repo_count,
        'minimal_repos': minimal_repos,
        'average_stars': sum(repo['stars'] for repo in repos) / max(total_repos, 1),
        'most_starred': max(repos, key=lambda x: x['stars']) if repos else None,
        'account_age_years': (datetime.now().year - datetime.fromisoformat(profile['created_at'].replace('Z', '+00:00')).year)
    }
    
    return analysis

def generate_roast(github_data, analysis, temperature=0.8):
    """Generate a roast using OpenAI"""
    
    # Prepare data summary for AI
    profile = github_data['profile']
    
    data_summary = f"""
    Profile Analysis:
    - Username: {profile['username']}
    - Bio: "{profile['bio']}"
    - Company: {profile['company']}
    - Account age: {analysis['account_age_years']} years
    - Total repositories: {analysis['total_repos']}
    - Original vs Forks: {analysis['original_repos']} original, {analysis['fork_percentage']:.1f}% forks
    - Top languages: {', '.join([f"{k} ({v} repos)" for k, v in analysis['top_languages'].items()])}
    - Repositories with generic names: {analysis['generic_names']}
    - Minimal/empty repositories: {analysis['minimal_repos']}
    - Average stars per repo: {analysis['average_stars']:.1f}
    - Most starred repo: {analysis['most_starred']['name'] if analysis['most_starred'] else 'None'} ({analysis['most_starred']['stars'] if analysis['most_starred'] else 0} stars)
    - Recent activity (2024): {analysis['recent_activity']} repositories updated
    
    Sample repository names: {', '.join([repo['name'] for repo in github_data['repositories'][:5]])}
    """
    
    # THIS IS WHERE YOU CUSTOMIZE THE GPT INSTRUCTIONS!
    system_prompt = """You are a sharp-eyed GitHub profile analyst who exposes the gap between what developers claim to be and what their code actually shows. Your mission: ruthlessly compare their bio claims against cold, hard repository evidence while highlighting what they're missing from current industry trends.

PRIMARY FOCUS - EXPOSE THE GAPS:

1. BIO vs REALITY AUDIT: example
- "Full-Stack Developer" with only frontend repos? Call it out.
- "Senior Engineer" with beginner-level projects? Roast them.
- "AI/ML Expert" with zero Python or data science repos? Demolish them.
- "DevOps Engineer" with no infrastructure/deployment code? Destroy them.
- Compare years of claimed experience vs actual project sophistication.

2. REPOSITORY QUALITY GAPS:
- Generic naming (test, my-project, hello-world) vs professional standards
- Missing READMEs, documentation, or proper project structure
- Abandoned projects vs claimed "attention to detail"
- Fork-heavy profiles vs claims of "building innovative solutions"
- Compare to current best practices they should know

3. CODING PATTERN SHORTFALLS:
- Language diversity claims vs mono-language reality
- "Polyglot programmer" using only JavaScript for 3 years
- Missing modern frameworks they should know (React, Next.js, TypeScript, etc.)
- No testing, CI/CD, or modern development practices
- Sporadic commits vs "passionate about coding" claims

4. PROFESSIONAL CONSISTENCY FAILURES:
- Junior-level projects from "senior" developers
- Missing industry-standard tools for their claimed role
- No collaboration evidence (all solo projects)
- Technology stack 5 years behind current trends
- Claims about "scalable systems" but only toy projects

CURRENT TRENDS TO CHECK FOR (2024-2025):
- TypeScript adoption vs plain JavaScript
- Modern React (hooks, context) vs class components
- Cloud platforms (AWS, Docker, Kubernetes)
- AI/ML integration in projects
- Modern CSS (Tailwind, CSS Grid) vs legacy approaches
- JAMstack, serverless, micro-services architecture
- Testing frameworks, CI/CD pipelines
- API design (GraphQL, REST best practices)

ROAST EXECUTION:
- Be mercilessly specific about what they're missing
- Compare their "claims" directly to "evidence"
- Point out outdated practices they should have evolved from
- Highlight industry trends they're clearly behind on
- Use their own bio words against them
- End with a brutal but motivating call to action

TONE: Brutally honest tech lead who's tired of inflated resumes. Think "senior developer reviewing a junior's profile who claimed to be senior.

DO THIS: Look for current trends in the field and reference it. Mention thing they need to do better"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please roast this GitHub profile:\n\n{data_summary}"}
            ],
            max_tokens=500,
            temperature=temperature  # Uses the slider value
        )
        
        content = response.choices[0].message.content
        return content.strip() if content is not None else "No response content received from OpenAI."
        
    except Exception as e:
        return f"Error generating roast: {str(e)}"

# Streamlit UI
def main():
    
    st.set_page_config(
        page_title="Roast My Github 🔥",
        page_icon="🔥",
        layout="wide"
    )
    
    st.title("🔥 Roast My Github")
    st.markdown("*Get constructively roasted based on your GitHub profile!*")
    
    col = st.columns(2)

    # Input section
    col[0].markdown("### Enter GitHub Profile")
    github_input = col[0].text_input(
        "GitHub URL or Username:",
        placeholder="https://github.com/username or just 'username'",
        help="Enter a GitHub profile URL or just the username"
    )
    
    # Temperature slider
    temperature = col[0].slider(
        "🌡️ Roast Temperature",
        min_value=0.1,
        max_value=1.0,
        value=0.8,
        step=0.1,
        help="Lower = more focused roasts, Higher = more creative chaos"
    )
    
    roast_button = col[0].button("🔥 ROAST ME!", type="primary")
    
    if roast_button and github_input:
        username = extract_username_from_url(github_input)
        
        if not username:
            col[0].error("Please enter a valid GitHub URL or username")
            return
            
        col[1].markdown(f"### Analyzing GitHub profile for: `{username}`")
        
        # Progress indicator
        progress_bar = col[1].progress(0)
        status_text = col[1].empty()
        
        # Fetch GitHub data
        status_text.text("Fetching GitHub data...")
        progress_bar.progress(25)
        
        github_data, error = fetch_github_data(username)
        
        if error:
            col[1].error(error)
            return
            
        progress_bar.progress(50)
        status_text.text("Analyzing repositories...")
        
        # Analyze data
        analysis = analyze_github_data(github_data)
        
        progress_bar.progress(75)
        status_text.text("Generating roast...")
        
        # Generate roast
        roast = generate_roast(github_data, analysis, temperature)
        
        progress_bar.progress(100)
        status_text.text("Complete!")
        st.markdown("---")
        # Display results
        st.markdown("### 🔥 Your Roast")
        # Create a styled container with the roast content
        roast_html = roast.replace('**', '<strong>').replace('**', '</strong>')
        roast_html = roast_html.replace('*', '<em>').replace('*', '</em>')
        roast_html = roast_html.replace('\n', '<br>')
        
        st.markdown(
            f"""
            <div style="
                background-color: #191970;
                padding: 25px;
                border-radius: 10px;
                border-left: 5px solid #ff4b4b;
                margin: 20px 0;
                font-size: 1.1rem;
                line-height: 1.6;
            ">
                {roast_html}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Show some stats
        with st.expander("📊 Profile Statistics"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Repos", analysis['total_repos'])
                st.metric("Original Repos", analysis['original_repos'])
                
            with col2:
                st.metric("Fork %", f"{analysis['fork_percentage']:.1f}%")
                st.metric("Avg Stars", f"{analysis['average_stars']:.1f}")
                
            with col3:
                st.metric("Account Age", f"{analysis['account_age_years']} years")
                st.metric("Recent Activity", f"{analysis['recent_activity']} repos")
                
            with col4:
                st.metric("Generic Names", analysis['generic_names'])
                st.metric("Minimal Repos", analysis['minimal_repos'])
            
            st.markdown("**Top Languages:**")
            st.write(analysis['top_languages'])
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "*This is all in good fun! The goal is constructive feedback with humor. "
        "Keep coding and improving! 💪*"
    )

if __name__ == "__main__":
    main()