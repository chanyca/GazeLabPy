# GazeLabPy
**Development Status: 🚧 Under Development**  

  
GazeLabPy is a research toolkit for getting real-time eye-tracking data from Pupil Neon and updating stimulus location based on gaze coordinates. It provides tools to set up a simple experiment using Psychopy, conversion between visual degree and pixel, designed to streamline experiments involving real-time gaze-contingent stimulus presentation.  

---
### Getting Started
#### Prerequisites
Note: It is recommended to install the requirements into a [virtual environment](https://docs.python.org/3/tutorial/venv.html).
- [PsychoPy](https://psychopy.org/?_gl=1*f13w9b*_ga*OTM0MzEyODMzLjE3MzE5NjA2NTA.*_ga_96LHQFPY1F*MTczMTk2MDY1Ni4xLjAuMTczMTk2MDY1Ni4wLjAuMA..)  
  ```
  pip install psychopy
  ```
- [Pupil](https://github.com/pupil-labs/pupil)  
  I copied these from their README (linked above). Follow the instructions here or on their repo as you wish.
  ```
  git clone https://github.com/pupil-labs/pupil.git
  cd pupil
  git checkout develop
  python -m pip install -r requirements.txt
  ```
- [Pupil Labs Real-Time API](https://github.com/pupil-labs/realtime-python-api) and [Real-time Screen Gaze](https://github.com/pupil-labs/real-time-screen-gaze) Python packages
  ```
  pip install pupil-labs-realtime-api
  pip install real-time-screen-gaze
  ```
  
 
#### Tested on:


#### Installation
1. Clone this repository:  
```
    git clone https://github.com/chanyca/GazeLabPy.git
```

---
### Key functions


---
# System compatibility & tests

| **OS**                                 |**Python Version** | **Tested & Works**        |
|----------------------------------------|-------------------|---------------------------|
| Windows 11                             | 3.8               | Yes ✅                   |
| Windows 10                             | 3.9               | Yes ✅                   |

---
### Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements, bug fixes, or other suggestions.

---
### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
