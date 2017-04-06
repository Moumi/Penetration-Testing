## php tips

1. XSS : there is no ``htmlspecialcharacter`` on user input. `PHP_SELF` is used in html post forms(check pentest tips for exploit)
2. SQL Inj: use prepare statements and bind parameters
3. Path traversal: clean up the string
4. : php.ini has arguments

  Error messaging
  ````
  ; Disable displaying errors to screen
  display_errors = off
  ; Enable writing errors to server logs
  log_errors = on
  ````

  Remote File Inclusion

  ````
  ; Disable including remote files
  allow_url_fopen = off
  ; Disable opening remote files for include(), require() and include_once() functions.
  ; If above allow_url_fopen is disabled, allow_url_include is also disabled.
  allow_url_include = off
  ````

5. Session
Don't allow session ID if changed. If someone uses your cookie and is in similar domain can pretend to be you.
  * httpOnly : this means that javascript cannot enter the value of the cookie
  * secure : prevents from sending the cookie through unencrypted communication channel

6. Password storing.
For the creation: Hash + salt
For the verification: password_verify

7. File Upload: Be sure to use `file_get_content` instead of `include` because otherwise php can be injected in your php.


## General Fingerprinting Approach
1. Interesting Functionalities :
  * Upload and download functionalities.
  * Authentication forms and links: login, logout, password recovery functions.
  * Administration section.
  * Data entry points: "Leave a comment", "Contact us" forms.
2. Source code comments
3. file extensions can provide info on what kind of application is running
4. robots.txt
5. dirbuster, nikto

## Pentest Tips for WebApps (Mainly PHP)


* Know the HTTP headers
      200 - OK
      302 - Found
      401 - Unauthorized
      404 - Not Found
      500 - Internal Error
* Encoding

| Character 	| URL encoded value 	|
|-----------	|-------------------	|
| \r 	| %0d 	|
| \n 	| %0a 	|
|  	| %20 or `+` 	|
| ? 	| %3f 	|
| & 	| %26 	|
| = 	| %3d 	|
| ; 	| %3b 	|
| # 	| %23 	|
| % 	| %25 	|
* **Cookies**: In PHP you can find the session folder generated with an unencrypted Cookies
````
cat /var/lib/php5/sess_o8d7lr4p16d9gec7ofkdbnhm93
pentesterlab|s:12:"pentesterlab";
````
* **XSS**: Watchout for ``PHP_SELF`` being rendered as a form attribute. This can be exploited by escaping the `Action` html element.
* **SQL Injc**:
 * When spaces are not allowed, you can use comments `/* */`
 * Numerical Injection can work with unions
* **Path Traversal**
  * You can use x00 at the end to remove things the server code appends.
  * You can append the destination to the existing file url if there is some kind of filtering
* **File Inclusion**
  * You can use x00 at the end to remove things the server code appends
* **Code Injection**
  * `Eval`: If this function is used then an example escape mechanism is: **test";system("uname -a");$dummy ="**
  * `preg_replace`: if PHP is below 7.0 you can append `/e` at the end of the pattern. This will cause the new pattern variable to be executed as code.
  * `assert`: When assertion arguments is wrong, it is executed as PHP code
* **Command Injection**
  * Use new line %0A to escape and append commands
  * If nothing happens then maybe the function `header` is used. This means that I can catch the redirect on burp.
* **LDAP** :
 * Always try null based credentials (this case was LDAP). To put null parameters you have to delete them not put them empty
 * Check the filter syntax. Easy to escape


## Other

List of machines:
https://www.owasp.org/index.php/OWASP_Vulnerable_Web_Applications_Directory_Project#tab=Virtual_Machines_or_ISOs


https://pentesterlab.com/exercises/web_for_pentester

https://pentesterlab.com/exercises/web_for_pentester_II

https://pentesterlab.com/exercises/xss_and_mysql_file


General Web App Pentest: https://www.owasp.org/index.php/Web_Application_Penetration_Testing

PHP security cheat sheet: https://www.owasp.org/index.php/PHP_Security_Cheat_Sheet#DRAFT_CHEATSHEET_-_THIS_IS_STILL_A_WORK_IN_PROGRESS_OR_OUT_OF_DATE
