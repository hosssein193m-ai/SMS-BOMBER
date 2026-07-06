# ERROR HANDLING MATRIX

| Error Type | Location | Handling | Recovery |
|------------|----------|----------|----------|
| ImportError | Selenium imports | Logs error, raises exception | Install selenium |
| ValueError | add > 11 | Raises ValueError | Reduce add value |
| ValueError | speed not valid | Raises ValueError | Use valid speed |
| ValueError | speed > 100 | Raises ValueError | Reduce speed |
| TimeoutException | ec() function | WebDriverWait timeout | Element not found |
| WebDriverException | chrome() init | Propagates up | Check ChromeDriver |
| Any Exception | start() loop | Finally block closes browser | Safe cleanup |

## Common Errors and Solutions

### Error: WebDriverException: Message: unknown error: cannot find Chrome binary
**Solution**: Install Chrome browser or specify Chrome binary path

### Error: WebDriverException: Message: chrome not reachable
**Solution**: Ensure ChromeDriver version matches Chrome version

### Error: TimeoutException: Message: 
**Solution**: Increase wait time or check if element selector is correct

### Error: NoSuchElementException: 
**Solution**: Update selectors (ID, XPath, CSS) based on website changes