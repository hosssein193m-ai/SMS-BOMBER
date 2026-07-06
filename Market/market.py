from allykit.web_kit.Get_Code import javascript_pro , BeautifulSoup , javascript_driver , WebDriverWait,By
from allykit.web_kit.Elastic_bands import DiskCache
from allykit.web_kit.CChrome import chrome, wait_for_element
import json
from deepdiff import DeepDiff
import csv
from typing import Optional, Dict ,Tuple , List ,Union 
from datetime import datetime

ec = wait_for_element

def dump_file(file: str, text: dict | list) -> bool:
    """
    Serializes a Python object to a JSON file.

    Args:
        file (str): The path to the file where JSON data will be saved.
        text (dict or list): The Python object (dict, list, etc.) to be serialized.

    Returns:
        None
    """
    try:
        with open(file, "w", encoding='utf-8') as f:
            json.dump(text, f, ensure_ascii=False, indent=4)
    except IOError:
        print("IOError: An error occurred while writing to the file.")
        return False
    except Exception as e:
        print(f"Exception: An unexpected error occurred: {e}")
        return False
    return True

def load_file(file: str, s: bool = False) -> dict | list:
    """
    Loads JSON data from a file. If the file is missing, it creates an empty file.

    Args:
        file (str): The path to the JSON file.
        s (bool): If True, returns an empty list ([]) on JSON decode error. 
                  If False, returns an empty dictionary ({}) on JSON decode error.

    Returns:
        dict | list: The parsed JSON data, or an empty container if an error occurs.
    """

    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] if s else {}
    except Exception as e:
        raise Exception(e)


# -------------------------

namefile_iran = "iran.json"
namefile_Market = "Market.json"
name_Rating = "rating.json"
online_market = "Online_Market.json"

def Disk(time, url : str) -> BeautifulSoup:
    """
    Fetches and parses a webpage using caching or direct request.

    Args:
        time (int): TTL in hours for cache. If 0, bypass cache.
        url (str): The target URL.

    Returns:
        BeautifulSoup: Parsed HTML of the page.
    """    
    if time == 0:
        soup = javascript_pro(url)
    else:
        DC = DiskCache(ttl_hours = time)
        soup = DC.javascript_pro(url)
    return soup    

class MarketLeaders:
    """
    A web scraping utility for extracting and managing market ranking data 
    from the Toobit cryptocurrency markets page with caching and persistence.

    This class provides functionality to scrape market data, store it locally,
    and query specific rankings and currency information.

    Attributes:
        namefile (str): JSON filename for persistent data storage
        _extraction_time_key (str): Internal key for timestamp tracking
        soup (Disk): Disk-based caching instance with TTL configuration
    """

    def __init__(self, namefile: str = name_Rating, time: int = 1):
        """
        Initializes the market data scraper with caching configuration.

        Args:
            namefile (str): JSON filename for persistent data storage. 
                           Defaults to name_Rating.
            time (int): Cache Time-To-Live (TTL) in hours. Defaults to 1 hour.

        Attributes:
            self.namefile: Stores the filename for data persistence
            self._extraction_time_key: Internal key for timestamp tracking 
                                       ("extraction time")
            self.soup: Disk-based caching instance that handles HTML parsing 
                       with TTL
        """
        self.namefile = namefile
        url = "https://www.toobit.com/fa/markets" 
        self._extraction_time_key = "extraction time"
        self.soup = Disk(time, url)            

    def _get_text(self, element: BeautifulSoup) -> str:
        """
        Extracts and cleans text from a BeautifulSoup element.

        Args:
            element (BeautifulSoup): The HTML element to extract text from

        Returns:
            str: Cleaned text without whitespace, or "N/A" if element is None
        """
        return element.get_text(strip=True) if element else "N/A"

    def get_top_ranks(self) -> List[Dict]:
        """
        Scrapes the current market data from the Toobit website and returns 
        structured ranking information.

        Returns:
            List[Dict]: A list where each element is a dictionary containing:
                - Ranking categories (e.g., "پیشروها" for top gainers) as keys
                - Nested dictionaries with 'name' and 'price' fields 
                - An additional dictionary containing the extraction timestamp

        Example:
            [
                {"پیشروها": {"name": "Bitcoin", "price": "45,000"}},
                {"بیشترین کاهش قیمت": {"name": "Ethereum", "price": "2,800"}},
                {"extraction time": "2026-06-28T14:30:00"}
            ]
        """
        data = []
        soup = self.soup
        rows = soup.find_all("div", class_="market-card-new flex-col")    
        for row in rows:
            name = row.find("span", class_="symbol-name flex-row items-center fz16 lh20")
            price = row.find("span", class_="card-price fz14 lh20")
            rank_type = row.find("span", class_="card-title-text")
            if name and price:
                data.append({
                    self._get_text(rank_type): {
                        "name": self._get_text(name),
                        "price": self._get_text(price)
                    }
                })
        data.append({self._extraction_time_key: datetime.now().isoformat()})
        return data
    
    def set(self):
        """
        Scrapes fresh data and persists it to the JSON file specified during 
        initialization.

        Behavior:
            - Calls get_top_ranks() to fetch current market data
            - Writes the data to the configured JSON file using dump_file()
        """
        text = self.get_top_ranks()
        dump_file(self.namefile, text)

    def _load_data(self) -> List:
        """
        Internal method that loads data from the JSON storage file.

        Returns:
            List: The parsed data list, or an empty list if:
                - The file doesn't exist
                - The file contains invalid JSON
                - The data is not a list type

        Exceptions: All exceptions are caught and return []
        """
        try:
            data = load_file(self.namefile)
            if not isinstance(data, list):
                return []
            return data
        except Exception:
            return []

    def search_time(self, came_back: bool = True) -> Dict:
        """
        Retrieves the extraction timestamp from the stored data.

        Args:
            came_back (bool): If True, returns just the timestamp string; 
                             if False, returns the entire timestamp dictionary.
                             Defaults to True.

        Returns:
            Union[str, Dict]: 
                - str: The ISO-format timestamp when came_back=True
                - Dict: The full dictionary containing the timestamp when 
                       came_back=False

        Example:
            >>> scraper.search_time()
            "2026-06-28T14:30:00"
            >>> scraper.search_time(came_back=False)
            {"extraction time": "2026-06-28T14:30:00"}
        """
        data = self._load_data()
        for item in data:
            if isinstance(item, dict) and self._extraction_time_key in item:
                if came_back:
                    return item[self._extraction_time_key]
                else:
                    return item

    def find_currency(self, name: str):
        """
        Searches for a specific currency by name across all ranking categories.

        Args:
            name (str): The exact currency name to search for (case-sensitive)

        Returns:
            Tuple(bool, Dict): 
                - First element: True if found, False otherwise
                - Second element: The dictionary containing the currency data 
                                 if found, otherwise {}

        Example:
            >>> found, data = scraper.find_currency("Bitcoin")
            >>> # Returns: (True, {"پیشروها": {"name": "Bitcoin", "price": "45,000"}})
        """
        data = self._load_data()
        for rows in data:
            if isinstance(rows, dict) and self._extraction_time_key not in rows:
                for key, value in rows.items():
                    row = value.get("name")
                    if name == row:
                        return (True, rows)
        return (False, {})

    def search(self, rank_type: str, field: Optional[str] = None) -> Union[Dict, str, None]:
        """
        Searches for a specific ranking category and optionally extracts a 
        specific field.

        Args:
            rank_type (str): The ranking category key to search for 
                            (e.g., "پیشروها")
            field (Optional[str]): Specific field within the ranking data to 
                                  extract (e.g., "name" or "price")

        Returns:
            Union[Dict, str, None]: 
                - Dict: The entire ranking dictionary if no field is specified
                - str: The value of the specified field if provided
                - None: If the ranking category is not found

        Raises:
            ValueError: If the specified field doesn't exist in the ranking data

        Example:
            >>> # Get entire ranking
            >>> scraper.search("پیشروها")
            {"پیشروها": {"name": "Bitcoin", "price": "45,000"}}
            
            >>> # Get specific field
            >>> scraper.search("پیشروها", "name")
            "Bitcoin"
        """
        data = self._load_data()
        
        target_item = None
        for item in data:
            if isinstance(item, dict) and rank_type in item:
                target_item = item
                break
        
        if not target_item:
            return None
        
        if field:
            rank_data = target_item.get(rank_type, {})
            if field in rank_data:
                return rank_data[field]
            raise ValueError(f"Field '{field}' does not exist in ranking '{rank_type}'")
        
        return target_item

    def get_all_rankings(self) -> Dict:
        """
        Retrieves all ranking categories from the stored data.

        Returns:
            Dict: A dictionary containing all ranking categories and their 
                 data, excluding the timestamp entry

        Example:
            {
                "پیشروها": {"name": "Bitcoin", "price": "45,000"},
                "بیشترین کاهش قیمت": {"name": "Ethereum", "price": "2,800"},
                "حجم برتر": {"name": "Tether", "price": "1.00"}
            }
        """
        data = self._load_data()
        result = {}
        for item in data:
            if isinstance(item, dict) and self._extraction_time_key not in item:
                result.update(item)
        return result

    def get_top_gainers(self) -> Optional[dict]:
        """
        Retrieves the top gainers (پیشروها) ranking data.

        Returns:
            Optional[dict]: The ranking dictionary if found, otherwise None
        """
        return self.search("پیشروها")
    
    def get_top_losers(self) -> Optional[dict]:
        """
        Retrieves the top losers (بیشترین کاهش قیمت) ranking data.

        Returns:
            Optional[dict]: The ranking dictionary if found, otherwise None
        """
        return self.search("بیشترین کاهش قیمت")
    
    def get_top_volume(self) -> Optional[dict]:
        """
        Retrieves the top volume (حجم برتر) ranking data.

        Returns:
            Optional[dict]: The ranking dictionary if found, otherwise None
        """
        return self.search("حجم برتر")

class Iranian_market:
    """
    Class to fetch and manage Iranian market data (e.g., gold, dollar, Tether)
    from tgju.org.
    """
    def __init__(self, namefile: str = namefile_iran, time: int = 1):
        """
        Initializes the Iranian market scraper.

        Args:
            namefile (str): JSON file to store data.
            time (int): Cache TTL in hours.
        """
        url = "https://www.tgju.org/" 
        self.soup = Disk(time,url)
        self.namefile = namefile

    def Currencies(self,ID : str ) -> str:
        """
        Extracts the price of a specific currency by its HTML ID.

        Args:
            ID (str): The HTML ID of the currency element.

        Returns:
            str: The price as a string.
        """        
        soup = self.soup.find("li",id = ID)
        return soup.find("span", class_ = "info-price").get_text(strip=True)

    def get_currencies(self) -> dict:
        """
        Fetches all defined Iranian market currency prices.

        Returns:
            dict: A dictionary with currency names as keys and their prices as values,
                  including an extraction timestamp.
        """
        data_map = {
            "gold 18": "l-geram18",
            "coin": "l-sekee",
            "stock market": "l-gc30",
            "grams of gold": "l-mesghal",
            "dollar": "l-price_dollar_rl",
            "Brent oil": "l-oil_brent",
            "Tether": "l-crypto-tether-irr",
            "Bitcoin": "l-crypto-bitcoin"
        }

        extracted_data = {key: self.Currencies(id_val) for key, id_val in data_map.items()}
        extracted_data["extraction time"] = datetime.now().isoformat()
        return extracted_data

    def search_time(self) -> str:
        """
        Retrieves the extraction time from the stored JSON file.

        Returns:
            str: The extraction time.

        Raises:
            ValueError: If the extraction time key is missing.
        """        
        time = "extraction time"
        data = load_file(self.namefile)  
        if time in data:
            return data.get(time)
        raise ValueError("The currency name is invalid.")
    
    def search(self, item : str) -> tuple[str,dict]:
        """
        Searches for a specific currency price in the stored JSON file.

        Args:
            item (str): The currency name.

        Returns:
            tuple: (price string, {currency: price})

        Raises:
            ValueError: If the currency name is not found.
        """
        data = load_file(self.namefile)  
        if item in data:
            price = data.get(item)
            return (price, {item:price})
        raise ValueError("The currency name is invalid.")

    def set(self) -> None:
        """
        Fetches live data and saves it to the JSON file.
        """        
        text = self.get_currencies() 
        dump_file(self.namefile,text)

class World_Market:
    """
    Class to fetch and manage world market data (cryptocurrencies, commodities)
    from toobit.com.
    """
    def __init__(self, namefile : str = namefile_Market, time : int = 1):
        """
        Initializes the world market scraper.

        Args:
            namefile (str): JSON file to store data.
            time (int): Cache TTL in hours.
        """        
        self.namefile = namefile
        url = "https://www.toobit.com/fa/markets" 
        self.soup = Disk(time,url)

    def get_currencies(self, license : bool = True) -> list[str,dict]:
        """
        Extracts a list of world market currency data.

        Args:
            license (bool): If True, prepends extraction timestamp.

        Returns:
            list: A list containing timestamp (if enabled) and dicts of currency data.
        """        
        soup = self.soup
        rows = soup.select("ul.flex-row.flex-row-space-between.items-center.w-full.border-xs-b.text-1.c-table-row.cursor-pointer")
        
        currencies_data = []

        if license:
            currencies_data.append(f"extraction time : {datetime.now().isoformat()}")    

        for row in rows:
            try:
                # استخراج نام ارز
                name_span = row.select_one("span.text-1.weight-500")
                currency_name = name_span.get_text(strip=True) if name_span else "N/A"
                
                # استخراج قیمت
                price_span = row.select("li.flex-row-flex-end.family-gilroy-b.table-td span.weight-500")[0]
                price = price_span.get_text(strip=True) if price_span else "N/A"
                
                # استخراج تغییرات 24 ساعته
                change_span = row.select("li.flex-row-flex-end.family-gilroy-b.table-td span.weight-500")[1]
                change = change_span.get_text(strip=True) if change_span else "N/A"
                
                # استخراج حجم معاملات
                volume_div = row.select("li.flex-row-flex-end.family-gilroy-b.table-td div.weight-500")[0]
                volume = volume_div.get_text(strip=True) if volume_div else "N/A"
                
                currencies_data.append({
                    currency_name:{
                        'price': price,
                        'change_24h': change,
                        'volume': volume
                        }
                })
                
            except (IndexError, AttributeError) as e:
                print(f"Error parsing row: {e}")
                continue
        
        return currencies_data    
        
    def set(self,license : bool = True) -> bool:
        """
        Fetches live world market data and saves it to JSON.

        Args:
            license (bool): Whether to include extraction timestamp.

        Returns:
            bool: True if save succeeded, False otherwise.
        """        
        text = self.get_currencies(license) 
        return dump_file(self.namefile,text) 

    def search_time(self) -> tuple:
        """
        Retrieves the extraction time from stored world market data.

        Returns:
            tuple: (full timestamp string, timestamp value after colon)
        """        
        data = load_file(self.namefile)        
        for Information  in data:
           if isinstance(Information, str):
                return Information , ''.join(Information.split(":")[1:])
        return None      

    def search(self, name: str, destination: str = None) -> dict | str:
        """
        Searches for a specific currency or its attribute.

        Args:
            name (str): Currency name (e.g., "BTCUSDT").
            destination (str, optional): Specific field to return (price, change_24h, volume).

        Returns:
            dict | str: The full currency dict or a specific value.

        Raises:
            ValueError: If currency name or destination is invalid.
        """        
        data = load_file(self.namefile)        
        for info in data:
            if isinstance(info, dict) and name in info:
                dict_info = info[name]
                if destination is None:
                    return dict_info
                if destination in dict_info:
                    return dict_info[destination]
                raise ValueError("The currency destination is invalid.")
        
        raise ValueError("The currency name is invalid.") 

class OnlineMarket:
    """
    A comprehensive class for extracting, processing, and storing cryptocurrency market data 
    from the Toobit exchange platform.
    
    This class handles the entire workflow of:
    - Launching and configuring a Chrome browser instance
    - Navigating to the Toobit markets page
    - Searching for specific trading pairs
    - Extracting price, volume, and change data
    - Storing data in JSON format
    - Querying stored data with flexible search options
    
    The class uses Selenium WebDriver for browser automation and BeautifulSoup for HTML parsing,
    providing a robust solution for market data extraction and management.
    Attributes:
        name_market (str): The market symbol to search for (e.g., "BTC", "ETH")
        filename (str): The JSON file path for data storage
    """
    def __init__(self, name_market: str, filename: str = online_market):
        """
        Initialize a new OnlineMarket instance with specified market and storage configuration.
        
        This constructor sets up the core parameters that define which market data to fetch
        and where to store the extracted information. The market name is used as the search
        query on the Toobit platform.
        
        Args:
            name_market (str): The cryptocurrency trading pair symbol to search for.
                Examples: "BTC", "ETH", "XRP", "ADAUSDT"
                This value is used as the search term in the Toobit search field.
            
            filename (str, optional): Path to the JSON file where market data will be stored.
                Defaults to "Online_Market.json". The file will be created/overwritten
                when saving data.
        
        Examples:
            >>> market = OnlineMarket("BTCUSDT")
            >>> market = OnlineMarket("ETH", "ethereum_data.json")
        
        Raises:
            TypeError: If name_market is not a string
        """
        self.name_market = name_market
        self.namefile = filename
        self.currencies_data = None

    def Online(self, *args) -> BeautifulSoup:
        """
        Launches a Chrome browser, navigates to Toobit markets page, searches for the 
        specified market, and returns the page source as a BeautifulSoup object.

        This method orchestrates the complete browser automation workflow:
        1. Initializes a Chrome WebDriver with custom configuration options
        2. Navigates to the Toobit markets page (https://www.toobit.com/fa/markets)
        3. Waits for the search input field to load (explicit wait up to 50 seconds)
        4. Enters the market name (self.name_market) into the search field
        5. Submits the search by pressing the Enter key
        6. Captures the page source after search results load
        7. Converts the HTML to a BeautifulSoup object for parsing
        8. Closes the browser and frees resources

        Args:
            *args: Variable length argument list passed to the chrome() function.
                These arguments configure the Chrome browser instance and can include:
                - criterion (bool): If True, runs in headless mode
                - service_path (str): Path to ChromeDriver executable
                - proxy (str): Proxy server address (e.g., '127.0.0.1:8080')
                - user_agent (str): Custom User-Agent string
                - incognito (bool): Enable incognito/private browsing mode
                - lang (str): Language setting (defaults to "en-US")
                - disable_images (bool): Disable image loading for faster performance
                - disable (bool): Disable extensions, notifications, and popups

        Returns:
            BeautifulSoup: A BeautifulSoup object containing the parsed HTML of the
                search results page. This object can be used for data extraction
                using CSS selectors or other BeautifulSoup methods.

        Raises:
            TimeoutException: If the search input field fails to load within 50 seconds.
            WebDriverException: If the Chrome driver fails to initialize or navigate.
            Exception: Any other Selenium-related exceptions during browser automation.

        Example:
            >>> market = OnlineMarket("BTCUSDT")
            >>> soup = market.Online(headless=True, disable_images=True)
            >>> # Extract data from soup
            >>> rows = soup.select("ul.flex-row")
            >>> print(f"Found {len(rows)} rows")
            Found 25 rows

        Notes:
            - The method uses an explicit wait with a 50-second timeout for element loading
            - The search input is located using class name "el-input__inner"
            - After search, the page automatically updates with filtered results
            - Browser is automatically closed after page source extraction
            - This method is synchronous and blocks until page loads
            - Network latency or slow page loads may increase execution time
        """
        url = "https://www.toobit.com/fa/markets"
        driver = chrome(*args)
        waits = WebDriverWait(driver , 50)
        driver.get(url)
        element = ec((By.CLASS_NAME,"el-input__inner"),waits)
        element.send_keys(self.name_market)
        javascript = javascript_driver(driver)
        return javascript

    def Read_code(self, *args):
        """
        Extracts and structures cryptocurrency market data from the Toobit website.

        This method performs the complete data extraction workflow:
        1. Calls Online() to fetch the page HTML as BeautifulSoup
        2. Uses CSS selectors to locate all currency rows in the search results
        3. For each row, extracts:
            - Currency name (trading pair)
            - Current price
            - 24-hour percentage change
            - 24-hour trading volume
        4. Structures the data into a list of dictionaries
        5. Optionally includes an extraction timestamp

        The extraction is resilient to missing data - if any element is not found,
        it defaults to "N/A" instead of failing. Individual row parsing errors are
        caught and logged, allowing the method to continue processing remaining rows.

        Args:
            *args: Variable length argument list passed to the Online() method.
                These arguments control browser configuration during page fetching.
                See Online() method documentation for available parameters.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries where each dictionary
                represents a single currency/trading pair. Each dictionary has the
                structure:
                
                {
                    "CURRENCY_NAME": {
                        "price": "42,567.89",
                        "change_24h": "+5.23%",
                        "volume": "1,234,567,890"
                    }
                }
                
                If the 'license' variable is truthy, a timestamp string is prepended
                to the list:
                
                [
                    "extraction time : 2026-06-28T14:30:45.123456",
                    {"BTCUSDT": {"price": "42567.89", "change_24h": "+5.23%", "volume": "1.2B"}},
                    ...
                ]

        Raises:
            ValueError: If no data rows are found in the page.
            AttributeError: If the soup object is invalid or None.
            Exception: Any exception from the Online() method (browser-related).

        Example:
            >>> market = OnlineMarket("ETH")
            >>> data = market.Read_code(headless=True)
            >>> for item in data:
            ...     if isinstance(item, dict):
            ...         for currency, info in item.items():
            ...             print(f"{currency}: ${info['price']} ({info['change_24h']})")
            ETHUSDT: $3,456.78 (+2.34%)

        Notes:
            - The method uses specific CSS selectors that match Toobit's HTML structure
            - Selector for rows: "ul.flex-row.flex-row-space-between.items-center.w-full.border-xs-b.text-1.c-table-row.cursor-pointer"
            - Currency name from: "span.text-1.weight-500"
            - Price from: first "li.flex-row-flex-end.family-gilroy-b.table-td span.weight-500"
            - Change from: second "li.flex-row-flex-end.family-gilroy-b.table-td span.weight-500"
            - Volume from: "li.flex-row-flex-end.family-gilroy-b.table-td div.weight-500"
            - The 'license' variable is referenced but not defined in this scope - ensure
            it's available in the calling context or define it as a class attribute
            - All numeric values are returned as strings to preserve formatting
            - The method gracefully handles IndexError and AttributeError per row
            - Processing continues even if individual rows fail to parse
        """
        soup = self.Online(*args)
        rows = soup.select("ul.flex-row.flex-row-space-between.items-center.w-full.border-xs-b.text-1.c-table-row.cursor-pointer")
        
        currencies_data = []

        if license:
            currencies_data.append(f"extraction time : {datetime.now().isoformat()}")    

        for row in rows:
            try:
                # استخراج نام ارز
                name_span = row.select_one("span.text-1.weight-500")
                currency_name = name_span.get_text(strip=True) if name_span else "N/A"
                
                # استخراج قیمت
                price_span = row.select("li.flex-row-flex-end.family-gilroy-b.table-td span.weight-500")[0]
                price = price_span.get_text(strip=True) if price_span else "N/A"
                
                # استخراج تغییرات 24 ساعته
                change_span = row.select("li.flex-row-flex-end.family-gilroy-b.table-td span.weight-500")[1]
                change = change_span.get_text(strip=True) if change_span else "N/A"
                
                # استخراج حجم معاملات
                volume_div = row.select("li.flex-row-flex-end.family-gilroy-b.table-td div.weight-500")[0]
                volume = volume_div.get_text(strip=True) if volume_div else "N/A"
                
                currencies_data.append({
                    currency_name:{
                        'price': price,
                        'change_24h': change,
                        'volume': volume
                        }
                })
                
            except (IndexError, AttributeError) as e:
                print(f"Error parsing row: {e}")
                continue
        self.currencies_data = currencies_data
        return currencies_data            

    def set(self) -> bool:
        """
        Fetches live market data from Toobit and saves it to a JSON file.

        This method provides a complete end-to-end workflow for data collection and persistence:
        1. Calls Read_code() to fetch and extract market data
        2. Receives structured data as a list of dictionaries
        3. Saves the data to the configured JSON file using dump_file()
        4. Returns a boolean indicating success or failure

        The method is designed for scheduled data collection tasks where you want to
        capture a snapshot of market data at a specific point in time. The data is
        saved with UTF-8 encoding and pretty formatting for human readability.

        Args:
            *args: Variable length argument list passed to Read_code().
                These arguments configure the browser behavior during data fetching:
                - criterion (bool): Run in headless mode (recommended for automation)
                - service_path (str): Custom ChromeDriver path
                - proxy (str): Proxy server configuration
                - user_agent (str): Custom User-Agent string
                - incognito (bool): Private browsing mode
                - lang (str): Language setting
                - disable_images (bool): Disable images for faster loading
                - disable (bool): Disable browser features

        Returns:
            bool: True if the data was successfully fetched AND saved to the JSON file.
                False if any error occurred during fetching or file writing.
                The method catches exceptions internally and returns False on failure.

        Raises:
            This method does not raise exceptions; all errors are caught and result
            in a False return value. Errors are printed to the console for debugging.

        Example:
            >>> market = OnlineMarket("BTCUSDT")
            >>> # Save data with timestamp and headless mode
            >>> success = market.set(
            ...     criterion=True,  # headless mode
            ...     disable_images=True
            ... )
            >>> if success:
            ...     print("Market data saved successfully!")
            ... else:
            ...     print("Failed to save market data")
            Market data saved successfully!

        Notes:
            - The 'license' parameter in the docstring refers to a variable that
            should be defined elsewhere or passed as a configuration option
            - The method does not include timestamp by default unless the 'license'
            variable is defined in the scope
            - The dump_file() function is assumed to handle JSON serialization
            - The file is overwritten on each call (not appended)
            - Recommended to run with headless=True for automated/scheduled tasks
            - Consider adding retry logic if the method frequently returns False
            - The success rate depends on network connectivity and website availability
        """   
        text = self.currencies_data
        return dump_file(self.namefile,text) 
    
    def search_time(self) -> tuple:
        """
        Retrieves the extraction timestamp from the stored market data file.

        This method searches through the loaded JSON data to find the timestamp
        entry that was added when data was saved with the timestamp option enabled.
        It extracts and returns both the full timestamp string and the timestamp
        value for convenient use in logging or data validation.

        The method is useful for:
        - Checking the freshness of stored data
        - Logging when data was collected
        - Validating that data isn't stale
        - Displaying the extraction time to users

        Returns:
            tuple: A tuple containing two elements:
                - First element (str): The full timestamp string as stored in the file.
                Format: "extraction time : 2026-06-28T14:30:45.123456"
                
                - Second element (str): The timestamp value without the label prefix.
                Format: "2026-06-28T14:30:45.123456"
                
                Returns None if no timestamp entry is found in the data file.

        Raises:
            FileNotFoundError: If the configured JSON file does not exist.
            JSONDecodeError: If the JSON file is corrupted or invalid.
            These exceptions are not caught - they propagate to the caller.

        Example:
            >>> market = OnlineMarket("BTC")
            >>> timestamp = market.search_time()
            >>> if timestamp:
            ...     full, value = timestamp
            ...     print(f"Data was extracted at: {value}")
            ...     print(f"Full timestamp entry: {full}")
            ... else:
            ...     print("No timestamp found in data")
            Data was extracted at: 2026-06-28T14:30:45.123456
            Full timestamp entry: extraction time : 2026-06-28T14:30:45.123456

        Notes:
            - The method searches for any string entry that starts with "extraction time"
            - It returns the first timestamp found (should only be one)
            - The timestamp format depends on how it was stored in Read_code()
            - The split operation extracts everything after the first colon
            - If the data was saved without a timestamp, this returns None
            - The timestamp is useful for cache invalidation strategies
            - Consider using this to decide if data needs to be refreshed
        """    
        data = load_file(self.namefile)        
        for Information  in data:
           if isinstance(Information, str):
                return Information , ''.join(Information.split(":")[1:])
        return None      
    
    def search(self, name: str, destination: str = None) -> dict | str:
        """
        Queries the stored market data for a specific currency and optional attribute.

        This method provides a flexible search interface for retrieving previously
        stored cryptocurrency data. It can return either:
        1. The complete data dictionary for a currency (if destination is None)
        2. A specific field value (price, change_24h, or volume) as a string

        The search is performed on the JSON file that was previously saved using
        the set() method. This makes it efficient for repeated queries without
        needing to fetch live data each time.

        Args:
            name (str): The exact currency name/trading pair to search for.
                Must match the key used in the stored data exactly.
                Examples: "BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT"
                The search is case-sensitive - "BTCUSDT" and "btcusdt" are different.

            destination (str, optional): The specific data field to return.
                Valid values are:
                - "price": Returns the current price as a formatted string
                - "change_24h": Returns the 24-hour percentage change
                - "volume": Returns the 24-hour trading volume
                If None (default), returns the complete currency data dictionary.

        Returns:
            dict | str: The returned data depends on the destination parameter:
                - If destination is None: Returns the complete dictionary for the
                currency with all available fields.
                Example: {"price": "42,567.89", "change_24h": "+5.23%", "volume": "1.2B"}
                
                - If destination is specified: Returns the value of that field as
                a string.
                Example: "42,567.89"

        Raises:
            ValueError: If the currency name is not found in the stored data.
                Error message: "The currency name is invalid."
            
            ValueError: If the destination field is specified but not valid for
                the found currency. Error message: "The currency destination is invalid."
                Valid destinations are checked against the available keys in the
                currency's data dictionary.

        Example:
            >>> market = OnlineMarket("BTC")
            >>> # Save data first
            >>> market.set(headless=True)
            
            >>> # Search for complete currency data
            >>> btc_data = market.search("BTCUSDT")
            >>> print(btc_data['price'])
            42,567.89
            
            >>> # Search for specific field
            >>> price = market.search("BTCUSDT", "price")
            >>> print(f"Current BTC price: ${price}")
            Current BTC price: $42,567.89
            
            >>> change = market.search("BTCUSDT", "change_24h")
            >>> print(f"24h change: {change}")
            24h change: +5.23%
            
            >>> # Handle invalid currency
            >>> try:
            ...     data = market.search("INVALID")
            ... except ValueError as e:
            ...     print(f"Search error: {e}")
            Search error: The currency name is invalid.
            
            >>> # Handle invalid destination
            >>> try:
            ...     data = market.search("BTCUSDT", "invalid_field")
            ... except ValueError as e:
            ...     print(f"Search error: {e}")
            Search error: The currency destination is invalid.

        Notes:
            - This method queries the stored JSON file, not the live website
            - Always ensure data is saved first using the set() method
            - The search is performed on the filename specified in self.namefile
            - All data is stored as strings to preserve formatting
            - The method assumes the data structure follows the format from Read_code()
            - For fresh data, call set() before calling search()
            - Consider caching the loaded data if performing multiple searches
            - The search is O(n) where n is the number of entries in the JSON file
            - For large datasets, consider implementing an indexing mechanism
        """      
        data = load_file(self.namefile)        
        for info in data:
            if isinstance(info, dict) and name in info:
                dict_info = info[name]
                if destination is None:
                    return dict_info
                if destination in dict_info:
                    return dict_info[destination]
                raise ValueError("The currency destination is invalid.")
        
        raise ValueError("The currency name is invalid.") 


# -----------------------------
#  Analysis and utility functions

def analyst(market_class: World_Market | Iranian_market, set: bool = True) -> DeepDiff:
    """
    Compares live market data against cached data and returns differences.

    Args:
        market_class (World_Market | Iranian_market): The market class to analyze.
        set (bool): If True, saves fresh data before comparing.

    Returns:
        DeepDiff: Difference object between cached and live data.
    """
    market = market_class()

    dict1 = market.get_currencies()

    market2 = market_class(time=0)
    if set:
        market2.set()
    dict2 = market2.get_currencies()

    diff = DeepDiff(dict1, dict2)
    return diff

def Dollar_to_Rial(dollar: float):
    """
    Converts USD to Iranian Rial using live dollar price.

    Args:
        dollar (float): Amount in USD.

    Returns:
        float: Equivalent in Rials.
    """
    Rial_dollar = int((Iranian_market().search("dollar")[0]).replace(',', ''))
    return dollar * Rial_dollar

def Rial_to_Dollar(Rial : float):
    """
    Converts Iranian Rial to USD using live dollar price.

    Args:
        Rial (float): Amount in Rials.

    Returns:
        float: Equivalent in USD.
    """    
    dollar = int((Iranian_market().search("dollar")[0]).replace(',', ''))
    return Rial // dollar

def Tether_to_Rial(tether: float) -> int:
    """
    Converts Tether (USDT) to Iranian Rial using live Tether price.

    Args:
        tether (float): Amount in Tether.

    Returns:
        int: Equivalent in Rials.
    """    
    Rial = int((Iranian_market().search("Tether")[0]).replace(',', ''))
    return Rial * tether

def Gold_to_Rial(gram: float) -> int:
    """
    Converts grams of gold to Iranian Rial using live gold price.

    Args:
        gram (float): Amount in grams.

    Returns:
        int: Equivalent in Rials.
    """    
    Rial = int((Iranian_market().search("grams of gold")[0]).replace(',', ''))
    return Rial * gram

def Read_price(price : int | float) -> str:
    """
    Formats a number with thousand separators.

    Args:
        price (int | float): The price to format.

    Returns:
        str: Formatted price string.
    """    
    return f"{int(price):,}"

def export_to_csv_iran(filename="prices_iran.csv"):
    """
    Exports Iranian market data to a CSV file.

    Args:
        filename (str): Output CSV filename.

    Returns:
        bool: True if successful, False otherwise.
    """    
    market = Iranian_market()
    data = market.get_currencies()
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['currency', 'price', 'time'])
            
            for key, value in data.items():
                if key != "extraction time":
                    writer.writerow([key, value, data['extraction time']])
    except FileNotFoundError:
        return False
    return True

def export_to_csv_world(filename="prices.csv"):
    """
    Exports world market data to a CSV file.

    Args:
        filename (str): Output CSV filename.

    Returns:
        bool: True if successful, False otherwise.
    """    
    market = World_Market()
    data_mp = market.get_currencies()
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['currency', 'price', 'time'])
            for data in data_mp:
                if isinstance(data, str):
                    data_time = data
                if isinstance(data, dict):
                    for key, value in data.items():
                        writer.writerow([key, value, ''.join(data_time.split(":")[1:])])
    except FileNotFoundError:
        return False
    return True
