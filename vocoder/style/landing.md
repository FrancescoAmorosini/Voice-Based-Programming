# Welcome to Vocoder!

![Vocoder logo](logo.png)

***
## Terms and Contitions **⚠️** 
 - Vocoder relies on speech recognition services provided by Wit.ai. Availability of Vocoder’s functionalities strictly depends on Wit.ai’s availability which is not under Vocoder’s control.
- Vocoder will not share any sensible data with Wit.ai. Voice commands are recorded locally and sent to Wit.ai anonymously for the sole purposes of recognition and training of the underlying recognition model.
- Vocoder is not responsible for any inappropriate usage of voice recordings by Wit.ai. Please refer to their [Terms of Service](https://wit.ai/terms) for further information.
***
## Prerequisites
Vocoder is currently available for `Python` language, which should be properly installed and set up in Visual Studio Code. If you don't have it, you can get it on [Python's official website](https://www.python.org/downloads/) for free.
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

  When declaring a variable without any expression assigned to it, `None` will be assigned as default.

* Assignment
  > **Assign** _expression_  **to**  _variable_name_

  > **Assign** _variable_name_ **equals** _expression_

  > **Assign** _variable_name_ **the value** _expression_

* Expressions
  > **Insert expression** _expression_

  > **Expression** _expression_

  The command is thought for the programmer to be able to update assignments when coding, or to later input pieces of code like loop/if conditions.

* Comment
  > **Add comment** _text_

  > **Create comment** _text_

* If statement
  > **Create if statement**

  > **If** _expression_ **then** _command_

  When creating a non-empty if statement it is possible to input the first instruction within the statement. Note that it cannot be another if based statement.

* If-else statement
  > **Create if else statement**

  > **If** _expression_ **then** _command_ **else** _command_

  When creating a non-empty if-else statement it is possible to input the first instruction within the then and else sections. Note that it cannot be another if based statement.

* While loop
  > **Create while loop**

  > **Create while loop until** _expression_

  > **While** _expression_

* For loop
  > **Create for loop**

  > **Create for loop with** _variable_name_ **in** _variable_name_

  > **Create for loop with** _variable_name_ **in range from** _expression_ **to** _expression_

* Function definition
  > **Create function** _function_name_

  > **Define function** _function_name_

  > **Create function** _function_name_ **with parameters** _parameter_1_ **comma** _parameter_2_

* Function call
  > **Call function** _function_name_

  > **Call function** _function_name_ **with parameters** _parameter_1_ **comma** _parameter_2_

* Return statement
  > **Return**

  > **Return** _expression_

### Editing Commands
* Undo
  > **Undo**

  > **Undo** _number_ **times**

  Allows you to revert the specified number of last actions, both when it is a voice command and when it is keyboard input.

* Redo
  > **Redo**

  > **Redo** _number_ **times**

  Allows you to redo the specified number of undone actions.

* Delete
  > **Delete**
  
  > **Delete from line** _number_ **to line** _number_

  Deletes the selected text in the editor in the first case, the specified lines in the second. If text is selected when specifying line ranges, the latter will have priority.
### Tutorial
Here you can find a demo that shows how to use VOCODE:

[![Tutorial](https://i9.ytimg.com/vi/VJDOLsqvzjY/mq1.jpg?sqp=CNzZ74MG&rs=AOn4CLBBCf_FQrBRyfQ80GxyjKH-QyRl6Q)](https://www.youtube.com/watch?v=VJDOLsqvzjY) 