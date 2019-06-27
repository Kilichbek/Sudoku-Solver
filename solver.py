import argparse
import time
from utils import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object.
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object
    """
    # Creates parse
    parser = argparse.ArgumentParser()

    # Creates a command line argument
    parser.add_argument('--level', type=str, default='easy',
                        help='difficulty level ( easy/medium/hard/expert/)')

    # returns parsed argument collection
    return parser.parse_args()

def main():

    in_args = get_input_args()
    level = in_args.level
    digits = dict()
    grid = ''
    url = 'https://sudoku.com'


    if level:
        url = url + '/' + level + '/'

    print(url)
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    driver.maximize_window()
    driver.get(url)


    numbers = driver.find_elements_by_xpath('//*[@class="numpad"]/div[@class="numpad-item"]')

    for number in numbers:
        # find SVG and its PATH attributes in a web page
        svg = number.find_element_by_tag_name('svg')
        path = svg.find_element_by_tag_name('path')

        key = path.get_attribute('d')
        value = number.get_attribute('data-value')
        digits[key] = value

    game_rows = driver.find_elements_by_xpath('//*[@class="game-row"]')
    for row in game_rows:
        tds = row.find_elements_by_tag_name('td')
        for td in tds:
            try:
                path = td.find_element_by_tag_name('path')
                dkey = path.get_attribute('d')
                grid = grid + digits[dkey]

            except NoSuchElementException:
                grid = grid + '.'

    sudoku = search(grid_values(grid))
    display(sudoku)

    for i, row in enumerate(game_rows):
        tds = row.find_elements_by_tag_name('td')
        for j, td in enumerate(tds):
            try:
                path = td.find_element_by_tag_name('path')
            except NoSuchElementException:
                pos = rows[i] + cols[j]
                answer = int(sudoku[pos]) - 1
                td.click()
                numbers[answer].click()

    time.sleep(5)


if __name__ == "__main__":
    main()