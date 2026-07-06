## EXECUTION FLOW DIAGRAM

```markdown```
# EXECUTION FLOW

PROGRAM START
│
└── if name == "main": main()
│
└── main(speed=20)
│
├── Validate speed (must be in [10, 20, 30, ..., 100])
│
├── Calculate threads = speed // 10
│
└── For each thread (i in range(threads)):
│
└── Thread(target=start, args=(number, path, add))
│
└── start(number, path, add)
│
├── Create Chrome driver (chrome())
│
├── Initialize SiteHandler(driver, number)
│
└── For each iteration (range(add)):
│
├── digimark()
│ ├── Navigate to digimark
│ ├── send_keys() → first input
│ ├── click() → first button
│ └── click(CSS_SELECTOR) → specific button
│
├── get_XPATHS()
│ ├── Navigate to Jabama
│ │ └── XPATH() → click by XPath
│ └── Navigate to Namava
│ └── XPATH() → click by XPath
│
└── urls()
└── For each URL in hrefs:
├── Navigate to URL
├── send_keys() → first input
└── click() → first button

└── (Loop continues for add iterations)

└── driver.quit() → Close browser
text