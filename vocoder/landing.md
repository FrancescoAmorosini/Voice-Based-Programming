# Welcome to Vocoder!

![Vocoder logo](style/logo.png)

***
## Terms and Contitions **⚠️** 
 - Vocoder relies on speech recognition services provided by Wit.ai. Availability of Vocoder’s functionalities strictly depends on Wit.ai’s availability which is not under Vocoder’s control.
- Vocoder will not share any sensible data with Wit.ai. Voice commands are recorded locally and sent to Wit.ai anonymously for the sole purposes of recognition and training of the underlying recognition model.
- Vocoder is not responsible for any inappropriate usage of voice recordings by Wit.ai. Please refer to their [Terms of Service](https://wit.ai/terms) for further information.
***

## Why voice-based programming?
Thousands of software developers suffer from repetitive strain injuries such as carpal tunnel syndrome and tendonitis. Support for programming by voice has the potential to increase the productivity of developers afflicted by these problems. In addition, it can enable individuals with upper-body motor impairments, e.g, due to spinal cord injuries or strokes, to write code.

Vocoder is a Visual Studio Code extension that intends to help injured programmers by allowing them to code with their voice.

## Prerequisites
For Vocoder to work properly you will need to have `npm` installed on your machine. If you don't, you can get it on [npm's official website](https://www.npmjs.com/get-npm) for free.
### Performance
We also suggest you to have `conda` installed on your machine. This will allow Vocoder to work on a virtual environment with noticeably better time performances, with respect to any virtual environment created by the default tools availble on your machine (i.e Python3's `venv`). You can get `anaconda`, or its lighter version `miniconda`, for free on [conda's official website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html).

## Available languages
Vocoder is currently able to support voice-based programming for Python code. Make sure to be working on a `.py` file in order to activate the extension.

## Usage
Vocoder has a simple and intuitive interface. To input any voice command you just need to:

* Place your **_cursor_** where you want the action to be taken
* Press the **_michrophone icon_** in the upper right corner of the editor
* Wait for the **_beep_** acoustic signal 
* **_Say_** your command

That's it!

You can also choose the naming convention you prefer by toggling the snake-camel button on the upper right of the editor to have your identifiers formatted in `camelCase` or in `snake_case`

## Available Commands
Vocoder provides a set of coding commands as well as a few editing commands that may be useful when programming. Its underlying machine-learning approach allows you to have few alternatives to input the same command. Here you have all available commands with examples of usage.

### Coding Commands
Place the cursor where you want your next code block to be inserted. You can also select a piece of your code to be replaced by the next inputed command.

* Variable declaration: 
  > **Declare** _variable_name_

  > **Declare** _variable_name_ **equals** _expression_

* Assignment
  > **Assign** _expression_  **to**  _variable_name_

  > **Assign** _variable_name_ **equals** _expression_

  > **Assign** _variable_name_ **the value** _expression_

* Comment
  > **Add comment** _text_

  > **Create comment** _text_

* If statement
  > **Create if statement**

  > **If** _expression_ _comparison_ _expression_ **then** _command_

  > **If** _expression_ **then** _command_

  When creating a non-empty if statement it is possible to input the first instruction within the statement. Note that it cannot be another if based statement.

* If-else statement
  > **Create if else statement**

  > **If** _expression_ _comparison_ _expression_ **then** _command_ **else** _command_

  > **If** _expression_ **then** _command_ **else** _command_

  When creating a non-empty if-else statement it is possible to input the first instruction within the statement. Note that it cannot be another if based statement.

* While loop
  > **Create while loop**

  > **Create while loop until** _expression_ _comparison_ _expression_

  > **Create while loop until** _expression_

  > **While** _expression_ _comparison_ _expression_ 

  > **While** _expression_

* For loop
  > **Create fors loop**

  > **Create for loop with** _variable_name_ **in** _variable_name_

  > **Create for loop with** _variable_name_ **in range from** _expression_ **to** _expression_


### Editing Commands
* Undo
  > **Undo**

  Allows you to revert the last action, both when it is a voice command and when it is keyboard input.

* Delete
  > **Delete**
  
  Deletes the selected text in the editor
