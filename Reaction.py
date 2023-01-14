import time
from furl import furl
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Reaction:

  def __init__(self, driver):

    self.driver = driver

    r = {
      "LIKE"  : "Like",
      "LOVE"  : "Love",
      "CARE"  : "Care",
      "HAHA"  : "Haha",
      "WOW"   : "Wow",
      "SAD"   : "Sad",
      "ANGRY" : "Angry"
    }
    self.reacts = namedtuple('Reacts', r.keys())(**r)

    postButtonsFrameClass = " xq8finb x16n37ib"

    url = furl(self.driver.current_url)
    url_segments = url.path.segments

    if url_segments[0] == "watch":
      # for videos
      postButtonsFrameClass =  "x78zum5 x1iyjqo2"
    elif url_segments[1] == "videos":
      # early type of videos
      postButtonsFrameClass = "x6s0dn4 xzsf02u x78zum5 x1q0g3np x1iyjqo2 x6prxxf x9ek82g"
    elif url_segments[0] == "photo" or url_segments[1] == "photos":
      # after click post photo, class are changed
      postButtonsFrameClass = " x3dsekl x1uuop16"
    
    self.postButtonsFrameXPATH =  f"//div[contains(@class, '{postButtonsFrameClass}')]"

    try:
      # check internet connection stuff
      ButtonsFrameElement = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
            self.postButtonsFrameXPATH
            ))
      )
    except TimeoutException:
      print("Bad Internet Connection or Cannot Locate Buttons Frame")
      exit()

  
  def giveReact(self, react):

    if not self.isLiked():
      likeButton = self.driver.find_element(By.XPATH,
          f"{self.postButtonsFrameXPATH}//descendant::div[@aria-label='Like' and @role='button']")

      # hover the like button
      ActionChains(self.driver).move_to_element(likeButton).perform()

      # find popup love react button
      reactElement = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
          f"//div[@aria-label='{react}' and @role='button']")))

      reactAction = ActionChains(self.driver)
      # move mouse to love react button
      reactAction.move_to_element(reactElement)
      # finally give a love react
      reactAction.click(reactElement)
      # remove hover from like button
      reactAction.move_to_element_with_offset(likeButton, 0, 30)
      reactAction.perform()

  
  def removeReact(self):
    if self.isLiked():
      likeButton = self.driver.find_element(By.XPATH, 
      f"{self.postButtonsFrameXPATH}//descendant::div[contains(@aria-label, 'Remove') and @role='button']")
      likeButton.click()
    
  
  def isLiked(self):
    already_liked = False

    try:
      # if there's already liked, aria-label starts with "Remove" keyword.
      # something like this (Remove Like, Remove Love, Remove Haha).
      self.driver.find_element(By.XPATH,
      f"{self.postButtonsFrameXPATH}//descendant::div[contains(@aria-label, 'Remove') and @role='button']")
      already_liked = True
    except NoSuchElementException:
      already_liked = False

    return already_liked


if __name__ == "__main__":

  # Chrome Driver
  options = webdriver.ChromeOptions()
  options.add_argument("--user-data-dir=chrome-data") # cookies
  driver = webdriver.Chrome(options=options)
  #driver.get("https://www.facebook.com/photo/?fbid=126412403651983&set=pcb.126412493651974")
  driver.get("https://www.facebook.com/thet.khine.587/posts/10218899022746124")
  #driver.get("https://www.facebook.com/watch?v=567273305033982")
  a = Reaction(driver)
  a.giveReact(a.reacts.LOVE)
  time.sleep(3)
  a.removeReact()
  time.sleep(10)