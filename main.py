from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from getpass import getpass

class ConnectX:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument("--incognito")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')

        self.browser = webdriver.Chrome(options=options)

    def auto_send_connection_universities(self, listOfUniversities:list, listOfRules:list = ['ceo', 'software', 'developer']):
        connections_sent = 0

        for u in listOfUniversities:
            for r in listOfRules:
                self.browser.get(f"https://www.linkedin.com/school/{u}/people/?keywords={r}")
                self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                print('Waiting connections to load...')
                sleep(3)
                while True:
                    addBTN = self.browser.find_elements(By.XPATH, "//span[text()='Connect'][ancestor::button[contains(@class, 'artdeco-button') and contains(@class, 'artdeco-button--2') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'ember-view') and contains(@class, 'full-width')]]")
                    if len(addBTN) == 0:
                        break
                    print("Buttons:", len(addBTN))
                    
                    
                    for i, btn in enumerate(addBTN):
                        try:
                            btn.click()
                            sleep(0.2)  # Add a small delay for the "Send now" button to appear
                            send_now_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[aria-label="Send now"]')
                            send_now_btn.click()
                            connections_sent += 1
                            print(f'Connection sent.')
                        except:
                            pass

                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f'Connections sent: {connections_sent}')

    def auto_send_connection_companies(self, listOfCompanies:list = ['taskure', 'mokalmat'], listOfRules:list = ['ceo', 'software', 'front', 'developer']):
        connections_sent = 0


        for u in listOfCompanies:
            for r in listOfRules:
                self.browser.get(f"https://www.linkedin.com/company/{u}/people/?keywords={r}")
                self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                print('Waiting connections to load...')
                sleep(3)
                while True:
                    addBTN = self.browser.find_elements(By.XPATH, "//span[text()='Connect'][ancestor::button[contains(@class, 'artdeco-button') and contains(@class, 'artdeco-button--2') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'ember-view') and contains(@class, 'full-width')]]")
                    if len(addBTN) == 0:
                        break
                    print("Buttons:", len(addBTN))
                    
                    
                    for i, btn in enumerate(addBTN):
                        try:
                            btn.click()
                            sleep(0.2)  # Add a small delay for the "Send now" button to appear
                            send_now_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[aria-label="Send now"]')
                            send_now_btn.click()
                            connections_sent += 1
                            print(f'Connection sent.')
                        except:
                            pass

                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        print(f'Connections sent: {connections_sent}')


    def auto_send_connection_mynetwork(self):
        # while True: #extreme mode !
            self.browser.get('https://www.linkedin.com/mynetwork/')
            while True:
                
                connections_sent = 0
                addBTN = self.browser.find_elements(By.CSS_SELECTOR, '.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view.full-width')
                for i, btn in enumerate(addBTN):
                    if "Connect" in btn.find_element(By.TAG_NAME, 'span').text:
                        try:
                            btn.click()
                            connections_sent += 1
                            print(f'{i} Connection sent.')
                        except:
                            pass

                if (i + 1) % 5 == 0:
                    # Scroll down to load more content
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(3)  # Add a delay to let the page load more content
                else:
                    break  # Exit the loop when no more "Connect" buttons are found

            return f'Total connection requests sent: {connections_sent}'


    def login_and_get_result(self, email, password):
        self.browser.get("https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=cold_join_sign_in")

        emailInput = self.browser.find_element(By.ID, "username")
        emailInput.clear()
        emailInput.send_keys(email)

        passInput = self.browser.find_element(By.ID, "password")
        passInput.clear()
        passInput.send_keys(password)

        self.browser.find_element(By.CLASS_NAME, "login__form_action_container").click()

        try:
            self.browser.find_element(By.ID, "error-for-password")
            return "Can't login to your account. Make sure the login credentials are correct."
        except NoSuchElementException:
            print("Logged in!")

        print('started looking for captcha')
        try:
            self.browser.implicitly_wait(3)
            print('started searching for captcha')
            captcha = self.check_captcha()
            if captcha:
                return captcha
            else:
                raise NoSuchElementException
        except NoSuchElementException as e:
            print('captcha is not required: ', e)
            try:
                return self.check_pin()
            except:
                if "login" in str(self.browser.current_url):
                    self.remove_user_webdriver()
                    return "Can't login to your account. Make sure the login credentials are correct."

    def check_captcha(self):
        # needs to be implemented with flask app ..
        return False

    def check_pin(self):
        WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "input_verification_pin")))
        while True:
            while True:
                try:
                    pin_value = int(input('Enter PIN number (from your email address): '))
                    break
                except ValueError:
                    print('Please enter a valid PIN number')
        
            self.browser.find_element(By.CLASS_NAME, "input_verification_pin").send_keys(pin_value)
            
            print("We did entered: ", pin_value)
            self.browser.find_element(By.XPATH, "//button[@aria-label='Submit pin']").click()
            sleep(5)
            try:
                self.browser.find_element(By.XPATH, "//span[text()=\"The verification code you entered isn't valid. Please check the code and try again.\"]")
                print("The verification code you entered isn't valid. Please check the code and try again.")
            except Exception as e:
                print('PIN is correct')
                break

    def remove_user_webdriver(self):
        self.browser.quit()

linkedinEmail = input('Enter your linkedin email address: ')
linkedinPassword = getpass('Enter your linkedin password: ')

algorithm = ConnectX()
algorithm.login_and_get_result(linkedinEmail, linkedinPassword)

        
while True:
    try:
        universityOrCompany = int(input('Would you like to send connections from companies (pick 1) or universities / schools (pick 2) or suggested from your network (pick 3) ?: '))
        if universityOrCompany <= 3 and universityOrCompany > 0:
            break
        else:
            print ('Please select 1 for a company or 2 for a university')
    except ValueError:
        print ('Please select 1 for a company or 2 for a university: ')
if universityOrCompany == 1: # company
    companies_list = [company.strip() for company in input('Please enter a list of company slugs (you can find them in the page link, as explained in the readme), separated by commas. For example, "Google, Amazon, Taskure": ').split(',')]
    job_rules = [rules.strip() for rules in input('Enter a list of job rules separated by commas, like "frontend, ui, software engineer": ').split(',')]
    algorithm.auto_send_connection_companies(companies_list, job_rules)
elif universityOrCompany == 2: # universities
    universities_list = [university.strip() for university in input('Please enter a list of universities slugs (you can find them in the page link, as explained in the readme), separated by commas. For example, "aucegypt, alexandria-university": ').split(',')]
    job_rules = [rules.strip() for rules in input('Enter a list of job rules separated by commas, like "frontend, ui, software engineer": ').split(',')]
    algorithm.auto_send_connection_universities(universities_list, job_rules)
elif universityOrCompany == 3: # mynetwork
    algorithm.auto_send_connection_mynetwork()

