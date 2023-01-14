import os, time
from furl import furl
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# Chrome Driver
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=chrome-data") # cookies
driver = webdriver.Chrome(options=options)


# Auth
# EMAIL = "micropower238@gmail.com"
# PASSWORD = os.environ["PASS"]

# driver.find_element(By.ID, "email").send_keys(EMAIL)
# driver.find_element(By.ID, "pass").send_keys(PASSWORD)
# driver.find_element(By.XPATH, "//button[@name='login']").click()

domain = "https://www.facebook.com"
IsPersonalAccount = True
wantSelfUploadedPhoto = True
photoType = "_by" if wantSelfUploadedPhoto else "_of"
targetUserID = "nawphaw.ehhtar.3"
userPhotosPath = f"/{targetUserID}/photos" + photoType if IsPersonalAccount else ""
programReactedImages = 0
countedReactedImages = 0
current_save_fbid = "2068874536627236"


def getCurrentPhotoId(URL):

  if IsPersonalAccount:
    return furl(URL).query.params['fbid']
  else:
    # the last path of the url is image id
    return furl(URL).path.segments[-1]


print(f"[target]\t{targetUserID}")

# nevigate to the target user photos path
driver.get(f"{domain}{userPhotosPath}")
print(f"[goto  ]\t{driver.current_url}")


if driver.current_url == f"{domain}{userPhotosPath}":

  try:


    # find first photo from all photos of target user
    if IsPersonalAccount:
      imgElement = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH,
          f"//a[contains(@href, '{domain}/photo.php?')]"))
      )
    else:
      imgElement = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH,
          f"//a[contains(@href, '{userPhotosPath}')]//img//ancestor::a"))
      )
    # xpath details 
    #    * https://www.guru99.com/xpath-selenium.html  (contains)
    #    * https://www.youtube.com/watch?v=aAWvwGFkySI (ancestor,descendant)

    imgElement.click()
    print(f"[click ]\t{imgElement.get_attribute('href')}")

    time.sleep(3) # delay

    firstPhotoId = getCurrentPhotoId(driver.current_url)
    firstTime = True


    while (firstPhotoId != getCurrentPhotoId(driver.current_url)) or firstTime:

      if firstTime:
        firstTime = False

      try:
        # check internet connection stuff
        ButtonsFrameElement = WebDriverWait(driver, 20).until(
              EC.presence_of_element_located((By.XPATH,
              "//div[@class=' x3dsekl x1uuop16']"
              ))
        )
      except TimeoutException:
        print("Bad Internet Connection or Cannot Locate Buttons Frame")
        exit()

      currentPhotoId = getCurrentPhotoId(driver.current_url)     

      # find like button and check already liked or not
      already_liked = False

      try:
        # 1st step find like button
        # if there's already liked, aria-label starts with "Remove" keyword.
        # something like this (Remove Like, Remove Love, Remove Haha).
        driver.find_element(By.XPATH,
        "//div[@class=' x3dsekl x1uuop16']//descendant::div[contains(@aria-label, 'Remove') and @role='button']")
        print(f"[alert ]\tYou've already given a react to this photo ({currentPhotoId})")
        already_liked = True
        countedReactedImages += 1
      except NoSuchElementException:
        already_liked = False

      if not already_liked:
        likeButton = driver.find_element(By.XPATH,
            "//div[@class=' x3dsekl x1uuop16']//descendant::div[@aria-label='Like' and @role='button']")

        # 2nd step hover the like button
        ActionChains(driver).move_to_element(likeButton).perform()

        # 3rd step find popup love react button
        loveReactElement = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH,
            "//div[@aria-label='Love' and @role='button']")))

        loveReactAction = ActionChains(driver)
        # 4th move mouse to love react button
        loveReactAction.move_to_element(loveReactElement)
        # finally give a love react
        loveReactAction.click(loveReactElement)
        # remove hover from like button
        loveReactAction.move_to_element_with_offset(likeButton, 4, 4)
        loveReactAction.perform()
        
        print(f"[react ]\t{currentPhotoId}")
        programReactedImages += 1
        countedReactedImages += 1

      if current_save_fbid:
        cu = furl(driver.current_url)
        cu.query.params.update({'fbid': current_save_fbid})
        current_save_fbid = ""
        driver.get(cu.url)
      else:
        # next Photo  
        ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()

      time.sleep(3) # delay

    time.sleep(10)


  except NoSuchElementException:
    print("No photo avaliable in target user")
  
  except KeyboardInterrupt:
    print("Terminated!")
    print(f"[result]\tprogram reacted {programReactedImages} image\
    {'s' if programReactedImages != 0 else ''}")
    print(f"[result]\tcounted reacted {countedReactedImages} image\
    {'s' if countedReactedImages != 0 else ''}")

