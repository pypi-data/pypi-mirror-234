<!-- 
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Hex2424/ProxyRipper">
    <img src="./images/logo.png" alt="Logo">
  </a>

<h3 align="center">BeutyPrinter</h3>

  <p align="center">
    A Python library to give beuty to your python scripts printing structure
    <br />
    <!-- <br>
    <a href="https://github.com/Hex2424/ProxyRipper">View Demo</a>
    · -->
    <a href="https://github.com/Hex2424/ProxyRipper/issues">Report Bug</a>
    ·
    <a href="https://github.com/Hex2424/ProxyRipper/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot](images/home.png)

Sometimes we all in hurry and just need simple printing tool just to preview our scripts scraping or processing output in more neat way than just plain text, each time need waste time writing something simple to print neatly, so I wrote this lib almost in all my projects since its meets my needs, I hope it will meet other people needs so I am sharing it with everyone

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With:

* ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Project is uploaded to PYPI, so you can install it pretty easily using pip tool.

### Installation

1. Install package using pip command
   ```sh
   pip install beuty-print
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

To use this library just import classes and create printer object
```python
from beutyprint import *

printer = BeutyPrint()
```
<br>**Setting format:**
<br>Each format is a list of spans, can be defined as here **(default instances)**:

```python
# Each span object represents style applied for each printer word
# Sequentialy, if there will be more words, it will start repeat

format = [
  BeutySpan(),
  BeutySpan(),
  BeutySpan()
]

# Setting default format pattern for printer
printer.setDefaultFormat(format)
```
Then we need to call print function of printer object:
```python
# Takes one string
printer.print("Hello")

# Or string list
printer.print(["Test1", "Test2", "Test3"])
```
**Output:**
```sh
[ Hello ]
[ Test1 ][ Test2 ][ Test3 ]
```

<br>**Configuring Individual span:**
<br>
```python
format = [
  BeutySpan(
    # Text color used in span text
    textColor = Fore.CYAN,
    # Minimum length of span text field
    textPadding = 10,
    # In which direction unused span space will be inserted
    textPaddingDirection = RIGHT,
    # Span background color
    textBackgroundColor = Back.GREEN,
    # Span styles like text style
    textStyle = Style.DIM,
    # Left span seperator string
    l_sep = '[ ',
    # Right span seperator string
    r_sep = ' ]',
    # Default color of span string
    defaultColor = Fore.RED,
    # Advanced function for handling span differently 
    # dependent on message
    postProcessor = functionHandler
  )
]
```
Output looks like this, since we defined only 1 span, it keeps repeating for all messages

![Product Name Screen Shot](images/span_example.png)

<br>**Second example:**
<br>
```python
format = [
  # First pattern element
  BeutySpan(
    textColor = Fore.BLUE,
    textPadding = 10,
    textPaddingDirection = CENTER,
    textStyle = Style.BRIGHT,
    l_sep = '[[-> ',
    r_sep = ' <-]]',
  ),
  # Second pattern element
  BeutySpan(
    textColor = Fore.GREEN,
    textPadding = 10,
    textPaddingDirection = CENTER,
    textStyle = Style.BRIGHT,
    l_sep = '[[-> ',
    r_sep = ' <-]]',
  ),
  # Third pattern element
  BeutySpan(
    textColor = Fore.RED,
    textPadding = 10,
    textPaddingDirection = CENTER,
    textStyle = Style.BRIGHT,
    l_sep = '[[-> ',
    r_sep = ' <-]]',
  )
]
```
**Output:**

![Product Name Screen Shot](images/span_example2.png)



<!-- ROADMAP -->
## Roadmap

- [ ] Generalizing parent span
- [ ] Improve this readme

See the [open issues](https://github.com/Hex2424/ProxyRipper/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Project has flexible python API object inheritence from parent API scrapping object, need more API Endpoints for scrapping in "api" folder, template is ProxyEngine.py file, which is template reference for other classes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

* Discord - Hex24#8712


<p align="right">(<a href="#readme-top">back to top</a>)</p>
