import * as vscode from 'vscode';
import { platform } from 'os';
const { exec } = require("child_process");
const path = require('path');
const fs = require("fs");

const cwd = path.resolve(__dirname, '../src');
const landingURI = vscode.Uri.file(path.resolve(__dirname, '../landing.md'));
const dsdVenv = path.resolve(cwd, '../../dsd-env');

let format = '-camel';
let discardNext = false;
// when first loading the extension give a default setting
//( or reload setting from a file)
vscode.commands.executeCommand('setContext', 'vocoder:isSnake', false);

//Detect OS
let shell = '';
let ext = '';
let pre = '';
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

const outputChannel = vscode.window.createOutputChannel("vocoder");

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
    if (fs.existsSync(pathh) && shell.includes("conda")) {
        outputChannel.appendLine('Duplicate environment detected: removing venv...');
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
    outputChannel.show(true);

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
            outputChannel.appendLine('--- dsd-env has been detected! ---');
            deleteFolderRecursive(dsdVenv); //Delete duplicate environment
            outputChannel.appendLine('Environment is ready!');
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
                        vscode.window.showInformationMessage('Everything is ready! Let\'s code!');
                    });
                });
            });
            
        }
        console.log(`stdout: ${stdout}`);
    });

    // ------ DISPOSABLE FUNCTIONS -------
	let disposable = vscode.commands.registerCommand('vocoder.captureAudio', () => {
        vscode.commands.executeCommand('setContext', 'vocoder:isRecording', true);
        var scriptName = `${pre}audiorecorder${ext}`;
        recordAudio(scriptName);
    });
    
    let recordConst = vscode.commands.registerCommand('vocoder.recordConst', () => {
        vscode.commands.executeCommand('setContext', 'vocoder:isRecording', true);
        var scriptName = `${pre}audiorecorderConst${ext}`;
        recordAudio(scriptName);
	});

    let toSnake = vscode.commands.registerCommand('vocoder.toSnake', () => {
        vscode.window.showInformationMessage('Switching to Snake Case');
        format = 'snake';
		vscode.commands.executeCommand('setContext', 'vocoder:isSnake', true);
    });

    let toCamel = vscode.commands.registerCommand('vocoder.toCamel', () => {
        vscode.window.showInformationMessage('Switching to Camel Case');
        format = 'camel';
		vscode.commands.executeCommand('setContext', 'vocoder:isSnake', false);
    });
    let discardAudio = vscode.commands.registerCommand('vocoder.discardAudio', () => {
        discardNext = true;
    });

    let fakeButton = vscode.commands.registerCommand('vocoder.fakeButton', () => {}); 
    
    context.subscriptions.push(recordConst);
    context.subscriptions.push(toSnake);
    context.subscriptions.push(toCamel);
    vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', true);
    vscode.commands.executeCommand('setContext', 'vocoder:isRecording', false);
}

// ------ UTILITY FUNCTIONS -------
function recordAudio(scriptName:string){
    outputChannel.appendLine('--- New command ---');
    outputChannel.appendLine('Recording...');
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
                    
                    discardNext ? outputChannel.appendLine('Discarded!') :
                    discardNext ? vscode.window.showWarningMessage('Command has been discarded') : elaborateCommand();
                    discardNext = false;
                    vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', true);
                    vscode.commands.executeCommand('setContext', 'vocoder:isRecording', false);
                });
            });
        });
}

function elaborateCommand(){
    outputChannel.appendLine('Interpreting audio input...');
    exec([`${pre}audiointerpreter${ext}`, format].join(' '), {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
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
        var sections = stdout.split("dsd-section");
        var intent = sections[0].match(/intents.*\}/).toString().match(/name': '[A-Z, a-z, 0-9]*'/).toString().match(/'[A-Z, a-z, 0-9]*'/).toString();
        outputChannel.appendLine('Intent detected: '.concat(intent));
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
    s = s.substring(s.indexOf('\n') + 1);

    // line from which the selection starts: does not depend on which direction the sel is made (start>end)
    const currLine = currSel.start.line;
    //selection of what stays before the selection --> to be used to align
    const currLineBegin = new vscode.Position(currLine,0);
    let alignmentSel = new vscode.Selection(currLineBegin,currSel.start);
    let alignmentString = editor.document.getText(alignmentSel);
    alignmentString = alignmentString.replace(/[^\t.]/g,' '); //if the alignment contains characters we don't want them
    //split lines and align
    let lines = s.split(/\r\n|\r|\n/);
    const writtenLines = lines.length;
    if(alignmentString !== ''){
        for(let i = 1; i < writtenLines; i++){
            lines[i] = alignmentString + lines[i];
        }
    }
    // reconstruct string
    let alignedS = lines[0];
    for(let i = 1; i < writtenLines; i++){
        alignedS = alignedS + '\n' + lines[i]; 
    }
    //write it
    await editor.edit( (edit) => { edit.replace(currSel,alignedS); } );

    // computation of new position of the cursor
    // create a position where to put the cursor: at the end of what just written
    // = last line + last char
    const newEnd = new vscode.Position(currLine + writtenLines - 1, lines[writtenLines-1].length);
    // set the selection to an empty one at the position we defined
    editor.selection = new vscode.Selection(newEnd,newEnd);
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