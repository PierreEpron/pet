const REACT_APP_API_URL = "http://localhost:8000/api"
const HOME_URL = "/HomePage"
const SIGNIN_URL = "/"

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

function get_header(auth=true) {
    const header = {"Content-Type":"application/json"}
    const user = JSON.parse(localStorage.getItem("currentUser"))
    if (auth && user)
        header["Authorization"] = "Bearer " + user.access
    return header
}

export {REACT_APP_API_URL, HOME_URL, SIGNIN_URL, get_header, checkCurrentUser, clearCurrentUser}