import * as vscode from 'vscode';
import { platform } from 'os';
const { exec } = require("child_process");
const path = require('path');

const cwd = path.resolve(__dirname, '../src');
const landingURI = vscode.Uri.file(path.resolve(__dirname, '../landing.md'));

let shell = '';
let ext = '';
let pre = '';

const outputChannel = vscode.window.createOutputChannel("vocoder");

//Detect OS
if (platform() === 'win32'){
    shell = 'scripts/cmd'; 
    ext = '.cmd';
}
else{
    shell = 'scripts/bash'; 
    ext = '.sh'; 
    pre = './'; 
}

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
        resolve();
    });
}); 

// ------ PROLOGUE END -------

export async function activate(context: vscode.ExtensionContext) {
    console.log('Activating the extension...');
    
    await detectConda;

    outputChannel.appendLine('Activating vocoder...');
    //outputChannel.show();

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
                    //writeOnEditor(stdout); //to be removed
                    elaborateCommand();
                });
            });
        });
	});
    
	context.subscriptions.push(disposable);
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
    s = s.substring(s.indexOf('\r\n') + 2, s.lastIndexOf('\r\n'));
    const editor = vscode.window.activeTextEditor;
    if(!editor){
        vscode.window.showWarningMessage('No editor available to write on');
        return;
    }
    const currSel = editor.selection;
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
