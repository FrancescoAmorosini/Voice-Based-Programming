import * as vscode from 'vscode';
const { exec } = require("child_process");
const path = require('path');

let cwd = path.resolve(__dirname, '../src');
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "vocoder" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('vocoder.captureAudio', () => {
        exec("audiorecorder.cmd", {cwd: path.resolve(cwd, 'bash')}, (error: any, stdout: any, stderr: any) => {
            if (error) {
                console.log(`error: ${error.message}`);
                return;
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                return;
            }
            console.log(`stdout: ${stdout}`);
        });
	});
    
	context.subscriptions.push(disposable);
}

// this method is called when your extension is deactivated
export function deactivate() {}
