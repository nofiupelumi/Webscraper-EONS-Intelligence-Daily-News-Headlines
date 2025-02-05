# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# from datetime import datetime

# ###
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# import os

# # Function to send an email with an attachment
# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     # Attach the body text
#     msg.attach(MIMEText(body, 'plain'))

#     # Attach the file
#     with open(attachment_path, 'rb') as attachment:
#         part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#     part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#     msg.attach(part)

#     # Send the email using SMTP_SSL for port 465
#     server = smtplib.SMTP_SSL(smtp_server, smtp_port)
#     server.login(sender_email, smtp_password)
#     server.sendmail(sender_email, receiver_email, msg.as_string())
#     server.quit()


# ###

# # Keyword lists
# risk_keywords = [
#     'Rape', 'rape', 'Kidnapping', 'kidnapping', 'Terrorism', 'terrorism',
#     'Assaults', 'Homicide', 'homicide', 'Cultism', 'cultism',
#     'Piracy', 'piracy', 'Drowning', 'Armed Robbery', 'Fire Outbreak',
#     'Unsafe Route/Violent Attacks', 'Human Trafficking', 'human trafficking',
#     'Crime', 'arrested', 'nabbed', 'paraded', 'detained', 'apprehended', 'arresting',
#     'remanded', 'rescued', 'crime', 'Arrest', 'arrest', 'ambush', 'Ambush',
#     'Bandit', 'bandit', 'accident', 'Accident', 'fraud', 'Fraud', 'corruption',
#     'Corruption', 'Organ Trafficking'
# ]
# life_death_keywords = ['Killed', 'casualties', 'casualty', 'dies', 'death', 'kill']
# state_keywords = [
#     'Abuja', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
#     'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
#     'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi',
#     'Kwara', 'Lagos', 'Nassarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
#     'Plateau', 'Rivers', 'Sokoto', 'FCT', 'Taraba', 'Yobe', 'Zamfara'
# ]
# case_situation_keywords = ['victims', 'victim', 'injured']

# # Chrome options
# chrome_options = Options()
# chrome_options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.83 Safari/537.36"
# )
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.binary_location = "/usr/bin/google-chrome"  # Ensure this is the correct path
# # Optional: Proxy settings
# chrome_options.add_argument("--proxy-server=http://your-proxy-server:port")

# # Initialize WebDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)


# url = 'https://www.ripplesnigeria.com/'

# try:
#     driver.get(url)

#     # Wait for content to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.TAG_NAME, "h2"))
#     )

#     # Scroll to load lazy content
#     for _ in range(5):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(3)

#     # Parse page content with BeautifulSoup
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     posts = soup.find_all('h2')

#     # Extract data
#     data = []
#     for post in posts:
#         title = post.get_text(strip=True)
#         link = post.find_parent('a')['href'] if post.find_parent('a') else None
#         if not link:
#             continue

#         # Visit the article link to extract content
#         driver.get(link)
#         time.sleep(3)  # Allow content to load

#         # Parse article content
#         article_soup = BeautifulSoup(driver.page_source, 'html.parser')
#         content_div = article_soup.find('div', {'id': 'mvp-content-wrap'})  # Adjust selector as needed
#         content = content_div.get_text(strip=True) if content_div else ""

#         # Check for keywords
#         risk_indicator = next((word for word in risk_keywords if word.lower() in content.lower()), 'NO')
#         life_death = next((word for word in life_death_keywords if word.lower() in content.lower()), 'NO')
#         state = next((word for word in state_keywords if word.lower() in content.lower()), 'NO')
#         case_situation = next((word for word in case_situation_keywords if word.lower() in content.lower()), 'NO')

#         # Filter out rows where state is NO
#         if state != 'NO':
#             # Ensure at least one other column has a match
#             if risk_indicator != 'NO' or life_death != 'NO' or case_situation != 'NO':
#                 data.append({
#                     'title': title,
#                     'link': link,
#                     'Risk Indicator': risk_indicator,
#                     'Life/Death': life_death,
#                     'State': state,
#                     'Case Situation': case_situation
#                 })

#     # Save data to CSV
#     if data:
#         df = pd.DataFrame(data)

#         # Save the filtered data to a CSV file with a timestamp to avoid overwriting
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         filename = f'filtered_news_headlines_{timestamp}.csv'
#         df.to_csv(filename, index=False)

#         ####
#         # Email configuration
#         sender_email =os.environ.get('USER_EMAIL')
#         receiver_email = "nofiumoruf17@gmail.com" #"riskcontrolservicesnig@gmail.com"
#         subject = "Ripples Nigeria Daily News Headlines"
#         body = "Please find attached the latest news headlines with categorized information."
#         smtp_server = "smtp.gmail.com"
#         smtp_port = 465  # SSL port for Gmail
#         smtp_password = os.environ.get('USER_PASSWORD')  

#         # Send the email
#         send_email(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, smtp_password)

#         print("Scraping, categorization, and email sent successfully.")

#     else:
#         print("No relevant data found to save.")

# except Exception as e:
#     print(f"Error: {e}")
# finally:
#     driver.quit()

# from playwright.sync_api import sync_playwright
# import pandas as pd
# from datetime import datetime
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# import os

# # Function to send email with attachment
# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject

#         # Attach the body text
#         msg.attach(MIMEText(body, 'plain'))

#         # Attach the file
#         with open(attachment_path, 'rb') as attachment:
#             part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#             part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#             msg.attach(part)

#         # Send the email
#         with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
#             server.login(sender_email, smtp_password)
#             server.send_message(msg)
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

# # Keyword lists
# risk_keywords = [
#     'Rape', 'rape', 'Kidnapping', 'kidnapping', 'Terrorism', 'terrorism',
#     'Assaults', 'Homicide', 'homicide', 'Cultism', 'cultism',
#     'Piracy', 'piracy', 'Drowning', 'Armed Robbery', 'Fire Outbreak',
#     'Unsafe Route/Violent Attacks', 'Human Trafficking', 'human trafficking',
#     'Crime', 'arrested', 'nabbed', 'paraded', 'detained', 'apprehended', 'arresting',
#     'remanded', 'rescued', 'crime', 'Arrest', 'arrest', 'ambush', 'Ambush',
#     'Bandit', 'bandit', 'accident', 'Accident', 'fraud', 'Fraud', 'corruption',
#     'Corruption', 'Organ Trafficking'
# ]
# life_death_keywords = ['Killed', 'casualties', 'casualty', 'dies', 'death', 'kill']
# state_keywords = [
#     'Abuja', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
#     'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
#     'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi',
#     'Kwara', 'Lagos', 'Nassarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
#     'Plateau', 'Rivers', 'Sokoto', 'FCT', 'Taraba', 'Yobe', 'Zamfara'
# ]
# case_situation_keywords = ['victims', 'victim', 'injured']

# # Scraper logic
# def scrape_ripples():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         context = browser.new_context()
#         page = context.new_page()

#         # Visit the website
#         page.goto("https://www.ripplesnigeria.com/")
#         # Wait for network to be idle
#         page.wait_for_load_state("networkidle")
#         # Save a screenshot to see the page state
#         page.screenshot(path="debug_screenshot.png", full_page=True)

#         # Save the page content to check if it loaded
#         with open("debug_page_content.html", "w", encoding="utf-8") as f:
#             f.write(page.content())

#         # page.wait_for_selector("h2")
#         # Increase timeout
#         if page.locator("h2").count() == 0:
#             print("No <h2> tags found on the page.")
#         else:
#             print(f"Found {page.locator('h2').count()} <h2> tags.")

#         page.wait_for_selector("h2", timeout=60000)  # 60 seconds timeout

#         # Scroll down to load all content
#         for _ in range(10):
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             page.wait_for_timeout(3000)

#         # Extract articles
#         articles = page.locator("h2").all()
#         data = []
#         for article in articles:
#             title = article.inner_text()
#             link = article.locator("xpath=..").get_attribute("href")
#             if not link:
#                 continue

#             # Visit article page
#             page.goto(link)
#             page.wait_for_selector("#mvp-content-wrap", timeout=5000)
#             content = page.locator("#mvp-content-wrap").inner_text()

#             # Check for keywords
#             risk_indicator = next((word for word in risk_keywords if word.lower() in content.lower()), 'NO')
#             life_death = next((word for word in life_death_keywords if word.lower() in content.lower()), 'NO')
#             state = next((word for word in state_keywords if word.lower() in content.lower()), 'NO')
#             case_situation = next((word for word in case_situation_keywords if word.lower() in content.lower()), 'NO')

#             if state != 'NO' and (risk_indicator != 'NO' or life_death != 'NO' or case_situation != 'NO'):
#                 data.append({
#                     'title': title,
#                     'link': link,
#                     'Risk Indicator': risk_indicator,
#                     'Life/Death': life_death,
#                     'State': state,
#                     'Case Situation': case_situation
#                 })

#         browser.close()

#         # Save data to CSV
#         if data:
#             df = pd.DataFrame(data)
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             filename = f'filtered_news_headlines_{timestamp}.csv'
#             df.to_csv(filename, index=False)

#             # Email configuration
#             sender_email = os.environ.get('USER_EMAIL')
#             receiver_email = "nofiumoruf17@gmail.com"
#             subject = "Ripples Nigeria Daily News Headlines"
#             body = "Please find attached the latest news headlines with categorized information."
#             smtp_server = "smtp.gmail.com"
#             smtp_port = 465
#             smtp_password = os.environ.get('USER_PASSWORD')

#             # Send the email
#             send_email(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, smtp_password)
#         else:
#             print("No relevant data found.")

# # Run the scraper
# if __name__ == "__main__":
#     scrape_ripples()

import os
import random
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# User-Agent Rotation (Prevents Blocking)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]

# Main News Page URL
MAIN_NEWS_URL = "https://eonsintelligence.com/posts/news-108923456"

# Selenium WebDriver Setup
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Use a unique user-data directory
user_data_dir = os.path.join(os.getcwd(), "selenium_data")
options.add_argument(f"--user-data-dir={user_data_dir}")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Keyword Filtering Lists
risk_keywords = ['Rape', 'rape', 'Kidnapping', 'kidnapping', 'Terrorism', 'terrorism',
    'Assaults', 'Homicide', 'homicide', 'Cultism', 'cultism',
    'Piracy', 'piracy', 'Drowning', 'Armed Robbery', 'Fire Outbreak',
    'Unsafe Route/Violent Attacks', 'Human Trafficking', 'human trafficking',
    'Crime', 'arrested', 'nabbed', 'paraded', 'detained', 'apprehended', 'arresting',
    'remanded', 'rescued', 'crime', 'Arrest', 'arrest', 'ambush', 'Ambush',
    'Bandit', 'bandit', 'accident', 'Accident', 'fraud', 'Fraud', 'corruption',
    'Corruption', 'Organ Trafficking']
life_death_keywords = ['Killed', 'casualty', 'dies', 'death', 'murder']
state_keywords = ['Abuja', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
    'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
    'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi',
    'Kwara', 'Lagos', 'Nassarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
    'Plateau', 'Rivers', 'Sokoto', 'FCT', 'Taraba', 'Yobe', 'Zamfara']
case_situation_keywords = ['victims','victim', 'injured', 'wounded', 'survivors']

def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
    """
    Function to send an email with an attachment.
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    with open(attachment_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
    msg.attach(part)

    # Send the email using SMTP_SSL for port 465
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

def get_article_links():
    """
    Extracts all news article links from the main news page.
    """
    driver.get(MAIN_NEWS_URL)

    # Wait until the news list loads
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "post")))

    # Extract HTML and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all news article links
    articles = soup.find_all("h2", class_="entry-title")
    article_links = []

    for article in articles:
        link_tag = article.find("a")
        if link_tag and "href" in link_tag.attrs:
            article_links.append("https://eonsintelligence.com" + link_tag["href"])

    return article_links

def scrape_article(url):
    """
    Scrapes title, description, and content from a given article URL.
    """
    driver.get(url)

    # Wait until article loads
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Extract HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract Title
    title = soup.find("title").text if soup.find("title") else "No title found"

    # Extract Description
    description = soup.find("meta", {"name": "description"})
    description = description["content"] if description else "No description found"

    # Extract Article Content
    article = soup.find("div", class_="entry-content")
    article_text = article.get_text(separator="\n").strip() if article else "No article content found"

    # Check for keywords
    risk_indicator = next((word for word in risk_keywords if word.lower() in article_text.lower()), 'NO')
    life_death = next((word for word in life_death_keywords if word.lower() in article_text.lower()), 'NO')
    state = next((word for word in state_keywords if word.lower() in article_text.lower()), 'NO')
    case_situation = next((word for word in case_situation_keywords if word.lower() in article_text.lower()), 'NO')

    return {
        "Title": title,
        "Description": description,
        "Content": article_text,
        "Risk Indicator": risk_indicator,
        "Life/Death": life_death,
        "State": state,
        "Case Situation": case_situation,
        "Link": url
    }

# Fetch all article links
article_links = get_article_links()

# Scrape each article
all_articles = []
for link in article_links:
    article_data = scrape_article(link)
    all_articles.append(article_data)
    time.sleep(2)  # Avoid getting blocked

# Save to CSV
if all_articles:
    df = pd.DataFrame(all_articles)

    # Save the filtered data to a CSV file with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'filtered_news_headlines_{timestamp}.csv'
    df.to_csv(filename, index=False)

    # Email configuration
    sender_email = os.environ.get('USER_EMAIL')
    receiver_email = "riskcontrolservicesnig@gmail.com"
    subject = "EONS Intelligence Daily News Headlines"
    body = "Attached are the latest news headlines with categorized risk information."
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL port for Gmail
    smtp_password = os.environ.get('USER_PASSWORD')

    # Send the email
    send_email(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, smtp_password)

    print("✅ Scraping, categorization, and email sent successfully.")
else:
    print("⚠️ No relevant data found.")

driver.quit()
