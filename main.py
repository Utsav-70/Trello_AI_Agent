import asyncio
import os
import json
from dotenv import load_dotenv
from browser_actions import TrelloBrowserActions
from trello_agent import TrelloAgent
import pandas as pd

# Load environment variables
load_dotenv()
# import os
# print("TRELLO_EMAIL:", os.getenv("TRELLO_EMAIL"))
# print("TRELLO_PASSWORD:", os.getenv("TRELLO_PASSWORD"))
# print("TRELLO_BOARD_URL:", os.getenv("TRELLO_BOARD_URL"))
async def main():
    """
    Main orchestrator function that handles the complete workflow:
    1. Scrape Trello member data
    2. Process with AI agent
    3. Generate insights and recommendations
    """
    print("🚀 Starting Trello Automation...")
    
    # Initialize browser actions
    browser = TrelloBrowserActions()
    
    try:
        # Step 1: Scrape member data
        print("📊 Scraping Trello member data...")
        try:
            members_data = await browser.scrape_members()
        except Exception as e:
            print(f"❌ Error during scraping: {str(e)}")
            members_data = []
        
        if not members_data:
            print("❌ No member data found. Please check your Trello board access.")
            return
        
        # Step 2: Save to CSV
        df = pd.DataFrame(members_data)
        os.makedirs('data', exist_ok=True)
        csv_path = 'data/members.csv'
        df.to_csv(csv_path, index=False)
        print(f"💾 Saved {len(members_data)} members to {csv_path}")
        
        # Step 3: Process with AI agent
        print("🤖 Processing data with Hugging Face AI agent...")
        agent = TrelloAgent()
        analysis = await agent.analyze_members(members_data)
        
        # Step 4: Generate additional reports
        print("📊 Generating additional reports...")
        recommendations = agent.generate_provisioning_recommendations(members_data)
        security_report = agent.generate_security_report(members_data)
        
        # Step 5: Display results
        print("\n" + "="*50)
        print("📋 HUGGING FACE AI ANALYSIS RESULTS")
        print("="*50)
        print(analysis)
        
        print("\n" + "="*50)
        print("📊 PROVISIONING RECOMMENDATIONS")
        print("="*50)
        print(json.dumps(recommendations, indent=2))
        
        print("\n" + "="*50)
        print("🔒 SECURITY REPORT")
        print("="*50)
        print(security_report)
        
        # Step 6: Save all results to files
        with open('data/analysis_results.txt', 'w') as f:
            f.write("HUGGING FACE AI ANALYSIS\n")
            f.write("="*50 + "\n")
            f.write(analysis)
            f.write("\n\nPROVISIONING RECOMMENDATIONS\n")
            f.write("="*50 + "\n")
            f.write(json.dumps(recommendations, indent=2))
            f.write("\n\nSECURITY REPORT\n")
            f.write("="*50 + "\n")
            f.write(security_report)
        
        print("\n💾 All analysis results saved to data/analysis_results.txt")
        
    except Exception as e:
        print(f"❌ Error in main execution: {str(e)}")
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())