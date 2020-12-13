import * as vscode from 'vscode';
import { platform } from 'os';
const { exec } = require("child_process");
const path = require('path');
const fs = require("fs");

const cwd = path.resolve(__dirname, '../src');
const landingURI = vscode.Uri.file(path.resolve(__dirname, '../landing.md'));
const dsdVenv = path.resolve(cwd, '../../dsd-env');

//Detect OS
let shell = platform() === 'win32' ? 'scripts/cmd' : 'scripts/bash';
let ext = platform() === 'win32' ? '.cmd' : '.sh';
let pre = platform() === 'win32' ? '' : './';

const outputChannel = vscode.window.createOutputChannel("vocoder");

<<<<<<< HEAD
=======
//Detect OS
if (platform() === 'win32'){
    shell = 'scripts/cmd'; 
    ext = '.cmd';
}
else{
    shell = 'scripts/bash'; 
    ext = '.sh'; 
    pre = './'; 
    prepareMacScript();
}

>>>>>>> b1042f8248be66777d9fa98cd426dfa2f9ddbf63
//Detect anaconda
let detectConda =new Promise(function (resolve, reject) {
    exec("conda --version", (error:any, stdout:any, stderr:any) => {
        if (stderr){ 
            shell = shell.concat('/venv'); 
            outputChannel.appendLine('WARNING: Anaconda is not installed, the extension will work fine but you may experience performance drops');
            vscode.window.showWarningMessage('We suggest to install Anaconda (or Miniconda) for a better user experience');
        }
        else{
            shell = path.join(shell, 'conda'); 
            outputChannel.appendLine('--- Anaconda has been detected! ---');
        }
        resolve(stdout);
    });
}); 

//Delete duplicate environment
const deleteFolderRecursive = function(pathh:any) {
    if (fs.existsSync(pathh)) {
      fs.readdirSync(pathh).forEach((file:string, index:number) => {
        const curPath = path.resolve(pathh, file);
        if (fs.lstatSync(curPath).isDirectory()) { // recurse
          deleteFolderRecursive(curPath);
        } else { // delete file
          fs.unlinkSync(curPath);
        }
      });
      fs.rmdirSync(pathh);
    }
  };

// ------ PROLOGUE END -------

export async function activate(context: vscode.ExtensionContext) {
    console.log('Activating the extension...');
    
    await detectConda;

    outputChannel.appendLine('Activating vocoder...');

    //Environment check
    exec(`${pre}check${ext}`, {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
        if (error) {
            console.log(`error: ${error.message}`);
            outputChannel.appendLine(error.message);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            outputChannel.appendLine(stderr.message);
            return;
        }
        if (stdout.includes('dsd-env')) {
            deleteFolderRecursive(dsdVenv);
            
            console.log('environment is ready!');
            outputChannel.appendLine('--- dsd-env has been detected! ---');
            vscode.window.showInformationMessage('Everything is ready! Let\'s code!'); 
            
            //Display landing page
            vscode.commands.executeCommand('markdown.showPreview', landingURI);
        }
        else { 
            //Environment setup
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "We are setting up your environment, it might take a few minutes...",
                cancellable: false
            }, (progress, token) => {
                return new Promise((resolve:any) => {
                    exec(`${pre}setup${ext}`, {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
                        if (error) {
                            resolve(`error: ${error.message}`);
                            console.log(`error: ${error.message}`);
                            outputChannel.append(error.message);
                            vscode.window.showErrorMessage('Environment was not loaded successfully');
                            return;
                        }
                        if (stderr) {
                            resolve(`stderr: ${stderr}`);
                            console.log(`stderr: ${stderr}`);
                            outputChannel.append(stderr.message);
                            vscode.window.showErrorMessage('Environment was not loaded successfully');
                            return;
                        }
                        resolve(`stdout: ${stdout}`);
                        outputChannel.appendLine('Modules successfully installed');
                        console.log('Environment is ready!');
                        vscode.window.showInformationMessage('Everything is ready! Let\'s code!');
                    });
                });
            });
            
        }
        console.log(`stdout: ${stdout}`);
    });

    //Disposable functions
	let disposable = vscode.commands.registerCommand('vocoder.captureAudio', () => {
<<<<<<< HEAD
        var scriptName = `${pre}'audiorecorder'${ext}`;
        recordAudio(scriptName);
=======
        vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', false);
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Please, speak your command after the acoustic signal",
            cancellable: false
        }, (progress, token) => {
            return new Promise((resolve:any) => {
                exec(`${pre}audiorecorder${ext}`, {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
                    if (error) {
                        resolve(`error: ${error.message}`);
                        console.log(`error: ${error.message}`);
                        outputChannel.append(error.message);
                        vscode.window.showErrorMessage('Recording failed');
                        return;
                    }
                    if (stderr) {
                        resolve(`stderr: ${stderr}`);
                        console.log(`stderr: ${stderr}`);
                        outputChannel.append(stderr.message);
                        vscode.window.showErrorMessage('Recording failed');
                        return;
                    }
                    console.log(`stdout: ${stdout}`);
                    resolve(`stdout: ${stdout}`);
                    elaborateCommand();
                    vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', true);
                });
            });
        });
>>>>>>> b1042f8248be66777d9fa98cd426dfa2f9ddbf63
    });
    
    let recordConst = vscode.commands.registerCommand('vocoder.recordConst', () => {
        var scriptName = `${pre}'audiorecorderConst'${ext}`;
        recordAudio(scriptName);
	});
    
    // when first loading the extension give a default setting
    //( or reload setting from a file)
    vscode.commands.executeCommand('setContext', 'vocoder:isSnake', false);

    let toSnake = vscode.commands.registerCommand('vocoder.toSnake', () => {
        vscode.window.showInformationMessage('Switching to Snake Case');
        //code to actually change some variable / setting
		vscode.commands.executeCommand('setContext', 'vocoder:isSnake', true);
    });

    let toCamel = vscode.commands.registerCommand('vocoder.toCamel', () => {
        vscode.window.showInformationMessage('Switching to Camel Case');
        //code to actually change some variable / setting
		vscode.commands.executeCommand('setContext', 'vocoder:isSnake', false);
    });
    
    context.subscriptions.push(disposable);
    context.subscriptions.push(recordConst);
    context.subscriptions.push(toSnake);
    context.subscriptions.push(toCamel);
    vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', true);
}

function recordAudio(scriptName:string){
    vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', false);
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Please, speak your command after the acoustic signal",
            cancellable: false
        }, (progress, token) => {
            return new Promise((resolve:any) => {
                exec(`${scriptName}`, {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
                    if (error) {
                        resolve(`error: ${error.message}`);
                        console.log(`error: ${error.message}`);
                        outputChannel.append(error.message);
                        vscode.window.showErrorMessage('Recording failed');
                        return;
                    }
                    if (stderr) {
                        resolve(`stderr: ${stderr}`);
                        console.log(`stderr: ${stderr}`);
                        outputChannel.append(stderr.message);
                        vscode.window.showErrorMessage('Recording failed');
                        return;
                    }
                    console.log(`stdout: ${stdout}`);
                    resolve(`stdout: ${stdout}`);
                    elaborateCommand();
                    vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', true);
                });
            });
        });
}

function elaborateCommand(){
    exec(`${pre}audiointerpreter${ext}`, {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
        if (error) {
            console.log(`error: ${error.message}`);
            vscode.window.showErrorMessage('Audio processing failed');
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            vscode.window.showErrorMessage('Audio processing failed');
            return;
        }
        console.log(`stdout: ${stdout}`);
        
        var sections = waitforOut(stdout);
        const vocoderSec = sections[1];
        
        if(vocoderSec.includes("vocoder-undo")){
            vscode.commands.executeCommand("undo");
            return;
        }
        if(vocoderSec.includes("vocoder-delete")){
            writeOnEditor('');
            return;
        }
        const codeSec = vocoderSec.split("vocoder-code-block");
        if(codeSec.length!==2){
            console.log(`Bad format from backend processing: no command or code-block section found`);
            vscode.window.showErrorMessage('Code processing failed');
            return;
        }
        writeOnEditor(codeSec[1]);
    });
}

async function writeOnEditor(s: string){
    
    const editor = vscode.window.activeTextEditor;
    if(!editor){
        vscode.window.showWarningMessage('No editor available to write on');
        return;
    }
    const currSel = editor.selection;
    s = s.substring(s.indexOf('\r\n') + 2, s.lastIndexOf('\r\n'));
    if(currSel.start.character === 0){
        s = s.substring(s.indexOf('\n') + 1);
    }
    await editor.edit( (edit) => { edit.replace(currSel,s);} );

    // computation of new position of the cursor

    // line from which the selection starts: does not depend on which direction the sel is made (start>end)
    const currLine = currSel.start.line;
    const writtenLines = s.split(/\r\n|\r|\n/).length;
    // create a position where to put the cursor: at the end of what just written
    const newEnd = new vscode.Position(currLine + writtenLines - 1,0);
    // set the selection to an empty one where defined
    editor.selection = new vscode.Selection(newEnd,newEnd);
}

let retries = 0;
function waitforOut(output:any) {
    if(!output.includes('dsd-section') && retries < 15) {
        ++retries;
        setTimeout(waitforOut, 100, [output, retries]);
        return;
    }
    else if(retries >= 15){
        retries = 0;
        console.log(`Bad format from backend processing: no dsd-section found or more than one found`);
        vscode.window.showErrorMessage('Code processing failed');
        return;
    }
    return output.split("dsd-section");
}

// this method is called when your extension is deactivated
export function deactivate() {}

async function prepareMacScript(){
    await exec(`python macscriptcreator.py ${path.resolve(cwd, shell)}`, {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
        if (error) {
            console.log(`Writing mac scritp failed`);
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`Writing mac scritp failed`);
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`Mac script written`);
    });
    let cPath = shell.concat('/conda');
    await exec(`chmod +x audioRecorderConst.sh`, {cwd: path.resolve(cwd, cPath)}, (error: any, stdout: any, stderr: any) => {
        if (error) {
            console.log(`Giving executable permission failed`);
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`Giving executable permission failed`);
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`Executable permissions granted to created script`);
    });
}