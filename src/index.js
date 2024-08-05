const jsonSchemaMap = new Map()
jsonSchemaMap.set("odcs", {
    schemaUrl: "https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/schema/odcs-json-schema-latest.json",
    exampleUrl: "https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/docs/examples/all/full-example.odcs.yaml",
    githubUrl: "https://github.com/bitol-io/open-data-contract-standard"
})
jsonSchemaMap.set("dataContractSpecification", {
    schemaUrl: "https://raw.githubusercontent.com/datacontract/datacontract-specification/main/datacontract.schema.json",
    exampleUrl: "https://raw.githubusercontent.com/datacontract/datacontract-specification/main/examples/covid-cases/datacontract.yaml",
    githubUrl: "https://github.com/datacontract/datacontract-specification"
})
jsonSchemaMap.set("dataProductSpecification", {
    schemaUrl: "https://raw.githubusercontent.com/datamesh-architecture/dataproduct-specification/main/dataproduct.schema.json",
    exampleUrl: "https://raw.githubusercontent.com/data-catering/data-contract-playground/main/example/data-product-specification/dataproduct.yaml",
    githubUrl: "https://github.com/datamesh-architecture/dataproduct-specification"
})
const exampleMap = new Map()
const defaultJsonSchemaName = "odcs"
let provider = LanguageProvider.fromCdn("https://cdn.jsdelivr.net/npm/ace-linters/build")
let editor = ace.edit("base-yaml")
const githubLinks = document.getElementById("github-links")

async function initAceEditor() {
    ace.require("ace/ext/language_tools")
    setupEditorSession()

    let providerSchemas = []
    for (const [jsonSchemaName, schemaDetails] of jsonSchemaMap.entries()) {
        const currSchema = await getUrlContentText(schemaDetails.schemaUrl)
        providerSchemas.push({
            uri: schemaDetails.schemaUrl,
            schema: currSchema
        })
        const currExample = await getUrlContentText(schemaDetails.exampleUrl)
        exampleMap.set(jsonSchemaName, currExample)

        if (jsonSchemaName === defaultJsonSchemaName) {
            editor.session.setValue(currExample)
            githubLinks.dataset.prevValue = defaultJsonSchemaName
            const githubLink = document.getElementById(`${defaultJsonSchemaName}-github-link`)
            githubLink.style.display = "block"
        }
    }

    provider.setGlobalOptions("yaml", {schemas: providerSchemas})
    provider.registerEditor(editor)
    provider.setSessionOptions(editor.session, {schemaUri: jsonSchemaMap.get(defaultJsonSchemaName).schemaUrl})
}

function initSelectSchemaListener() {
    const selectSchema = document.getElementById("data-contract-type")
    selectSchema.addEventListener("change", function () {

        const newSession = ace.createEditSession(exampleMap.get(this.value))
        editor.setSession(newSession)
        setupEditorSession()
        const schemaDetails = jsonSchemaMap.get(this.value)
        provider.setSessionOptions(editor.session, {schemaUri: schemaDetails.schemaUrl})

        const prevSchemaDetails = jsonSchemaMap.get(githubLinks.dataset.prevValue)
        const prevGithubLink = document.getElementById(`${githubLinks.dataset.prevValue}-github-link`)
        prevGithubLink.style.display = "none"
        const githubLink = document.getElementById(`${this.value}-github-link`)
        githubLink.style.display = "block"
        githubLinks.dataset.prevValue = this.value
    }, false)
}

async function getUrlContentText(url) {
    return fetch(url)
        .then(resp => resp.text())
        .catch(err => {
            console.log(err)
        })
}

function setupEditorSession() {
    editor.session.setMode("ace/mode/yaml")
    editor.setTheme("ace/theme/chrome")
    editor.setOptions({
        autoScrollEditorIntoView: true,
        customScrollbar: true,
        enableAutoIndent: true,
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        minLines: 100,
        useWorker: false,
        wrap: true
    })
}

initAceEditor()
initSelectSchemaListener()
