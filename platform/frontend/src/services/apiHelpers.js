import {HOME_URL} from "./apiConfig"

function clearCurrentUser() {
    localStorage.removeItem("currentUser")
}

function checkCurrentUser() {
    if (localStorage.getItem("currentUser")) {
        window.location = HOME_URL
        return true
    }
    return false
}

function getHeader(auth=true) {
    const header = {"Content-Type":"application/json"}
    const user = JSON.parse(localStorage.getItem("currentUser"))
    if (auth && user)
        header["Authorization"] = "Bearer " + user.access
    return header
}

function parseQuery(query) {
    const parsed = []
    for (var key in query)
        parsed.push(encodeURIComponent(key) + '=' + encodeURIComponent(query[key]))
    return parsed.join('&')
}

export {clearCurrentUser, checkCurrentUser, getHeader, parseQuery}