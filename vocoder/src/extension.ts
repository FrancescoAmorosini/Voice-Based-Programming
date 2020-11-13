import * as vscode from 'vscode';
const { exec } = require("child_process");
const path = require('path');
const cwd = path.resolve(__dirname, '../src');

let shell = '';
let ext = '';
let pre = '';

let detectOS =  new Promise(function (resolve, reject) {
                    exec("ls", (error: any, stdout: any, stderr: any) => {
                        if (stderr) { shell = 'scripts/cmd'; ext = '.cmd'; }
                        else { shell = 'scripts/bash'; ext = '.sh'; pre = './'; }
                        resolve();
                    });
                });

export async function activate(context: vscode.ExtensionContext) {
    console.log('Activating the extension...');

    //Waiting completion of OS detection
    await detectOS;

    //Environment setup
    exec(`${pre}check${ext}`, {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        if (stdout.includes('dsd-end')) {
            console.log('environment is ready!');
            vscode.window.showInformationMessage('Everything is ready! Let\'s code!');
            
        }
        else {
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
                            vscode.window.showErrorMessage('Environment was not loaded successfully');
                            return;
                        }
                        if (stderr) {
                            resolve(`stderr: ${stderr}`);
                            console.log(`stderr: ${stderr}`);
                            vscode.window.showErrorMessage('Environment was not loaded successfully');
                            return;
                        }
                        resolve(`stdout: ${stdout}`);
                        console.log('environment is ready!');
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
            title: "Recording...",
            cancellable: false
        }, (progress, token) => {
            return new Promise((resolve:any) => {
                exec(`${pre}audiorecorder${ext}`, {cwd: path.resolve(cwd, shell)}, (error: any, stdout: any, stderr: any) => {
                    if (error) {
                        resolve(`error: ${error.message}`);
                        console.log(`error: ${error.message}`);
                        vscode.window.showErrorMessage('Recording failed');
                        writeOnEditor(error.message); //to be moved --> here is the only place where I (Serena) can see a result
                        return;
                    }
                    if (stderr) {
                        resolve(`stderr: ${stderr}`);
                        console.log(`stderr: ${stderr}`);
                        vscode.window.showErrorMessage('Recording failed');
                        return;
                    }
                    console.log(`stdout: ${stdout}`);
                    resolve(`stdout: ${stdout}`);
                });
            });
        });
	});
    
	context.subscriptions.push(disposable);
}

function writeOnEditor(s: string){
    const editor = vscode.window.activeTextEditor;
		if(!editor){
			vscode.window.showWarningMessage('No editor available to write on');
			return;
		}
		const position = editor.selection.active;
		editor.edit( (edit) => { edit.insert(position,s)} );
}

// this method is called when your extension is deactivated
export function deactivate() {}
