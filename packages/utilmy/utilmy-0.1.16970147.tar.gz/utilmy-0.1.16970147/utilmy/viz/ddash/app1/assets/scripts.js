const PATH              = {
                            'html'          :'assets/html/',
                            'dash'          :'pages/'
                         }
const html              = 'html'
const NUMERIC           = new RegExp(/^[0-9]*$/)
const VALID_LINKS       = new RegExp('^(http[s]?:\\/\\/(www\\.)?|www\\.){1}([0-9A-Za-z-\\.@:%_\+~#=]+)+((\\.[a-zA-Z]{2,3})+)(/(.)*)?(\\?(.)*)?')
const LINE_BREAKS       = /[\r\n]/gm

let render_editor       = false
let editor              = Object

function editorInstance(container) {
    const options         = {
                                mode    : 'code',
                                modes   : ['code', 'preview'], // allowed modes
                            }
    return new JSONEditor(container, options)
  }

window.dash_clientside  = Object.assign({}, window.dash_clientside, {
    clientside: {
        render: function(targetRender, homePage) {

            if (targetRender.length == 0){
                // Handle Initial targetRender to homePage

                if (VALID_LINKS.test(homePage)){
                    return homePage
                } else if (homePage.endsWith(html)) {
                    return `${PATH[html]}${homePage}` 
                } else if (homePage.endsWith('.py')) {
                    return `${PATH['dash']}${homePage}`
                }
            } else {
                let target = targetRender[0]

                if (!NUMERIC.test(target)){ // Filter targetRender not Number
    
                    if (VALID_LINKS.test(target)){
                        return target 
                    } else if (target.endsWith(html)){
                        return `${PATH[html]}${target}`
                    } else if (target.endsWith('.py')) {
                        return `${PATH['dash']}${target}`
                    }
    
                }

            }

            return dash_clientside.no_update 
            
        },
        liveEditor: function(content, filename) {
            
            html_container = document.getElementById("jsoneditor")

            if (html_container.childElementCount == 0){
                editor = editorInstance(html_container)
            }
            
            
            if (content != undefined){
                // Parsing content
                let [contentType, contentString] = content.split(',')
                let JsonString                   = "{}"

                try {
                    if (filename.endsWith('.json')) {
                        JsonString               = atob(contentString).replace(LINE_BREAKS, '')
                    } else {
                        alert("File must in Json extension");
                        return ""
                    }

                } catch (err) {
                    console.log('There was an error in ', err)
                    return ""
                }


                editor.set(JSON.parse(JsonString))

                return filename
            }

            return ""

        
        }, saveJSON : function(nClick) {
            if (nClick != undefined){
                return editor.get()
            }
                
        }
    }
});