import asyncio
from playwright.async_api import async_playwright
import os
import time
import csv
from typing import List, Dict, Optional

class TrelloBrowserActions:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.email = os.getenv('TRELLO_EMAIL')
        self.password = os.getenv('TRELLO_PASSWORD')
        self.board_url = os.getenv('TRELLO_BOARD_URL')
        
        if not self.email or not self.password:
            raise ValueError("Please set TRELLO_EMAIL and TRELLO_PASSWORD in your .env file")
        
        if not self.board_url:
            raise ValueError("Please set TRELLO_BOARD_URL in your .env file")
    
    async def setup_browser(self):
        """Initialize browser with stealth settings"""
        print("🌐 Setting up browser...")
        playwright = await async_playwright().start()
        
        # Launch browser with stealth settings
        self.browser = await playwright.firefox.launch(
            headless=False
        )
        
        # Create context with realistic settings
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = await self.context.new_page()
        
        # Add stealth scripts
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
    
    async def login_to_trello(self) -> bool:
        """Login to Trello with email and password"""
        try:
            print("🔐 Logging into Trello...")
            
            # Navigate to Trello login page
            await self.page.goto('https://trello.com/login', wait_until='networkidle')
            await self.page.wait_for_timeout(2000)
            
            # Enter email
            email_input = await self.page.wait_for_selector('[data-testid="username"]', timeout=30000)
            await email_input.fill(self.email)
            
            # Click continue
            await self.page.click('#login-submit')
            await self.page.wait_for_timeout(2000)
            
            # Enter password
            password_input = await self.page.wait_for_selector('#password', timeout=30000)
            await password_input.fill(self.password)
            
            # Submit login
            await self.page.click('#login-submit')
            await self.page.wait_for_timeout(3000)

            # Always pause for manual 2FA/verification
            print("\nIf you see a 2FA/verification code prompt in the browser, please enter the code now.")
            print("When you have completed any verification, press Enter here to continue...")
            input()

            # Wait for login to complete
            try:
                await self.page.wait_for_selector('[data-testid="header-member-menu-button"]', timeout=10000)
                print("✅ Successfully logged into Trello!")
                return True
            except:
                print("❌ Login failed - unknown error")
                return False
                    
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    async def navigate_to_team_board(self) -> bool:
        """Navigate to the specific Trello board"""
        try:
            print(f"📋 Navigating to board: {self.board_url}")
            
            # Navigate directly to the specified board URL
            await self.page.goto(self.board_url, wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            # Check if we successfully loaded the board
            try:
                # Wait for board content to load
                await self.page.wait_for_selector('[data-testid="board-name-display"]', timeout=10000)
                print("✅ Successfully navigated to board!")
                return True
            except:
                # Alternative check - look for board header
                try:
                    await self.page.wait_for_selector('.board-header', timeout=5000)
                    print("✅ Successfully navigated to board!")
                    return True
                except:
                    print("❌ Could not access board. Please check:")
                    print("1. Board URL is correct")
                    print("2. You have access to this board")
                    print("3. Board is not private/restricted")
                    return False
            
        except Exception as e:
            print(f"❌ Navigation error: {str(e)}")
            return False
    
    async def scrape_members(self) -> List[Dict]:
        """Scrape member data from Trello board"""
        await self.setup_browser()
        
        if not await self.login_to_trello():
            return []
        
        if not await self.navigate_to_team_board():
            return []
        
        try:
            print("👥 Scraping member data...")
            
            # Wait for the board to fully load
            await self.page.wait_for_timeout(3000)
            
            # Use the selector for facepile members
            facepile_members = await self.page.locator('[data-testid="board-facepile-member"]').all()
            print(f"🔍 Found {len(facepile_members)} facepile member(s) on the board")

            members = []
            for member_elem in facepile_members:
                try:
                    title = await member_elem.get_attribute('title')
                    if title:
                        if '(' in title and ')' in title:
                            name = title.split('(')[0].strip()
                            username = title.split('(')[1].split(')')[0].strip()
                        else:
                            name = title.strip()
                            username = "Unknown"
                        members.append({
                            'name': name,
                            'username': username,
                            'email': 'Not available in free tier',
                            'role': 'Member',
                            'last_login': 'Not available in free tier'
                        })
                        print(f"✅ Found member: {name} ({username})")
                except Exception as e:
                    print(f"⚠️ Error extracting member data: {str(e)}")
                    continue

            if not members:
                print("⚠️ No members found. This might be due to:")
                print("1. Free tier limitations")
                print("2. Board permissions")
                print("3. UI changes in Trello")
                # Fallback: At least get current user info
                try:
                    user_menu = await self.page.locator('[data-testid="header-member-menu-button"]').first
                    if user_menu:
                        members.append({
                            'name': 'Current User',
                            'username': 'current_user',
                            'email': self.email,
                            'role': 'Admin',
                            'last_login': 'Currently active'
                        })
                except:
                    pass
            print(f"✅ Found {len(members)} members")
            return members
            
        except Exception as e:
            print(f"❌ Scraping error: {str(e)}")
            return []
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
            print("�� Browser closed")
