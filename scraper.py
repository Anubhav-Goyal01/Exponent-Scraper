from playwright.sync_api import sync_playwright
import time

def scrape_questions(url):
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
        number_of_questions = questions_elements.count()

        time.sleep(35)
        for i in range(number_of_questions):
            # Navigate to each question's link
            question_element = questions_elements.nth(i)
            question_element.click(force=True)  # Click the link

            page.wait_for_selector('h1[class*="inline align-middle mr-2"]')  # Adjust class selector as needed

            question = page.locator('h1[class*="inline align-middle mr-2"]').inner_text()
            # asked at div[class*=[flex justify-start mt-2] span span
            asked_at = page.locator('div[class*="flex justify-start mt-2"] span span').nth(0).inner_text()

            print(f"Question: {question}\nAsked at: {asked_at}")

            # div that contains all divs
            # class="comment border border-gray-200 rounded-lg mb-3"
            comments = page.locator('div[class*="comment border border-gray-200 rounded-lg mb-3"]')
            number_of_comments = comments.count()
            answers = []
            for j in range(number_of_comments):
                comment = comments.nth(j)
                answer = comment.locator('div[class*="comment-message-chop"]').inner_text()
                answers.append(answer)

            for i, answer in enumerate(answers):
                print(f"Answer {i+1}: {answer}")

            # Go back to the main list (adjust based on the actual navigation needs)
            page.goto(url)
            page.wait_for_selector('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul')

        time.sleep(1000)

# URL of the website to scrape
url = "https://www.tryexponent.com/questions?page=1"

# Call the function and print the questions
scrape_questions(url)