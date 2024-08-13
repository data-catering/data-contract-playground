import {setJsonSchema, setupEditorSession} from "./util.js";
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

    selectSchema.addEventListener("change", function () {
        const newSession = ace.createEditSession("")
        editorOutput.setSession(newSession)
        const outputOption = document.getElementById(`output-${this.value}`)
        const editorMode = outputOption.getAttribute("editor_mode")
        setupEditorSession(editorOutput, `ace/mode/${editorMode}`)
        const schemaDetails = jsonSchemaMap.get(this.value)
        provider.setSessionOptions(editorOutput.session, {schemaUri: schemaDetails.schemaUrl})
    }, false)
}

initOutputAceEditor()
initInputAceEditor()
initInputSchemaListener()
initOutputSchemaListener()
