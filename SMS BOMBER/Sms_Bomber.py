import logging
from threading import Thread

# ===================================================================
# LOGGING CONFIGURATION
# ===================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""Configure logging system with INFO level for tracking automation progress"""

# ===================================================================
# SELENIUM IMPORTS WITH ERROR HANDLING
# ===================================================================

try:
    from selenium.webdriver.support import expected_conditions as EC
    """Pre-defined conditions for WebDriverWait"""
    
    from selenium.webdriver.remote.webelement import WebElement
    """Represents HTML elements in the DOM"""
    
    from selenium.webdriver.support.ui import WebDriverWait
    """Implements explicit waits for element presence"""
    
    from selenium.webdriver.chrome.service import Service
    """Manages ChromeDriver service lifecycle"""
    
    from selenium.webdriver.chrome.options import Options
    """Configures Chrome browser options"""
    
    from selenium.webdriver.common.by import By
    """Provides element locator strategies (ID, XPATH, CSS, etc.)"""
    
    from selenium.webdriver import Chrome
    """Main WebDriver class for Chrome browser automation"""
    
except ImportError:
    raise ImportError("ImportError: Selenium not installed. Run: pip install selenium")


# ===================================================================
# CONFIGURATION DICTIONARIES
# ===================================================================

ID_dict = { 
    # ID for send_keys (input fields)
    "https://raastin.com/auth/register": ":R4dad57dd6:",
    "https://snappfood.ir/login/phone/": "submitPhoneNumber",
    "https://auth.digikala.com/realms/dk-group/protocol/openid-connect/auth?client_id=digikala-web-public&redirect_uri=https%3A%2F%2Fwww.digikala.com%2Fsso-redirect%2F%3Fback-url%3D%252Ffaq%252Fquestion%252F649%252F&state=8ae2798f-ff7b-4cc3-89a5-b91278b4a23f&response_mode=fragment&response_type=code&scope=openid&nonce=9f8a880c-8b6f-4dbc-a67a-67305304541a&code_challenge=RuD191YxZMYyRf8GMpSsfEp9qtrmCmzf_B_6cAovxiY&code_challenge_method=S256": "dk-login",
    "https://app.snapp.taxi/login": "login-submit",
    
    # ID for click (submit buttons)
    "https://accounts.theforge.ir/Account/SignIn": "username",
    "https://web.splus.ir/": "sign-in-phone-number"
}
"""
ID_dict: Maps website URLs to element IDs
- Keys: Full website URLs
- Values: Element IDs for input fields (send_keys) or buttons (click)

Usage: 
    For send_keys: locates input field by ID
    For click: locates button by ID
"""

hrefs = [
    "https://aryaland.ir/users/login",
    "https://talasea.ir/login/login-otp",
    "https://www.sheypoor.com/session",
    "https://positron-shop.com/sign-in",
    "https://drdr.ir/login/?f=true",
    "https://www.paziresh24.com/login/",
    "https://www.filimo.com/signin",
    "https://bama.ir/login", 
    "https://virgool.io/register", 
    "https://www.aparat.com/login",  
    "https://www.skyroom.online/panel/sign-up", 
    "https://www.alibaba.ir/login",  
    "https://safarmarket.com/auth/signin",
]
"""
hrefs: List of URLs for generic automation
- Uses default selectors: first <input> tag and first <button> tag
- No specific IDs required - suitable for simple login forms
"""

# ===================================================================
# FUNCTION: chrome() - Browser Initialization
# ===================================================================

def chrome(criterion: bool = False, service_path: str = None) -> Chrome:
    """
    Initializes and configures Chrome WebDriver with specified options.
    
    Parameters:
    -----------
    criterion : bool, default=False
        If True, enables headless mode (no GUI display)
        Reduces resource usage and enables background execution
    
    service_path : str, default=None
        File path to ChromeDriver executable
        Required if ChromeDriver is not in system PATH
    
    Returns:
    --------
    Chrome
        Configured Chrome WebDriver instance ready for automation
    
    Configuration Details:
    ----------------------
    Headless Mode (when criterion=True):
        - --headless: No GUI window
        - --disable-gpu: Disables GPU hardware acceleration
        - --window-size=1920,1080: Standard desktop resolution
        - --no-sandbox: Disables sandbox for container environments
        - --disable-dev-shm-usage: Prevents /dev/shm issues in Docker
    
    Example:
    --------
    >>> # Normal mode with default driver
    >>> driver = chrome()
    >>> 
    >>> # Headless mode with custom driver path
    >>> driver = chrome(criterion=True, service_path="/usr/bin/chromedriver")
    """
    chrome_options = Options()
    
    if criterion:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  
        chrome_options.add_argument("--window-size=1920,1080") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")    
    
    if service_path:
        service = Service(executable_path=service_path)
        return Chrome(service=service, options=chrome_options)
    else:
        return Chrome(options=chrome_options)
    
# ===================================================================
# FUNCTION: ec() - Element Wait Utility
# ===================================================================

def ec(t: tuple, waits: WebDriverWait) -> WebElement:
    """
    Waits for an element to be present in the DOM and returns it.
    This is a wrapper around Selenium's expected_conditions.
    
    Parameters:
    -----------
    t : tuple
        Selenium locator tuple in format (By.STRATEGY, "selector")
        Examples:
            (By.ID, "username")
            (By.XPATH, "//button[@type='submit']")
            (By.CSS_SELECTOR, ".btn-primary")
    
    waits : WebDriverWait
        Configured WebDriverWait instance with timeout value
        Typically: WebDriverWait(driver, timeout_seconds)
    
    Returns:
    --------
    WebElement
        The located element once it becomes present in the DOM
    
    Raises:
    -------
    TimeoutException
        If element not found within the configured timeout period
    
    Notes:
    ------
    - Uses presence_of_element_located condition
    - Blocks execution until element is found or timeout occurs
    - More reliable than implicit waits for dynamic content
    
    Example:
    --------
    >>> wait = WebDriverWait(driver, 20)
    >>> element = ec((By.ID, "submit-btn"), wait)
    >>> element.click()
    """
    return waits.until(EC.presence_of_element_located(t))

# ===================================================================
# CLASS: WebAutomation - Base Automation Class
# ===================================================================

class WebAutomation:
    """
    Base class providing core web interaction methods for automation.
    
    This class handles fundamental operations like:
    - Sending keys to input fields
    - Clicking elements using JavaScript
    - Waiting for element presence
    - Managing WebDriverWait instances
    
    Attributes:
    -----------
    driver : Chrome
        Active Chrome WebDriver instance
    number : int
        Phone number to be submitted
    waits : WebDriverWait
        WebDriverWait with 20-second timeout
    
    Inheritance:
    ------------
    This class is meant to be inherited by site-specific handler classes.
    """
    
    def __init__(self, driver: Chrome, number: str):
        """
        Initializes the WebAutomation instance.
        
        Parameters:
        -----------
        driver : Chrome
            Active Chrome WebDriver instance
        number : int
            Phone number to be submitted across all sites
            
        Initialization:
        ---------------
        - Stores driver and number as instance attributes
        - Creates WebDriverWait with 30-second timeout
        """
        self.driver = driver
        self.number = number
        self.waits = WebDriverWait(driver, 30)

    def XPATH(self, t: tuple):
        """
        Handles sites where input is the first <input> tag and submit button is located via XPath.
        
        Process:
        1. Locates the first <input> element on the page
        2. Sends the phone number to it
        3. Waits for button using provided XPath
        4. Clicks the button using JavaScript execution
        
        Parameters:
        -----------
        t : tuple
            XPath locator tuple for submit button
            Format: (By.XPATH, "xpath_expression")
        
        Notes:
        ------
        - Creates a separate WebDriverWait instance for reliability
        - Uses JavaScript click to handle overlay and scrolling issues
        - Assumes the first input tag is the phone number field
        
        Example:
        --------
        >>> automation.XPATH((By.XPATH, "/html/body/form/button"))
        """
        self.driver.find_element(By.TAG_NAME, "input").send_keys(self.number)
        btm = ec(t, self.waits)
        self.driver.execute_script("arguments[0].click();", btm)
    
    def send_keys(self, ID: str = None):
        """
        Locates phone number input field and sends the phone number.
        
        Logic:
        ------
        - If ID is provided: Locates input element by ID
        - If ID is None: Locates the first <input> tag on page
        
        Parameters:
        -----------
        ID : str, optional
            Element ID for specific input field
            If None, uses first input tag
        
        Example:
        --------
        >>> # Using first input
        >>> automation.send_keys()
        >>> 
        >>> # Using specific ID
        >>> automation.send_keys("phone-number-input")
        """
        if ID is None:
            btm_1 = ec((By.TAG_NAME, "input"), self.waits)
            btm_1.send_keys(self.number) 
        else:
            btm_1 = ec((By.ID, ID), self.waits)
            btm_1.send_keys(self.number)

    def click(self, ID: str = None, CSS_SELECTOR: str = None):
        """
        Clicks on an element using JavaScript execution.
        
        Uses JavaScript to click elements because it:
        - Bypasses overlay and iframe issues
        - Handles scrolling automatically
        - Works even if element is not interactable via normal click
        
        Priority Order:
        1. If ID provided: Click element by ID
        2. If CSS_SELECTOR provided: Click element by CSS selector
        3. Default: Click first <button> tag
        
        Parameters:
        -----------
        ID : str, optional
            Element ID to click
            
        CSS_SELECTOR : str, optional
            CSS selector for element
        
        Example:
        --------
        >>> # Click by ID
        >>> automation.click(ID="submit-btn")
        >>> 
        >>> # Click by CSS selector
        >>> automation.click(CSS_SELECTOR=".btn-primary")
        >>> 
        >>> # Click first button
        >>> automation.click()
        """
        if ID:
            btm = ec((By.ID, ID), self.waits)
            self.driver.execute_script("arguments[0].click();", btm)
        elif CSS_SELECTOR:
            btm = ec((By.CSS_SELECTOR, CSS_SELECTOR), self.waits)
            self.driver.execute_script("arguments[0].click();", btm)                
        else:
            btm = ec((By.TAG_NAME, "button"), self.waits)
            self.driver.execute_script("arguments[0].click();", btm) 

# ===================================================================
# CLASS: SiteHandler - Site-Specific Implementation
# ===================================================================

class SiteHandler(WebAutomation):
    """
    Handles site-specific automation patterns for various websites.
    
    This class extends WebAutomation and implements specific methods
    for each website or group of websites with similar patterns.
    
    Inherits:
    ---------
    All methods from WebAutomation class
    
    Methods:
    --------
    - digimark(): Handles Digimark AI login
    - get_XPATHS(): Handles XPath-based sites
    - get_ID(): Handles ID-based sites
    - urls(): Handles generic sites
    """
    
    def digimark(self):
        """
        Automates login process for Digimark AI website.
        
        Process:
        1. Navigates to https://app.digimark-ai.com/account/login/
        2. Finds first input field and sends phone number
        3. Clicks first button (submit)
        4. Clicks specific button with CSS selector .btn.ai-primary-btn.flex-center
        
        Website URL:
        ------------
        https://app.digimark-ai.com/account/login/
        
        Notes:
        ------
        - Requires two clicks: first for submit, second for confirmation
        - Uses CSS selector for second button due to dynamic class names
        """
        link = "https://app.digimark-ai.com/account/login/"
        self.driver.get(link)
        self.send_keys()
        self.click()
        self.click(CSS_SELECTOR=".btn.ai-primary-btn.flex-center")

    def get_XPATHS(self) -> None:
        """
        Automates sites requiring XPath-based selectors.
        
        Sites Handled:
        --------------
        1. Jabama: https://host.jabama.com/
           Uses nested XPath for button: /html/body/div[1]/main/div/div/div/footer/div/button
        
        2. Namava: https://www.namava.ir/register
           Uses simplified XPath: /html/body/div/div/div/div/button
        
        Process:
        --------
        For each site:
        1. Navigate to URL
        2. Execute XPATH() method with specific XPath
        3. Phone number is sent to first input
        4. Button is clicked via XPath
        
        Notes:
        ------
        - XPaths are hardcoded and may break with site updates
        - Both sites follow similar pattern: first input for phone
        """
        self.driver.get("https://host.jabama.com/")
        self.XPATH((By.XPATH, "/html/body/div[1]/main/div/div/div/footer/div/button"))
        self.driver.get("https://www.namava.ir/register")
        self.XPATH((By.XPATH, "/html/body/div/div/div/div/button"))
    
    def get_ID(self):
        """
        Automates sites from ID_dict with specific ID-based interactions.
        
        Two-stage processing due to different interaction patterns:
        
        Stage 1 (items 4-6):
        -------------------
        - Sites: snapp.taxi, theforge.ir, web.splus.ir
        - Pattern: send phone to first input, click button by ID
        - Usage: self.send_keys() + self.click(value)
        
        Stage 2 (items 0-4):
        -------------------
        - Sites: raastin.com, snappfood.ir, digikala.com
        - Pattern: send phone to specific input ID, click first button
        - Usage: self.send_keys(value) + self.click()
        
        Note:
        -----
        Processes items in reverse order (4:6 then 0:4) to handle
        different interaction patterns correctly.
        """
        for key, value in list(ID_dict.items())[4:6]:
            self.driver.get(key)
            self.send_keys()
            self.click(value)

        for key, value in list(ID_dict.items())[0:4]:            
            self.driver.get(key)
            self.send_keys(value)
            self.click()

    def urls(self):
        """
        Automates all URLs in the hrefs list using generic selectors.
        
        Process for each URL:
        1. Navigate to URL
        2. Find first <input> tag and send phone number
        3. Find first <button> tag and click it
        
        URLs Processed:
        ---------------
        13 websites including:
        - aryaland.ir
        - talasea.ir
        - sheypoor.com
        - positron-shop.com
        - drdr.ir
        - paziresh24.com
        - filimo.com
        - bama.ir
        - virgool.io
        - aparat.com
        - skyroom.online
        - alibaba.ir
        - safarmarket.com
        
        Notes:
        ------
        - Uses default selectors (first input, first button)
        - Works for simple login/registration forms
        - May fail on complex pages with multiple forms
        """
        for link in hrefs:
            self.driver.get(link)
            self.send_keys()
            self.click()

# ===================================================================
# FUNCTION: start() - Single Thread Execution
# ===================================================================

def start(number: str, path: str = None, add: int = 2) -> None:
    """
    Executes complete automation sequence in a single thread.
    
    This function creates a Chrome driver and runs the automation
    sequence for the specified number of iterations.
    
    Parameters:
    -----------
    number : str
        Phone number to submit across all websites
        
    path : str, default=None
        ChromeDriver executable path
        If None, uses system PATH
        
    add : int, default=2
        Number of automation iterations to run
        Maximum allowed: 11
        
    Validation:
    -----------
    Raises ValueError if add > 11
    
    Execution Sequence:
    -------------------
    For each iteration:
    1. digimark() - Digimark AI website
    2. get_XPATHS() - Jabama and Namava websites
    3. urls() - All hrefs list websites
    
    Cleanup:
    --------
    - driver.quit() is called in finally block
    - Ensures browser is closed even if errors occur
    
    Example:
    --------
    >>> start("09123456789", path="/usr/bin/chromedriver", add=3)
    
    Notes:
    ------
    - Each iteration processes approximately 18 websites
    - Time per iteration: ~3-5 minutes depending on network
    """
    if add > 11:
        raise ValueError("add It is very big")
    driver = chrome(criterion = False, service_path = path)
    get = SiteHandler(driver,number)   
    try:
        for _ in range(add):
            try:
                get.digimark()
                get.get_XPATHS()
                get.urls()
            except:
                pass
    finally:
        driver.quit()     

# ===================================================================
# FUNCTION: main() - Multi-Threaded Orchestrator
# ===================================================================

def main(speed: int = 20) -> None:
    """
    Orchestrates multi-threaded execution of automation tasks.
    
    This function creates multiple threads, each running the automation
    sequence independently with its own browser instance.
    
    Parameters:
    -----------
    speed : int, default=20
        Controls the number of threads to create
        Must be a multiple of 10 (10, 20, 30, ..., 100)
        
    Valid Values:
    -------------
    [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    Validation:
    -----------
    - Raises ValueError if speed > 100
    - Raises ValueError if speed not in valid values list
    
    Thread Calculation:
    -------------------
    thread_count = speed // 10
    Examples:
        - speed=20 -> 2 threads
        - speed=50 -> 5 threads
        - speed=100 -> 10 threads
    
    Thread Configuration:
    --------------------
    - Each thread runs start() function
    - Thread names: "start 0", "start 1", "start 2", ...
    - Each thread uses:
        - Phone: "number"
        - Path: D:\oo\porojes_my\py\web_scraping\chromedriver.exe
        - Iterations: 2
    
    Resource Considerations:
    -----------------------
    - Each thread opens its own Chrome browser (~200MB RAM)
    - Network bandwidth scales with thread count
    - CPU usage increases with active threads
    
    Example:
    --------
    >>> # Start with 4 threads
    >>> main(speed=40)
    >>> 
    >>> # Start with 8 threads
    >>> main(speed=80)
    
    Notes:
    ------
    - Phone number is hardcoded (should use environment variables)
    - ChromeDriver path is hardcoded (should be configurable)
    - Threads run concurrently and independently
    - Errors in one thread do not affect others
    """
    adds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    if speed > 100:
        raise ValueError("speed is You can't give more than a hundred.")
    if not speed in adds:
        raise ValueError(f"I cannot support the position you gave. The value must be a member of this list: {adds} .")
    speed = speed//10
    number = "09963913815" 
    add = 2
    path = r"D:\oo\porojes_my\py\web_scraping\chromedriver.exe"
    logger.info("Pages currently opening:",speed)
    threads = []
    for i in range(speed):
        t = Thread(target=start, args=(number,path,add,),name=f"start {i}")
        t.start()
        threads.append(t)
    for t in threads:
        t.join()  
    # ===================================================================
# PROGRAM ENTRY POINT
# ===================================================================

if __name__ == "__main__":
    """
    Entry point for script execution.
    
    When the script is run directly (not imported as a module),
    this executes main() with default speed of 20.
    
    This creates 2 threads (20 // 10) running the automation
    sequence concurrently.
    
    To run with different thread counts, modify the main() call:
        main(speed=40)  # 4 threads
        main(speed=80)  # 8 threads
        main(speed=100) # 10 threads
    """
    main(speed=20)

