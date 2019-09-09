# selenium for testing
from selenium import webdriver
# time to pause, allow time for webpage to load during script execution
import time

driver_location = "C:\\Users\Kayla\Documents\chromedriver.exe"
web_address = "https://smithkaylar.printercloud.com/admin/index.php"
res = open("login_results.txt", "w+")
valid_admin_user = "smithkaylar"
valid_admin_pass = "t3stpass"
driver = webdriver.Chrome(driver_location)
driver.get(web_address)


def login_test(username, password):
    try:
        driver.find_element_by_id("relogin_user").send_keys(username)
        driver.find_element_by_id("relogin_password").send_keys(password)
        driver.find_element_by_id("admin-login-btn").click()
        time.sleep(4)
        driver.find_element_by_id("user-menu").click()
        driver.find_element_by_class_name("allowlink").click()
        return True
    except:
        return False


def is_allowed(allow, file):
    if allow:
        file.write("ALLOWED\n")
    else:
        file.write("BLOCKED\n")


# Test 1: valid login
allowed = login_test(valid_admin_user, valid_admin_pass)
res.write("TEST 1: Admin login ")
is_allowed(allowed, res)


# Test 2: valid username, add extra characters to end of invalid password
res.write("\nTEST 2: valid username with password variations\nVariation 1: password with trailing spaces ")
allowed = login_test(valid_admin_user, valid_admin_pass + "    ")
is_allowed(allowed, res)

res.write("Variation 2: password with leading spaces ")
allowed = login_test(valid_admin_user, "   " + valid_admin_pass)
is_allowed(allowed, res)

res.write("Variation 3: all capitalized password ")
allowed = login_test(valid_admin_user, valid_admin_pass.upper())
is_allowed(allowed, res)

res.write("Variation 4: password with non-space trailing characters ")
allowed = login_test(valid_admin_user, valid_admin_pass + "1")
is_allowed(allowed, res)

res.write("Variation 5: password with non-space leading characters ")
allowed = login_test(valid_admin_user, "1" + valid_admin_pass)
is_allowed(allowed, res)

res.write("Variation 6: backwards password ")
allowed = login_test(valid_admin_user, "ssapts3t")
is_allowed(allowed, res)

res.write("Variation 7: admin/admin ")
allowed = login_test("admin", "admin")
is_allowed(allowed, res)


# Test 3, user names
res.write("\nTEST 3: bad user names\n")
res.write("Variation 1: all caps username ")
allowed = login_test(valid_admin_user.upper(), valid_admin_pass)
is_allowed(allowed, res)

res.write("Variation 2: use other employee username with admin password ")
allowed = login_test("employee1", valid_admin_pass)
is_allowed(allowed, res)

res.write("Variation 3: unrelated username with admin password ")
allowed = login_test("administrator", valid_admin_pass)
is_allowed(allowed, res)

res.write("\nTest 4: Lost password link ")
driver.find_element_by_id("forgot-password").click()
time.sleep(2)
try:
    driver.find_element_by_id("email")
    res.write("ALLOWED\n")
except:
    res.write("BLOCKED\n")

res.close()
