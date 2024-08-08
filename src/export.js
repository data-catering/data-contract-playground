import {setJsonSchema, setupEditorSession} from "./util.js";
import {dataContractSpecificationDetails, defaultJsonSchemaName, odcsDetails} from "./config.js";

const jsonSchemaMap = new Map()
jsonSchemaMap.set("odcs", odcsDetails)
jsonSchemaMap.set("dataContractSpecification", dataContractSpecificationDetails)
const exampleMap = new Map()
let provider = LanguageProvider.fromCdn("https://cdn.jsdelivr.net/npm/ace-linters/build")
let editorInput = ace.edit("input-yaml")

async function initInputAceEditor() {
    ace.require("ace/ext/language_tools")
    setupEditorSession(editorInput, "ace/mode/yaml")
    await setJsonSchema(jsonSchemaMap, exampleMap, editorInput, provider, defaultJsonSchemaName)
}

function initInputSchemaListener() {
    const selectSchema = document.getElementById("convert-input-type")

    selectSchema.addEventListener("change", function () {
        const newSession = ace.createEditSession(exampleMap.get(this.value))
        editorInput.setSession(newSession)
        setupEditorSession(editorInput, "ace/mode/yaml")
        const schemaDetails = jsonSchemaMap.get(this.value)
        provider.setSessionOptions(editorInput.session, {schemaUri: schemaDetails.schemaUrl})
    }, false)
}

initInputAceEditor()
initInputSchemaListener()
