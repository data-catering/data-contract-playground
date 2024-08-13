export async function setJsonSchema(jsonSchemaMap, exampleMap, aceEditor, provider, defaultJsonSchemaName) {
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
            aceEditor.session.setValue(currExample)
        }
    }

    provider.setGlobalOptions("yaml", {schemas: providerSchemas})
    provider.registerEditor(aceEditor)
    provider.setSessionOptions(aceEditor.session, {schemaUri: jsonSchemaMap.get(defaultJsonSchemaName).schemaUrl})
}

export function setupEditorSession(editor, mode) {
    editor.session.setMode(mode)
    editor.setTheme("ace/theme/chrome")
    editor.setOptions({
        autoScrollEditorIntoView: true,
        customScrollbar: true,
        enableAutoIndent: true,
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        minLines: 50,
        useWorker: false,
        wrap: true
    })
}

async function getUrlContentText(url) {
    return fetch(url)
        .then(resp => resp.text())
        .catch(err => {
            console.log(err)
        })
}

