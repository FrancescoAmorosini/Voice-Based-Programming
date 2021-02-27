# Vocoder: Voice-Based-Programming

### Sponsors 
Fernando Castor, Federal University of Pernambuco, Brazil.

### Project Abstract
Thousands of software developers suffer from repetitive strain injuries such as carpal tunnel syndrome and tendonitis. Support for programming by voice has the potential to increase the productivity of developers afflicted by these problems. In addition, it can enable individuals with upper-body motor impairments, e.g, due to spinal cord injuries or strokes, to write code. In this project, we explore the development of a prototype system to support programming by voice.
 
### Project Description		
VOCODER is a system to support developers in the task of programming by voice. It can be implemented either as a standalone editor or as a plugin to existing IDEs such as Eclipse, Visual Studio Code, or Atom. It should support voice-based programming in the Python programming language. VOCODER should focus on recognizing voice-based input to write procedural (non-object-oriented) programs in Python. 
We envision a scenario where typical programming tasks can be recognized by providing higher-level instructions. More specifically, a useful metaphor for our vision is the following. Consider that one person makes a phone call to another one and instructs the latter on how to write a program on-the-fly. In this scenario, if the caller just provides input character-by-character, that will be tiresome and not productive. On the other hand, if the input is too high level, the callee may misunderstand or not understand what she should do. Achieving this kind of balance is key to successful voice-based programming.
In addition to the aforementioned features, the system should be able to: 
Work reasonably well (this is left purposefully imprecise) without the need for users to provide input character-by-character, as is often the case in real-world voice-based programming systems. 
Identify typical mistakes made by speech recognition systems when dealing with voice-based input in the context of programming, e.g., identifying that a function declaration is initiated by the def keyword, instead of "deaf", "death", or "depth".
Treating identifiers as camel (or snake) case words, e.g., even though the name of a function is input as "function doing something", the system is able to (i) infer that all those words are part of the identifier and (ii) combine them into a single camel case identifier, i.e., functionDoingSomething. Alternatively, it is possible to opt for a snake case instead, i.e., function_doing_something.

### Project Scope
The team should build a system that supports all the functionalities. It should tackle a Python subset consisting of function and variable declarations and expressions (as many as possible). In terms of statements, only return, assignment, and declaration statements are required, although having for loops and if statements is useful. Dealing with lists is also not required. Although navigation is also very important, it is not required for this project. The reasoning is that problems such as repetitive strain injuries are more intensified by the act of writing code than by navigating through it using a keyboard or mouse.
Process Requirements
Teams can use any development process and the choice should be motivated and discussed in the project report. If agile development is adopted, user stories must be created to drive iterations. Third-party code or libraries may be reused, provided reuse is explicitly acknowledged and the reused code uses a compatible license.
Automated tests are not required, due to the nature of the system. However, the team is expected to provide a comprehensive set of (voice-based input, expected program) pairs for testing purposes. 
All project artifacts must be hosted on a public repository, with a version control system and an issue tracker (e.g., GitHub, BitBucket, GitLab). To track the project activity, the teams should adhere to the following rules:
For each iteration or major set of development tasks, a milestone must be defined.
For each task, including user stories, an issue describing it must be defined, within the corresponding milestone.
Task granularity is up to the teams, provided that the corresponding issue can be assigned to a single team member.
The use of branches for working on partial solutions is recommended.
All users must make sure their partial solutions do not break the system (project must compile, tests that passed before must still pass).

### Environmental Constraints
The team is free to choose whatever language and tools they prefer. The only constraint is that no commercial tools or services, e.g., Google's speech recognition service, must be required for the system to work. 

### Project Restrictions
This project has no specific restrictions. It is suggested, however, that machine learning be employed to recognize English utterances of programs. This approach has the upside of being tolerant of imprecision and being able to handle unforeseen cases. The downside is that constructing the dataset to employ such an approach is non-trivial.

### Project License
The suggested license for this project is GPL 3.0. This is not a requirement, however. The team is free to choose any license they deem appropriate, as long as it is a free software license. A comprehensive list of licenses that meet this requirement is available in the following address: https://www.gnu.org/licenses/license-list.en.html  