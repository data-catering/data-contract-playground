import {setJsonSchema, setupEditorSession} from "./util.js";
import {applyInitialTheme, initThemeToggle} from "./theme.js";
import {dataContractSpecificationDetails, defaultJsonSchemaName, odcsDetails} from "./config.js";

const jsonSchemaMap = new Map()
jsonSchemaMap.set("odcs", odcsDetails)
jsonSchemaMap.set("dataContractSpecification", dataContractSpecificationDetails)
const jsonSchemaExampleMap = new Map()
const defaultInputMode = "sql"


let provider = LanguageProvider.fromCdn("https://cdn.jsdelivr.net/npm/ace-linters/build")
let editorInput = ace.edit("input-yaml")
let editorOutput = ace.edit("output-text")

async function initOutputAceEditor() {
    ace.require("ace/ext/language_tools")
    setupEditorSession(editorOutput, "ace/mode/yaml")
    await setJsonSchema(jsonSchemaMap, jsonSchemaExampleMap, editorOutput, provider, defaultJsonSchemaName)
}

async function initInputAceEditor() {
    setupEditorSession(editorInput, `ace/mode/${defaultInputMode}`)
}

function initInputSchemaListener() {
    const selectSchema = document.getElementById("convert-input-type")

    selectSchema.addEventListener("change", function () {
        const inputOption = document.getElementById(`input-${this.value}`)
        const editorMode = inputOption.getAttribute("editor_mode")
        editorInput.session.setMode(`ace/mode/${editorMode}`)
        //get example from 'input_examples' (set from create.py) and set it as current value
        editorInput.session.setValue(input_examples.get(this.value))
    }, false)
}

function initOutputSchemaListener() {
    const selectSchema = document.getElementById("convert-output-type")

    selectSchema.addEventListener("change", async function () {
        console.log("selectSchema.addEventListener", this.value)
        const outputOption = document.getElementById(`output-${this.value}`)
        const editorMode = outputOption.getAttribute("editor_mode")
        
        // Reinitialize the entire editor session
        editorOutput = ace.edit("output-text")
        setupEditorSession(editorOutput, `ace/mode/${editorMode}`)
        
        const schemaDetails = jsonSchemaMap.get(this.value)
        if (schemaDetails && schemaDetails.schemaUrl) {
            console.log("Setting schema URL:", schemaDetails.schemaUrl)
            await setJsonSchema(jsonSchemaMap, jsonSchemaExampleMap, editorOutput, provider, this.value)
        } else {
            console.log("No schema URL found for", this.value)
            provider.setSessionOptions(editorOutput.session, {schemaUri: null})
        }

        // Trigger the convert button click after schema change
        const convertBtn = document.getElementById("convert-btn")
        if (convertBtn) {
            convertBtn.click()
        }
    }, false)
}

applyInitialTheme()
initOutputAceEditor()
initInputAceEditor()
initInputSchemaListener()
initOutputSchemaListener()
initThemeToggle("theme-toggle", [editorInput, editorOutput])
