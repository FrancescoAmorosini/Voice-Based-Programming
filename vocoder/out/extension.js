"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const os_1 = require("os");
const { exec } = require("child_process");
const path = require('path');
const fs = require("fs");
const cwd = path.resolve(__dirname, '../out');
const landingURI = vscode.Uri.file(path.resolve(__dirname, '../style/landing.md'));
const dsdVenv = path.resolve(cwd, '../../dsd-env');
const outputChannel = vscode.window.createOutputChannel("Vocoder");
let format = '-camel';
let discardNext = false;
let placeholders = new Map([]);
vscode.commands.executeCommand('setContext', 'vocoder:isSnake', false);
vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', true);
vscode.commands.executeCommand('setContext', 'vocoder:isRecording', false);
//Detect OS
let shell = '';
let ext = '';
let pre = '';
os_1.platform() === 'win32' ?
    (shell = 'scripts/cmd', ext = '.cmd') :
    (shell = 'scripts/bash', ext = '.sh', pre = './', prepareMacScript());
//Detect anaconda
let detectConda = new Promise(function (resolve, reject) {
    exec("conda --version", (error, stdout, stderr) => {
        if (stderr) {
            shell = shell.concat('/venv');
            outputChannel.appendLine('WARNING: Anaconda is not installed, the extension will work fine but you may experience performance drops');
            vscode.window.showWarningMessage('We suggest to install Anaconda (or Miniconda) for a better user experience');
        }
        else {
            shell = path.join(shell, 'conda');
            outputChannel.appendLine('--- Anaconda has been detected! ---');
        }
        resolve(stdout);
    });
});
//Delete duplicate environment
const deleteFolderRecursive = function (pathh) {
    if (fs.existsSync(pathh)) {
        fs.readdirSync(pathh).forEach((file, index) => {
            const curPath = path.resolve(pathh, file);
            if (fs.lstatSync(curPath).isDirectory()) { // recurse
                deleteFolderRecursive(curPath);
            }
            else { // delete file
                fs.unlinkSync(curPath);
            }
        });
        fs.rmdirSync(pathh);
    }
};
// ------ PROLOGUE END -------
function activate(context) {
    return __awaiter(this, void 0, void 0, function* () {
        console.log('Activating the extension...');
        outputChannel.show(true);
        yield detectConda;
        outputChannel.appendLine('Activating vocoder...');
        //Environment check
        exec(`${pre}check${ext}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
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
                //Detect and Delete duplicate environment
                if (shell.includes("conda") && fs.existsSync(dsdVenv)) {
                    outputChannel.appendLine('Duplicate environment detected: removing venv...');
                    deleteFolderRecursive(dsdVenv);
                }
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
                    return new Promise((resolve) => {
                        exec(`${pre}setup${ext}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
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
        let record = vscode.commands.registerCommand('vocoder.captureAudio', () => {
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
            format = '-snake';
            vscode.commands.executeCommand('setContext', 'vocoder:isSnake', true);
        });
        let toCamel = vscode.commands.registerCommand('vocoder.toCamel', () => {
            vscode.window.showInformationMessage('Switching to Camel Case');
            format = '-camel';
            vscode.commands.executeCommand('setContext', 'vocoder:isSnake', false);
        });
        let discardAudio = vscode.commands.registerCommand('vocoder.discardAudio', () => {
            discardNext = true;
            vscode.window.showWarningMessage('Current recording will be discarded');
        });
        let fakeButton = vscode.commands.registerCommand('vocoder.fakeButton', () => { });
        context.subscriptions.push(recordConst);
        context.subscriptions.push(toSnake);
        context.subscriptions.push(toCamel);
    });
}
exports.activate = activate;
// ------ UTILITY FUNCTIONS -------
function recordAudio(scriptName) {
    outputChannel.appendLine('--- New command ---');
    outputChannel.appendLine('Recording...');
    vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', false);
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Please, speak your command after the acoustic signal",
        cancellable: false
    }, (progress, token) => {
        return new Promise((resolve) => {
            exec(`${scriptName}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
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
                discardNext ? outputChannel.appendLine('Command has been discarded!') : elaborateCommand();
                discardNext = false;
                vscode.commands.executeCommand('setContext', 'vocoder:isKeybindingPressed', true);
                vscode.commands.executeCommand('setContext', 'vocoder:isRecording', false);
            });
        });
    });
}
function elaborateCommand() {
    outputChannel.appendLine('Interpreting audio input...');
    exec([`${pre}audiointerpreter${ext}`, format].join(' '), { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
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
        var sections = stdout.split("dsd-section\r\n");
        var intent = sections[0].match(/intents.*\}/).toString().match(/name': '[A-Z, a-z, 0-9]*'/).toString().match(/'[A-Z, a-z, 0-9]*'/).toString();
        outputChannel.appendLine('Intent detected: '.concat(intent));
        const vocoderCommand = sections[sections.length - 1].split("vocoder-parsed-command\r\n")[1];
        const vocoderMessages = sections[sections.length - 1].split("vocoder-parsed-command\r\n")[0];
        if (vocoderMessages.includes("vocoder-error")) {
            const message = vocoderMessages.split("vocoder-error")[1];
            vscode.window.showErrorMessage(message);
            return;
        }
        if (vocoderMessages.includes("vocoder-warning")) {
            const message = vocoderMessages.split("vocoder-warning")[1];
            outputChannel.appendLine("Warning:" + message);
        }
        if (vocoderCommand.includes("vocoder-undo")) {
            var num = parseInt(vocoderCommand.match(/[0-9]+/));
            if (isNaN(num)) {
                num = 1;
            }
            for (var i = 0; i < num; i++) {
                vscode.commands.executeCommand("undo");
            }
            return;
        }
        if (vocoderCommand.includes("vocoder-redo")) {
            var num = parseInt(vocoderCommand.match(/[0-9]+/));
            if (isNaN(num)) {
                num = 1;
            }
            for (var i = 0; i < num; i++) {
                vscode.commands.executeCommand("redo");
            }
            return;
        }
        if (vocoderCommand.includes("vocoder-delete")) {
            deleteFromEditor(false, 0, 0);
            return;
        }
        if (vocoderCommand.includes("vocoder-line-delete")) {
            let lines = vocoderCommand.split("vocoder-line-delete\r\n");
            if (lines.length !== 2) {
                console.log(`Bad format from backend processing: incorrect specification of lines`);
                vscode.window.showErrorMessage('Code processing failed');
                return;
            }
            lines = lines[1].split(/\r\n|\r|\n/);
            deleteFromEditor(true, parseInt(lines[0]), parseInt(lines[1]));
            return;
        }
        const codeSec = vocoderCommand.split("vocoder-code-block\r\n");
        if (codeSec.length !== 2) {
            console.log(`Bad format from backend processing: no command or code-block section found`);
            vscode.window.showErrorMessage('Code processing failed');
            return;
        }
        writeOnEditor(codeSec[1]);
    });
}
function writeOnEditor(s) {
    return __awaiter(this, void 0, void 0, function* () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No editor available to write on');
            return;
        }
        const currSel = editor.selection;
        // line from which the selection starts: does not depend on which direction the sel is made (start>end)
        const currLine = currSel.start.line;
        //selection of what stays before the selection --> to be used to align
        const currLineBegin = new vscode.Position(currLine, 0);
        let alignmentSel = new vscode.Selection(currLineBegin, currSel.start);
        let alignmentString = editor.document.getText(alignmentSel);
        alignmentString = alignmentString.replace(/[^\t.]/g, ''); //if the alignment contains characters we don't want them
        //split lines and align
        let lines = s.split(/\r\n|\r|\n/);
        const writtenLines = lines.length;
        if (alignmentString !== '') {
            for (let i = 1; i < writtenLines; i++) {
                lines[i] = alignmentString + lines[i];
            }
        }
        // reconstruct string
        let alignedS = '';
        let newStart;
        let newEnd;
        for (let i = 0; i < writtenLines; i++) {
            i === 0 ?
                alignedS = lines[i] :
                alignedS = alignedS + '\n' + lines[i];
            if (lines[i].includes('$$')) {
                const index = getPlaceholderPos(lines[i]);
                newStart = new vscode.Position(currLine + i, index);
                newEnd = new vscode.Position(currLine + i, index + 2);
            }
        }
        //write it
        yield editor.edit((edit) => { edit.replace(currSel, alignedS); })
            .then(success => {
            if (newStart !== undefined) {
                editor.selection = new vscode.Selection(newStart, newEnd);
            }
            else {
                const newEnd = new vscode.Position(currLine + writtenLines - 1, lines[writtenLines - 1].length);
                // set the selection to an empty one at the position we defined
                editor.selection = new vscode.Selection(newEnd, newEnd);
            }
        });
    });
}
function deleteFromEditor(lines, start, end) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No editor where to delete');
        return;
    }
    let toDelete;
    if (lines) {
        if (start <= 0) {
            start = 1;
        }
        const maxLines = editor.document.lineCount;
        if (end > maxLines) {
            end = maxLines;
        }
        const startPos = new vscode.Position(start - 2, 0);
        const endPos = new vscode.Position(end - 2, 0);
        toDelete = new vscode.Selection(startPos, endPos);
    }
    else {
        toDelete = editor.selection;
    }
    editor.edit((edit) => { edit.replace(toDelete, ''); });
}
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
function getPlaceholderPos(s) {
    var regex = /\$\$/g, result, index = 0;
    while ((result = regex.exec(s))) {
        index = result.index;
    }
    return index;
}
function prepareMacScript() {
    return __awaiter(this, void 0, void 0, function* () {
        grantMacExecutablePermission('/conda', 'check.sh');
        grantMacExecutablePermission('/venv', 'check.sh');
        grantMacExecutablePermission('/conda', 'setup.sh');
        grantMacExecutablePermission('/venv', 'setup.sh');
        grantMacExecutablePermission('/conda', 'audiointerpreter.sh');
        grantMacExecutablePermission('/venv', 'audiointerpreter.sh');
        grantMacExecutablePermission('/conda', 'audiorecorderActivator.sh');
        grantMacExecutablePermission('/venv', 'audiorecorderActivator.sh');
        grantMacExecutablePermission('/conda', 'audiorecorderConstActivator.sh');
        grantMacExecutablePermission('/venv', 'audiorecorderConstActivator.sh');
        yield exec(`python macscriptcreator.py ${path.resolve(cwd, shell)}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
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
            grantMacExecutablePermission('/conda', 'audioRecorderConst.sh');
            grantMacExecutablePermission('/venv', 'audioRecorderConst.sh');
            grantMacExecutablePermission('/conda', 'audioRecorder.sh');
            grantMacExecutablePermission('/venv', 'audioRecorder.sh');
        });
    });
}
function grantMacExecutablePermission(folder, file) {
    let cPath = shell.concat(folder);
    exec(`chmod +x ${file}`, { cwd: path.resolve(cwd, cPath) }, (error, stdout, stderr) => {
        if (error) {
            console.log(`Giving executable permission to ${folder}/${file} failed`);
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`Giving executable permission to ${folder}/${file} failed`);
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`Executable permissions granted to ${folder}/${file}`);
    });
}
//# sourceMappingURL=extension.js.map