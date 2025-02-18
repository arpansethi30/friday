import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
from typing import Dict, List, Any, Optional
import json
import os
import requests
from selenium.webdriver.chrome.options import Options

class WebAssistant:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('FRIDAY.WebAssistant')
        self.driver = None
        self._setup_browser()

    def _setup_browser(self):
        """Setup selenium webdriver with automatic ChromeDriver installation"""
        try:
            options = Options()
            if not hasattr(self.config, 'DEBUG') or not self.config.DEBUG:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.logger.info("Browser setup completed successfully")
        except Exception as e:
            self.logger.error(f"Error setting up browser: {e}")
            raise

    def search_and_summarize(self, query: str) -> Dict[str, Any]:
        """Search Google and summarize results"""
        try:
            self.driver.get(f"https://www.google.com/search?q={query}")
            
            # Wait for results
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Get search results
            results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            summarized_results = []
            for result in results[:5]:  # First 5 results
                try:
                    title = result.find_element(By.CSS_SELECTOR, "h3").text
                    link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    snippet = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                    summarized_results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
                except:
                    continue
            
            return {
                "query": query,
                "results": summarized_results,
                "summary": self._generate_summary(summarized_results)
            }
        except Exception as e:
            self.logger.error(f"Error searching: {e}")
            return {"error": str(e)}

    def compose_email_in_browser(self, email_data: Dict[str, Any]) -> bool:
        """Open email client and compose email"""
        try:
            # Open Gmail
            self.driver.get("https://mail.google.com")
            
            # Wait for and click compose button
            compose_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][gh='cm']"))
            )
            compose_btn.click()
            
            # Fill email fields
            self._fill_email_field("to", email_data['to'])
            self._fill_email_field("subject", email_data['subject'])
            self._fill_email_field("body", email_data['body'])
            
            return True
        except Exception as e:
            self.logger.error(f"Error composing email in browser: {e}")
            return False

    def _fill_email_field(self, field: str, value: str):
        """Fill email field in Gmail"""
        selectors = {
            "to": "textarea[name='to']",
            "subject": "input[name='subjectbox']",
            "body": "div[role='textbox']"
        }
        
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selectors[field]))
        )
        element.send_keys(value)

    def _generate_summary(self, results: List[Dict[str, str]]) -> str:
        """Generate a summary of search results"""
        summary = "Here's what I found:\n\n"
        for i, result in enumerate(results, 1):
            summary += f"{i}. {result['title']}\n"
            summary += f"   {result['snippet']}\n\n"
        return summary

    def __del__(self):
        """Cleanup browser when object is destroyed"""
        try:
            self.driver.quit()
        except:
            pass
