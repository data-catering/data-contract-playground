import {setJsonSchema, setupEditorSession} from "./util.js";
import {
    dataContractSpecificationDetails,
    dataProductSpecificationDetails,
    defaultValidateJsonSchemaName,
    odcsDetails,
    odcsV3Details
} from "./config.js";

const jsonSchemaMap = new Map()
jsonSchemaMap.set("odcs", odcsDetails)
jsonSchemaMap.set("odcs-v3", odcsV3Details)
jsonSchemaMap.set("dataContractSpecification", dataContractSpecificationDetails)
jsonSchemaMap.set("dataProductSpecification", dataProductSpecificationDetails)

const exampleMap = new Map()
let provider = LanguageProvider.fromCdn("https://cdn.jsdelivr.net/npm/ace-linters/build")
let editor = ace.edit("base-yaml")
const githubLinks = document.getElementById("github-links")

async function initAceEditor() {
    ace.require("ace/ext/language_tools")
    setupEditorSession(editor, "ace/mode/yaml")

    githubLinks.dataset.prevValue = defaultValidateJsonSchemaName
    const githubLink = document.getElementById(`${defaultValidateJsonSchemaName}-github-link`)
    githubLink.style.display = "block"
    await setJsonSchema(jsonSchemaMap, exampleMap, editor, provider, defaultValidateJsonSchemaName)
}

function initSelectSchemaListener() {
    const selectSchema = document.getElementById("data-contract-type")

    selectSchema.addEventListener("change", function () {
        const newSession = ace.createEditSession(exampleMap.get(this.value))
        editor.setSession(newSession)
        setupEditorSession(editor, "ace/mode/yaml")
        const schemaDetails = jsonSchemaMap.get(this.value)
        provider.setSessionOptions(editor.session, {schemaUri: schemaDetails.schemaUrl})

        const prevGithubLink = document.getElementById(`${githubLinks.dataset.prevValue}-github-link`)
        prevGithubLink.style.display = "none"
        const githubLink = document.getElementById(`${this.value}-github-link`)
        githubLink.style.display = "block"
        githubLinks.dataset.prevValue = this.value
    }, false)
}

initAceEditor()
initSelectSchemaListener()
