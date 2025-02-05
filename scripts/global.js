async function getRootPage(){
    window.location.replace(window.location.origin);
}

async function getPage(page){
    window.location.replace(window.location.origin+'/'+page);
}