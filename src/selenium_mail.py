from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from retrieve_secrets import RetrieveSecrets
secrets = RetrieveSecrets()

print('Enter the gmailid and password')
gmailId = secrets.EMAIL_SEND_ADDRESS
passWord = secrets.EMAIL_SEND_PASSWORD

try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
    'https%3A%2F%2Fmail.google.com%2Fmail%2F&amp;service=mail&amp;sacu=1&amp;rip=1'+\
    '&amp;flowName=GlifWebSignIn&amp;flowEntry = ServiceLogin')
    driver.implicitly_wait(15)

    loginBox = driver.find_element(By.XPATH,'//*[@id =&quot;identifierId&quot;]')
    loginBox.send_keys(gmailId)

    nextButton = driver.find_elements(By.XPATH,'//*[@id =&quot;identifierNext&quot;]')
    nextButton[0].click()

    passWordBox = driver.find_element(
        By.XPATH,'//*[@id =&quot;password&quot;]/div[1]/div / div[1]/input')
    passWordBox.send_keys(passWord)

    nextButton = driver.find_elements(By.XPATH,'//*[@id =&quot;passwordNext&quot;]')
    nextButton[0].click()

    print('Login Successful...!!')
except:
    print('Login Failed')
