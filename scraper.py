from playwright.sync_api import sync_playwright
import time
import gspread
from google.oauth2.service_account import Credentials


scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(credentials)

workbook = client.open_by_key("1YqZB6jw8KQXoS8CB5lz7mHAX2AjOQB73SGYj1JfsK_o")
worksheet = workbook.worksheet("Sheet1")


def scrape_questions(url, total_pages):
    with sync_playwright() as p:
        # Start the browser in headless mode
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to the URL
        page.goto(url)

        # Wait for the content to load by waiting for a specific XPath element
        page.wait_for_selector('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul')

        # Extract questions using XPath
        # Adjust XPath based on actual requirement if needed
        questions_elements = page.locator('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul/li/div/div/div[1]/div/div[1]/h3/a')
        questions_elements.nth(0).click(force=True) 
        time.sleep(30)

        for page_number in range(7, total_pages + 1):
            if page_number > 1:
                url = f"https://www.tryexponent.com/questions" + f"?page={page_number}"
                page.goto(url)
                page.wait_for_selector('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul')

            questions_elements = page.locator('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul/li/div/div/div[1]/div/div[1]/h3/a')
            number_of_questions = questions_elements.count()          

            for i in range(number_of_questions):
                try:
                # Navigate to each question's link
                    question_element = questions_elements.nth(i)
                    question_element.click(force=True)  # Click the link
                  
                    page.wait_for_selector('h1[class*="inline align-middle mr-2"]')  # Adjust class selector as needed
                    question_link = page.url
                    print(f"Question Link: {question_link}")
    
                    question = page.locator('h1[class*="inline align-middle mr-2"]').inner_text(timeout=2000)
                    # asked at div[class*=[flex justify-start mt-2] span span
                    asked_at = page.locator('div[class*="flex justify-start mt-2"] span span').nth(0).inner_text(timeout=2000)

                    print(f"Question: {question}\nAsked at: {asked_at}")

                    # div that contains all divs
                    # class="comment border border-gray-200 rounded-lg mb-3"
                    page.wait_for_selector('div[class*="comment border border-gray-200 rounded-lg mb-3"]')  # Adjust class selector as needed
                    comments = page.locator('div[class*="comment border border-gray-200 rounded-lg mb-3"]')
                    print(comments.count())
                    number_of_comments = comments.count()
                    answers = []
                    for j in range(number_of_comments):
                        comment = comments.nth(j)
                        answer = comment.locator('div[class*="comment-message-chop"]').inner_text(timeout=2000)
                        answers.append(answer)

                    data = []
                    data.append(question)
                    data.append(asked_at)
                    data.append(question_link)
                    # append answers 1 by 1
                    for answer in answers:
                        data.append(answer)

                    worksheet.append_row(data)


                    page.goto(url)
                    page.wait_for_selector('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul')
                except Exception as e:
                    print(f"Error: continuing to the next question due to {e}")

                    data = []
                    data.append(question)
                    data.append(asked_at)
                    data.append(question_link)
                    worksheet.append_row(data)

                    page.goto(url)
                    page.wait_for_selector('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul')
                    continue

        time.sleep(5)

# URL of the website to scrape
url = f"https://www.tryexponent.com/questions"
scrape_questions(url, 155)