# Vocoder: Voice-Based-Programming

### Sponsors 
Fernando Castor, Federal University of Pernambuco, Brazil.

### Project Scope
Thousands of software developers suffer from repetitive strain injuries such as carpal tunnel syndrome and tendonitis. Support for programming by voice has the potential to increase the productivity of developers afflicted by these problems. In addition, it can enable individuals with upper-body motor impairments, e.g, due to spinal cord injuries or strokes, to write code. In this project, we explore the development of a prototype system to support programming by voice.
 
### Project Description		
Vocoder is an application that intends to help software developers by providing them with the possibility of programming using their voice.

Carpal tunnel syndrome and tendonitis are painful conditions very common among software developers, as they are caused by overstressing certain tendons with repetitive actions (for example typing on a keyboard).
Using Natural Language Processing, we were able to build a Visual Studio Code extension that is able to write in the editor your vocal Python commands, so that any user affected by such conditions can recover from his/her strain injury without a significant drop in productivity.

VOCODER has been developed thanks to the joint efforts of six students, three from Politecnico di Milano and three from Mälardalens högskola, and is currently attending the SCORE21 competition @ICSEconf.

Full project assignment: https://docs.google.com/document/d/1ly9NTnhpajnhPrgtFI8vu0EJ9nhfC0wtdk1QYEIhB5U/edit

### Terms and Contitions **⚠️** 
 - Vocoder relies on speech recognition services provided by Wit.ai. Availability of Vocoder’s functionalities strictly depends on Wit.ai’s availability which is not under Vocoder’s control.
- Vocoder will not share any sensible data with Wit.ai. Voice commands are recorded locally and sent to Wit.ai anonymously for the sole purposes of recognition and training of the underlying recognition model.
- Vocoder is not responsible for any inappropriate usage of voice recordings by Wit.ai. Please refer to their [Terms of Service](https://wit.ai/terms) for further information.
***
## Prerequisites
Vocoder is currently available for `Python` language, which should be properly installed and set up in Visual Studio Code. If you don't have it, you can get it on [Python's official website](https://www.python.org/downloads/) for free.
### Performance
We also **suggest** you to have `conda` installed on your machine. This will allow Vocoder to work on a virtual environment with noticeably better time performances, with respect to any virtual environment created by the default tools availble on your machine (i.e Python3's `venv`). You can get `anaconda`, or its lighter version `miniconda`, for free on [conda's official website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html).
