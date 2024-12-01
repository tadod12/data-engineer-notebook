# Data Visualization
## Working With APIs

1. GitHub's API
    
    https://api.github.com/search/repositories?q=language:python&sort=stars
    // Returns the number of Python projects currently hosted on GitHub

2. Install Requests
    ```
   python -m pip install --user requests
   ```

3. Monitoring API Rate Limits
    https://api.github.com/rate_limit
    // Limit how many requests you can make in a certain amount of time
    
    ```
   --snip--
   "search": {
     "limit": 10,  # 10 requests per minute
     "remaining": 8,  # 8 requests remaining for the current minute
     "reset": 1721614436,  # in Unix/epoch time (the number of seconds since midnight January 1, 1970)
     "used": 0,
     "resource": "search"
   }
   ```
   > Many APIs require you to register and obtain an API key to make API calls. As of this writing, GitHub has no such requirement, but if you obtain an API key, your limits will be much higher.

