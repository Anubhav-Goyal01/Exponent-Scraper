from playwright.sync_api import sync_playwright

def scrape_questions(url):
    with sync_playwright() as p:
        # Start the browser in headless mode
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the URL
        page.goto(url)

        # Wait for the content to load by waiting for a specific XPath element
        page.wait_for_selector('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul')

        # Extract questions using XPath
        # Adjust XPath based on actual requirement if needed
        questions_elements = page.locator('xpath=//*[@id="__next"]/div[2]/div/div[3]/div[1]/div[1]/ul/li/div/div/div[1]/div/div[1]/h3/a')

        # Retrieve the text of each question element
        questions = [question.text_content() for question in questions_elements.element_handles()]

        # Close the browser
        browser.close()

        return questions

# URL of the website to scrape
url = "https://www.tryexponent.com/questions?page=1"

# Call the function and print the questions
questions = scrape_questions(url)
for question in questions:
    print(question)
