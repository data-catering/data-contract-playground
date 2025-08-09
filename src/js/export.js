import {getCurrentAceTheme, setJsonSchema, setupEditorSession} from "./util.js";
import {applyInitialTheme, initThemeToggle} from "./theme.js";
import {dataContractSpecificationDetails, defaultJsonSchemaName, odcsDetails} from "./config.js";

const jsonSchemaMap = new Map()
jsonSchemaMap.set("odcs", odcsDetails)
jsonSchemaMap.set("dataContractSpecification", dataContractSpecificationDetails)
const exampleMap = new Map()
let provider = LanguageProvider.fromCdn("https://cdn.jsdelivr.net/npm/ace-linters/build")
let editorInput = ace.edit("input-yaml")
let editorOutput = null

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

applyInitialTheme()
initInputAceEditor()
initInputSchemaListener()
initThemeToggle("theme-toggle", [editorInput])

// Ensure output editor adopts current theme when it's initialized (PyScript or lazy)
function ensureOutputThemeSync() {
    const target = document.getElementById('output-text')
    if (!target) return
    const applyTheme = () => {
        try {
            editorOutput = ace.edit("output-text")
            editorOutput.setTheme(getCurrentAceTheme())
        } catch (e) {}
    }
    if (target.querySelector('.ace_scroller')) { applyTheme(); return }
    const observer = new MutationObserver(() => {
        if (target.querySelector('.ace_scroller')) { applyTheme(); observer.disconnect() }
    })
    observer.observe(target, { childList: true, subtree: true })
}
ensureOutputThemeSync()

// Also update output editor theme on toggle
const themeBtn = document.getElementById("theme-toggle")
if (themeBtn) {
    themeBtn.addEventListener("click", () => {
        if (editorOutput) {
            try { editorOutput.setTheme(getCurrentAceTheme()) } catch (e) {}
        }
    })
}
