# StonkSensei

**Your AI-Powered Stock Market Oracle**

*Harnessing social sentiment and advanced ML to guide your investment decisions.*

## 📖 Inspiration
Traditional stock analysis tools often overlook the power of social sentiment, while retail investors increasingly rely on platforms like Reddit and Twitter for market insights. We built StonkSensei to bridge this gap, combining **quantitative metrics** with **qualitative social sentiment** to democratize data-driven investing. Inspired by the GameStop saga, we wanted to create a tool that decodes "meme stock" hype while maintaining rigorous financial analysis.

## 🚀 What it does

StonkSensei is a next-gen stock analysis platform that:
- **Analyzes sentiment** across Reddit and financial news using FinBERT and FinTwitBERT ML models
- Calculates real-time **"Hype Score"** based on social media engagement
- Generates **risk profiles** using real market data + proprietary volatility algorithms
- Delivers plain-English investment theses via **DeepSeek-7B** LLM
- Flags blacklisted/meme stocks while suggesting whitelisted opportunities

## ⚙️ How we built it
Tech Stack
- Frontend: React/Next.js (TypeScript) + Tailwind CSS
- Backend: FastAPI + Python 3.11 async workers
- ML Pipeline:
  - FinBERT and FinTwitBERT for sentiment analysis
  - Custom hype/risk scoring algorithms
  - DeepSeek-7B for natural language insights
- Data Infrastructure:
  - Web scraping: Selenium + Beautiful Soup
  - Database: MongoDB Atlas
  - Auth: Okta Auth0
- Deployment:
  - AI/ML: Modal for GPU-accelerated inference
  - Frontend: Vercel
  - Backend:

## Challenges we ran into
1. Model Integration Hell: Getting FinBERT/FinTwitBERT to play nicely with real-time sentiment streams
2. Reddit Rate Limits: Overcoming API restrictions with smart Selenium scraping
3. Meme Stock Detection: Separating genuine hype from bot-driven noise
4. Risk Calculation: Blending traditional beta scores with social volatility metrics

## Accomplishments that we're proud of

## What we learned
- Financial NLP requires domain-specific fine-tuning (generic models fail)
- Social sentiment has asymmetric impact – panic sells faster than hype buys
- User experience is king: Traders want insights, not raw data
- Web scraping ethics – when does "public data" become intrusive?
- The power of JIT model loading on Modal's GPU cluster

## What's next for StonkSensei

🚀 Ready for Smarter Investing?
StonkSensei – Where Wall Street Meets Main Street

## Acknowledgements
This project uses the following pre-trained models:

- **FinBERT**: [GitHub](https://github.com/ProsusAI/finBERT) | [MIT License](https://opensource.org/licenses/MIT)
- **FinTwitBERT**: [Hugging Face](https://huggingface.co/StephanAkkerman/FinTwitBERT-sentiment) | [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- **DeepSeek-7B**: [Hugging Face](https://huggingface.co/deepseek-ai/deepseek-llm-7b-chat) | [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)

```
@misc{FinTwitBERT-sentiment,
  author = {Stephan Akkerman, Tim Koornstra},
  title = {FinTwitBERT-sentiment: A Sentiment Classifier for Financial Tweets},
  year = {2023},
  publisher = {Hugging Face},
  howpublished = {\url{https://huggingface.co/StephanAkkerman/FinTwitBERT-sentiment}}
}
```

```
@misc{araci2019finbert,
  author = {Dogu Araci},
  title = {FinBERT: Financial Sentiment Analysis with Pre-trained Language Models},
  year = {2019},
  eprint = {1908.10063},
  archivePrefix = {arXiv},
  primaryClass = {cs.CL},
  doi = {10.48550/arXiv.1908.10063},
  url = {https://arxiv.org/abs/1908.10063}
}
```
