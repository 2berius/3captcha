# 2berius' ReCAPTCHA ducker (FINAL)

# misc
import speech_recognition as sr
import time
from pydub import AudioSegment
import random
import string
import wget
import os

# selenium libraries
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def main():

    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        time.sleep(3)
        driver.get("https://www.google.com/recaptcha/api2/demo")
    except:
        print("--- Update chromedriver ---")

    def manipulate_captcha(driver):
        captcha = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(captcha[0])
        time.sleep(3)
        driver.find_element_by_class_name("recaptcha-checkbox-border").click()
        driver.switch_to.default_content()
        captcha = driver.find_element_by_xpath(
            "/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
        driver.switch_to.frame(captcha[0])
        time.sleep(3)
        driver.find_element_by_id("recaptcha-audio-button").click()
        driver.switch_to.default_content()
        captcha = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(captcha[-1])
        time.sleep(3)
        driver.find_element_by_xpath(
            "/html/body/div/div/div[3]/div/button").click()

        src = driver.find_element_by_id("audio-source").get_attribute("src")
        print("[INFO] Audio src: %s" % src)

        source = 'payload.mp3'

        # download audio challenge from recaptcha
        wget.download(src, out=source)

        wavfile = "audio" + ''.join(random.choice(string.ascii_lowercase)
                                 for _ in range(6)) + ".wav"

        # .mp3 to .wav conversion
        aud = AudioSegment.from_mp3(source)
        aud.export(wavfile, format="wav")

        # remove unnecessary files
        os.remove(source)

        # call proceeding function to output audio text
        audio2text(wavfile, driver)

    def audio2text(wavfile, driver):
        time.sleep(3)
        rec = sr.Recognizer()

        with sr.AudioFile(wavfile) as src:

            rec.adjust_for_ambient_noise(src)
            audio = rec.listen(src)

            try:
                extracted_text = rec.recognize_google(audio, language='en-IN')
                print('Audio to text: ' + extracted_text)

                aud_elem = driver.find_element_by_id('audio-response')
                aud_elem.clear()
                aud_elem.send_keys(extracted_text)
                driver.find_element_by_id(
                    'recaptcha-verify-button').click()

            except Exception as error:
                print(error)

            finally:
                os.remove(wavfile)
                time.sleep(15)
                driver.close()

    if __name__ == '__main__':
        manipulate_captcha(driver)


if __name__ == "__main__":
    main()
